#!/usr/bin/env python
import asyncio, websockets
import datetime
import random, string, json

sockets = {}

def uniqueID(size=12, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

async def sendUser(data):
    if sockets[data['host']]:
        sigJSON = json.dumps({'type': 'signature', 'signature': data['signature']})
        await sockets[data['host']].send(sigJSON)

async def main(websocket, path):
    uID = uniqueID() # a unique id for connection
    sockets[uID] = websocket
    uIDJson = json.dumps({'type': 'uID', 'uID': uID})
    await websocket.send(uIDJson)

    for key,val in sockets.items():
        print(key, "=>", val)

    try:
        async for message in websocket:
            print(message)
            data = json.loads(message)
            for key,val in sockets.items():
                print(key, "=>", val)

            # if its a login attempt
            if(data['type'] == 'loginSig'):
                await sendUser(data)


        while True:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            await websocket.send("Hello world")
            print(len(USERS))
            await asyncio.sleep(random.random() * 3)

    finally:
        del sockets[uID]

start_server = websockets.serve(main, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
