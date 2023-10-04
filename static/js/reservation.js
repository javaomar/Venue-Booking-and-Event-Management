const reservation_socket = new WebSocket(
    'ws://'
    +window.location.host
    +'/ws/'
    +'reservation/'
)


reservation_socket.onopen = function(e){
    console.log('RESERVATION CONNECTED')
}

reservation_socket.onclose = function(e){
    console.log('RESERVATION CLOSE')
}

reservation_socket.onerror = function(e){
    console.log('websocket error',e);
}

var reserv_count_badge = document.getElementById('reserv_count_badge')

reservation_socket.onmessage = function(e){
    const data = JSON.parse(e.data)
    reserv_count_badge.innerHTML = data.count 
    console.log(e)
}

 
 