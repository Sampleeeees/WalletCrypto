const socket = io('ws://127.0.0.1:8000', {path: '/ws/socket.io'});
const user_cookie = document.cookie
const block_message = $('#block_message')




socket.on('connect', () => {
    console.log('connected')
    socket.emit('test', user_cookie)
})



socket.on('disconnect', () => {
    console.log('disconnect')
})

function send_message(){
    // let header_avatar = $('#header_avatar')
    let message = $('#my_message')[0]
    console.log(message.value)
    // let my_message_block = `<li class="chat-message chat-message-right">
    //                         <div class="d-flex overflow-hidden">
    //                           <div class="chat-message-wrapper flex-grow-1">
    //                             <div class="chat-message-text">
    //                               <p class="mb-0">${message.value}</p>
    //                             </div>
    //                             <div class="text-end text-muted mt-1">
    //                               <i class="ti ti-checks ti-xs me-1 text-success"></i>
    //                               <small>10:00 AM</small>
    //                             </div>
    //                           </div>
    //                           <div class="user-avatar flex-shrink-0 ms-3">
    //                             <div class="avatar avatar-sm">
    //                               <img src="${header_avatar.src}" alt="Avatar" class="rounded-circle" />
    //                             </div>
    //                           </div>
    //                         </div>
    //                       </li>`
    // console.log(message.value)
    socket.emit('my_message', message.value)
    // block_message.append(my_message_block)
}

socket.on('message', (data) => {
    let user_chat_image = ''
    if (data.avatar){
        user_chat_image = data.avatar
    }else{
        user_chat_image = base_image
    }
    console.log('Message:', data.message, 'User id:', data.user_id, user_id.text())
    if (data.user_id === parseInt(user_id.text())){
        console.log('My message')
        let my_message_block = `<li class="chat-message chat-message-right">
                            <div class="d-flex overflow-hidden">
                              <div class="chat-message-wrapper flex-grow-1">
                                <div class="chat-message-text">
                                  <p class="mb-0">${data.message}</p>
                                </div>
                                <div class="text-end text-muted mt-1">
                                  <i class="ti ti-checks ti-xs me-1 text-success"></i>
                                  <small>${new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</small>
                                </div>
                              </div>
                              <div class="user-avatar flex-shrink-0 ms-3">
                                <div class="avatar avatar-sm">
                                  <img src="${user_chat_image}" alt="Avatar" class="rounded-circle" />
                                </div>
                              </div>
                            </div>
                          </li>`
    block_message.append(my_message_block)
    }else{
        let other_message_block = ` <li class="chat-message">
                            <div class="d-flex overflow-hidden">
                              <div class="user-avatar flex-shrink-0 me-3">
                                <div class="avatar avatar-sm">
                                  <img src="${user_chat_image}" alt="Avatar" class="rounded-circle" />
                                </div>
                              </div>
                              <div class="chat-message-wrapper flex-grow-1">
                                <div class="chat-message-text">
                                  <p class="mb-0">${data.message}</p>
                                </div>
                                <div class="text-muted mt-1">
                                  <small>${new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}</small>
                                </div>
                              </div>
                            </div>
                          </li>`
        block_message.append(other_message_block)
    }

})