const socket = io('ws://127.0.0.1:8000', {path: '/ws/socket.io'});
const user_cookie = document.cookie
const block_message = $('#block_message')
const insert_image = $('#insert_image_chat')[0]
const check_image = $('#check_image')



socket.on('connect', () => {
    console.log('connected')
    socket.emit('test', user_cookie)
})



socket.on('disconnect', () => {
    console.log('disconnect')
})

function get_image(image){
    console.log('Image', image.files[0]);
    let header_name_image = $('#header_name_image');
    let name_image = $('#name_insert_image')[0];
    let chat_image = image.files[0];
    if (chat_image.type !== 'image/jpeg' && chat_image.type !== 'image/png' && chat_image.type !== 'image/jpg') {
        toastr.error('Дозволені лише файли типу "jpeg", "png" та "jpg"')
    }else{
        name_image.innerText = chat_image.name;
        header_name_image.text(chat_image.name);
        console.log(name_image);
        show_preview_chat_image(chat_image);}
}

function show_preview_chat_image(image){
    let modal_image = image;
    if (modal_image){
        const reader = new FileReader();

        reader.onload = function (event) {
            const modal_image_result = event.target.result;
            // Assuming check_image is an <img> element
            $('#check_image').attr('src', modal_image_result);
        };

        reader.readAsDataURL(modal_image);
    }
}


function delete_image(){
    insert_image.value = '';
    $('#name_insert_image')[0].innerText = '';
}

function send_message(){
    let message = $('#my_message')[0]
    let image = insert_image.files[0];
    let name_image = $('#name_insert_image')[0];
    console.log('Image', image)
    if (message.value || image){
        if (image) {
            const reader = new FileReader();

            reader.onload = function (event) {
                const modal_image_result = event.target.result;
                name_image.innerText = '';
                insert_image.value = '';
                // socket.emit('my_message', {'message': message.value, 'image': modal_image_result})

            };

            reader.readAsDataURL(image);

        } else {
            console.log(message.value)
            socket.emit('my_message', {'message': message.value, 'image': null})
        }
    }else{
        toastr.error('Введіть в поле якесь повідомлення', 'Error')
    }
}

socket.on('message', (data) => {
    let user_chat_image = ''
    let img_class = 'd-none'
    let img_src = null

    if(data.image){
        img_class = '';
        img_src = data.image
    }


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
                                  <img class="${img_class}" src="${img_src}" alt="">
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