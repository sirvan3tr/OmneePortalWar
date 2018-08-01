from web3.auto import w3
from eth_account.messages import defunct_hash_message
import json, binascii
from hexbytes import HexBytes

import asyncio
import websockets

# Acting like the mobile phone
msg = 'bmMfnO5HE2m2'
pk = '0xb50c18d670e82f3f559142d63773b5f60882d337f7d40e78f87973484740ab0d'
msgHash = defunct_hash_message(text=msg)

signedMsg = w3.eth.account.signHash(msgHash, private_key=pk)
#hexdecimal = "".join(["{:02X}".format(b) for b in hb])
#print(hexdecimal)
hexSig = binascii.hexlify(signedMsg.signature)
sig = str(hexSig).split("'")[1]
print('------------------------------')
print(w3.eth.account.recoverHash(msgHash, signature=signedMsg.signature))
print('------------------------------')


v = json.dumps({
			'type' : 'loginSig',
			'host' : msg,
			'signature' : str(sig)
		})

print(v)



async def hello():
    async with websockets.connect(
            'ws://localhost:5678') as websocket:

        await websocket.send(v)

asyncio.get_event_loop().run_until_complete(hello())