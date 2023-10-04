const notify_socket = new WebSocket(
    'ws://'
    +window.location.host
    +'/ws/'
    +'notify/'
)

notify_socket.onopen = function(e){
    console.log('NOTIFICATION CONNECTED')
   
}

notify_socket.onclose = function(e){
    console.log('CLOSE CONNECTION')

}

//getting hold of the id in room.html
var count_badge = document.getElementById('count_badge')

//sending data to  the room.html to display it 
notify_socket.onmessage = function(e){
    // const data = JSON.parse(e.data)
    // console.log(data.count)
    // count_badge.innerHTML = data.count
    try {
        const data = JSON.parse(e.data);
        console.log(data.count);
        count_badge.innerHTML = data.count;
    } catch (error) {
        console.error('Error in onmessage handler:', error);
    }
 
}