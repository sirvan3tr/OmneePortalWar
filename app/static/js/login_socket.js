// Generate a random string, that will act as a unique ID for our URL
// currently not used -- maybe as a method to stop replay attack later


function createID() {
    var text = "",
        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < 20; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

var ws = new WebSocket("ws://127.0.0.1:5678/"),
    messages = document.createElement('ul'),
    submit = document.getElementById('mysubmit');

ws.onopen = function() {
    console.log('Opened websocket');
};

sessionInfo = {'uID' : '', 'signature': ''};
ws.onmessage = function (event) {
    var content = document.createTextNode(event.data),
        dataJSON = JSON.parse(event.data);

    if (dataJSON['type'] == "uID") {
        console.log('We have uID');
        console.log(dataJSON['uID']);
        sessionInfo['uID'] = dataJSON['uID'];
        document.getElementById('session-id').innerHTML = dataJSON['uID'];
        var qr = new QRious({
          element: document.getElementById('qr'),
          size: 200,
          value: dataJSON['uID']
        });
    } else if(dataJSON['type'] == 'signature') {
        console.log('We have signature');
        console.log(dataJSON['signature']);
        sessionInfo['signature'] = dataJSON['signature'];
        console.log(sessionInfo);
    }

    console.log(event.data);

    if (sessionInfo['signature'] != '') {
        endURL = sessionInfo['uID']+'/'+sessionInfo['signature'];
        window.location.href = 'http://localhost:5000/login/confirm/'+endURL
    }

    //console.log(window.location.href = 'http://localhost:5000/login/'+event.data;
};


document.getElementById('loading').style.visibility = 'hidden';
document.getElementById('login-content').style.visibility = 'visible';