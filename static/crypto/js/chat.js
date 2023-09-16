const latest_message = window.location.origin + "/api/v1/messages/"
const block_message = $('#block_message')
const chat_history = $('#chat_history')
const insert_image = $('#insert_image_chat')[0]
const check_image = $('#check_image')
const online_block = $('#contact-list')


let chatHistoryBody = document.querySelector('.chat-history-body');

// Ініціалізуємо PerfectScrollbar
let ps = new PerfectScrollbar(chatHistoryBody);

$(document).ready(function (){
    get_10_last_messages()

})


// Функція для відображення списку онлайн користувачів
function updateUsersList(users) {
    console.log('users', users)
    users.forEach((user) => {
            let user_img = base_image
        if ((parseInt(user_id.text())) === user.user_id){}else{
            if(user.avatar){
                user_img = user.avatar
            }
            let user_data = `<li class="chat-contact-list-item">
                                  <a class="d-flex align-items-center">
                                    <div class="flex-shrink-0 avatar avatar-online">
                                      <img src="${user_img}" alt="Avatar" class="rounded-circle">
                                    </div>
                                    <div class="chat-contact-info flex-grow-1 ms-2">
                                      <h6 class="chat-contact-name text-truncate m-0">${user.username}</h6>
                                    </div>
                                  </a>
                                </li>`
            online_block.append(user_data)

    }})
}

// Отримання та відображення списку онлайн користувачів
socket.on('update_users_status', (users) => {
    online_block[0].innerHTML = '';
    updateUsersList(users);
});

socket.on('transaction', (data) => {
    console.log('Hello')
    console.log('Sokcet data', data)
    toastr.success(`${data}`, 'Hello')
})



function get_image(image){
    let header_name_image = $('#header_name_image');
    let name_image = $('#name_insert_image')[0];
    let chat_image = image.files[0];
    if (chat_image.type !== 'image/jpeg' && chat_image.type !== 'image/png' && chat_image.type !== 'image/jpg') {
        toastr.error('Дозволені лише файли типу "jpeg", "png" та "jpg"')
    }else{
        name_image.innerText = chat_image.name;
        header_name_image.text(chat_image.name);
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
                socket.emit('my_message', {'message': message.value, 'image': modal_image_result})

            };

            reader.readAsDataURL(image);

        } else {
            console.log(message.value)
            socket.emit('my_message', {'message': message.value, 'image': null})
        }
        message.value = '';
    }else{
        toastr.error('Введіть в поле якесь повідомлення', 'Error')
    }

}

socket.on('message', (data) => {
    let user_chat_image = ''
    let img_class = 'd-none'
    let img_src = null

    let my_date = new Date().toLocaleDateString(['en-US'], {day: 'numeric', month: 'long'}) + ', ' +new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});

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
                                  <img width="auto" style="max-width: 250px;" height="auto" class="${img_class} mt-2" src="${img_src}" alt="">
                                </div>
                                <div class="text-end text-muted mt-1">
                                  <i class="ti ti-checks ti-xs me-1 text-success"></i>
                                  <small>${my_date}</small>
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
                                  <img width="auto" style="max-width: 250px;" height="auto" class="${img_class} mt-2" src="${img_src}" alt="">
                                </div>
                                <div class="text-muted mt-1">
                                  <small>${my_date}</small>
                                </div>
                              </div>
                            </div>
                          </li>`
        block_message.append(other_message_block)
    }
    chatHistoryBody.scrollTop = chatHistoryBody.scrollHeight;
})

function get_10_last_messages(){
    $.ajax({
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        url: latest_message,
        success: function (data){
            console.log('10 message', data)
            for(let i = data.length - 1; i >= 0; i--) {
                let user_chat_image = null;
                let img_class = 'd-none'
                let img_src = null
                let my_date = new Date(data[i].date_send).toLocaleDateString(['en-US'], {day: 'numeric', month: 'long'}) + ', ' +new Date(data[i].date_send).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
                if (data[i].image) {
                    img_class = '';
                    img_src = data[i].image
                }

                if (data[i].avatar){
                    user_chat_image = data[i].avatar
                }else{
                    user_chat_image = base_image
                }

                if (data[i].user_id === parseInt(user_id.text())) {
                    let my_message_block = `<li class="chat-message chat-message-right">
                            <div class="d-flex overflow-hidden">
                              <div class="chat-message-wrapper flex-grow-1">
                                <div class="chat-message-text">
                                  <p class="mb-0">${data[i].content}</p>
                                  <img width="auto" style="max-width: 250px;" height="auto" class="${img_class} mt-2" src="${img_src}" alt="">
                                </div>
                                <div class="text-end text-muted mt-1">
                                  <i class="ti ti-checks ti-xs me-1 text-success"></i>
                                  <small>${my_date}</small>
                                </div>
                              </div>
                              <div class="user-avatar flex-shrink-0 ms-3">
                                <div class="avatar avatar-sm">                           
                                  <img src="${user_chat_image}" alt="${data[i].username}" title="${data[i].username}" class="rounded-circle" />
                                </div>
                              </div>
                            </div>
                          </li>`
                    block_message.append(my_message_block)
                } else {
                    let other_message_block = ` <li class="chat-message">
                            <div class="d-flex overflow-hidden">
                              <div class="user-avatar flex-shrink-0 me-3">
                                <div class="avatar avatar-sm">
                                  <img src="${user_chat_image}" alt="${data[i].username}" title="${data[i].username}" class="rounded-circle" />
                                </div>
                              </div>
                              <div class="chat-message-wrapper flex-grow-1">
                                <div class="chat-message-text">
                                  <p class="mb-0">${data[i].content}</p>
                                  <img width="auto" style="max-width: 250px;" height="auto" class="${img_class} mt-2" src="${img_src}" alt="">
                                </div>
                                <div class="text-muted mt-1">
                                  <small>${my_date}</small>
                                </div>
                              </div>
                            </div>
                          </li>`
                    block_message.append(other_message_block)
                }
            }chatHistoryBody.scrollTop = chatHistoryBody.scrollHeight;
        }

    }
    )
}

// send message when you press enter
$(document).keydown(function(e) {
    if (e.keyCode === 13) {
        send_message()
    }
})
