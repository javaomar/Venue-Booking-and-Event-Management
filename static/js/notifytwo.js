const notify_sockettwo = new WebSocket(
    'ws://'
    +window.location.host
    +'/ws/'
    +'notifytwo/'
)

notify_sockettwo.onopen = function(e){
    console.log('NOTIFICATION CONNECTED TWO')
   
}

notify_sockettwo.onclose = function(e){
    console.log('CLOSE CONNECTION')

}

//getting hold of the id in room.html
var count_badge = document.getElementById('count_badgetwo')

//sending data to  the room.html to display it 
notify_sockettwo.onmessage = function(e){
    // const data = JSON.parse(e.data)
    // console.log(data.count)
    // count_badge.innerHTML = data.count
    try {
        const data = JSON.parse(e.data);
        console.log(data.count);
        count_badge.innerHTML = 1
    } catch (error) {
        console.error('Error in onmessage handler:', error);
    }
 
}