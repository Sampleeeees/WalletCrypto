const socket = io('ws://127.0.0.1:8000', {path: '/ws/socket.io'});
const user_cookie = document.cookie

socket.on('connect', () => {
    console.log('connected')
    socket.emit('test', user_cookie)
})

socket.on('disconnect', () => {
    console.log('disconnect')
})

