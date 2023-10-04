const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);




const socket = new WebSocket(
    'ws://'
    +window.location.host
    +'/ws/'
    +id
    +'/'
);


socket.onopen = function(e){
    console.log('CONNECTION MADE');
}


socket.onclose = function(e){
    console.log('NO CONNECTION');
    if (e.wasClean) {
        console.log(`Connection closed cleanly, code=${e.code}, reason=${e.reason}`);
    } else {
        console.log('error is ',e);
    }
}
socket.onerror = function(e){
    console.log('websocket error',e);
 
}

socket.onmessage = function(e){
    console.log(e.data)
    const data = JSON.parse(e.data)

    if(data.username == message_username){
        document.querySelector("#chat-body").innnerHTML += `
        <tr>
        <td>
            <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                ${data.message}
                
            </p>
        </td>
        </tr>
        `
    }else{ document.querySelector('#chat-body').innerHTML += `
    <tr>
    <td>
        <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
            ${data.message}
        </p>
    </td>
    </tr>
    `
    }
}




document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username,
        'receiver':receiver
    }));

    message_input.value = '';
}