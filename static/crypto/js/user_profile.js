// API urls
const user_profile_url = window.location.origin + "/api/v1/user/profile/"
const user_wallets_url = window.location.origin + "/api/v1/wallets/current-user/"
const user_messages_url = window.location.origin + "/api/v1/message/current-user/"
const user_update_profile_url = window.location.origin + '/api/v1/user/'
const wallet_create_url = window.location.origin + '/api/v1/wallet/'
const wallet_import_url = window.location.origin + '/api/v1/wallet/import/'

// Profile forms
const profile_email = $('#profile_email')
const profile_username = $('#profile_username')
const profile_user_username = $('#profile_user_username')
const profile_password = $('#profile_password')
const profile_password_repeat = $('#profile_password_repeat')
const user_avatar = $("#user_avatar")
const wallet_import = $("#modalImportWallet")

// Save old data in form user
let old_username = ''
let old_image_src = ''

// basic image, name
const dropdown_image = $("#dropdown_image")
const header_avatar = $('#header_avatar')
const user_basic_username = $("#user_basic_username")

// users message and wallet
const messages_count = $("#profile_count_messages")
const wallets_count = $("#profile_count_wallets")

const block_wallets = $('#block_wallets')

// Завантаження даних при завантаженні сторінки
$(document).ready(function (){
    load_user_profile()
    get_wallets()
    get_count_messages()
})

// Отримання всіх повідомлень авторизованого користувача
function get_count_messages(){
    $.ajax({
        method: "GET",
        headers: {
            'Content-Type': 'application-json'
        },
        url: user_messages_url,
        success: function (data){
            messages_count.text(data.length)
        }
    })
}

// Запит на дані користувача
function load_user_profile(){
    $.ajax({
        method: 'GET',
        headers: {
            "Content-Type": 'application/json'
        },
        url: user_profile_url,
        success: function (data){
            console.log(data)
            profile_email.val(data.email)
            profile_username.val(data.username)
            profile_user_username.text(data.username)
            old_username = data.username
            if (data.avatar){
                user_avatar.attr('src', data.avatar)
                old_image_url = data.avatar
            }

        }
    })
}

// Запит на отримання всіх гаманців юзера
function get_wallets(){
    $.ajax({
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
        url: user_wallets_url,
        success: function (data){
            console.log(data)
            wallets_count.text(data.length)
            let wallets_block = $('#block_wallets')
            if (data.length === 0){
                let no_wallet = '<h3 class="m-4">No Wallets</h3>'
                wallets_block.append(no_wallet)
            }else{
            for (let i of data){
                let eth_svg = '<svg width="35px" height="35px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n' +
                    '                    <path fill="#8d6c9f" d="M63 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C64 35.553 63.553 36 63 36zM58 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C59 35.553 58.553 36 58 36zM53 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C54 35.553 53.553 36 53 36zM11 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C12 35.553 11.552 36 11 36zM6 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C7 35.553 6.552 36 6 36zM1 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C2 35.553 1.552 36 1 36z"></path><path fill="#ace3ff" d="M15 32L32 2 49 32 32 42.909z"></path><path fill="#85cbf8" d="M32 2L49 32 32 42.909z"></path><path fill="#ace3ff" d="M15 37L32 47 49 37 32 62z"></path><path fill="#85cbf8" d="M32 47L49 37 32 62zM15 32L32 23.818 49 32 32 42.909z"></path><path fill="#7bbeeb" d="M32 23.818L49 32 32 42.909z"></path><g><path fill="#8d6c9f" d="M32,43.909c-0.188,0-0.375-0.053-0.54-0.158l-17-10.909c-0.447-0.287-0.592-0.873-0.33-1.335l17-30 c0.355-0.626,1.385-0.626,1.74,0l17,30c0.262,0.462,0.117,1.048-0.33,1.335l-17,10.909C32.376,43.856,32.188,43.909,32,43.909z M16.336,31.669L32,41.721l15.663-10.051L32,4.028L16.336,31.669z"></path><path fill="#8d6c9f" d="M32,43.909c-0.165,0-0.33-0.041-0.479-0.122C31.2,43.611,31,43.274,31,42.909V2 c0-0.454,0.306-0.851,0.745-0.967c0.441-0.116,0.901,0.079,1.125,0.474l17,30c0.262,0.462,0.117,1.048-0.33,1.335l-17,10.909 C32.376,43.856,32.188,43.909,32,43.909z M33,5.793v35.286l14.663-9.41L33,5.793z"></path><path fill="#8d6c9f" d="M32,63c-0.331,0-0.64-0.163-0.826-0.437l-17-24.909c-0.268-0.393-0.222-0.92,0.109-1.261 c0.332-0.34,0.857-0.4,1.257-0.145L32,46.812l16.46-10.562c0.399-0.257,0.926-0.196,1.257,0.145 c0.332,0.341,0.377,0.868,0.109,1.261l-17,24.909C32.64,62.837,32.33,63,32,63z M18.597,40.587L32,60.226l13.403-19.639 L32.54,48.842c-0.328,0.212-0.75,0.211-1.08,0L18.597,40.587z"></path><path fill="#8d6c9f" d="M32 63c-.098 0-.198-.015-.295-.045C31.286 62.826 31 62.438 31 62V48c0-.341.173-.657.46-.842l17-10.909c.399-.257.926-.196 1.257.145.332.341.377.868.109 1.261l-17 24.909C32.636 62.842 32.324 63 32 63zM33 48.547v10.214l12.403-18.174L33 48.547zM32 43.909c-.188 0-.375-.053-.54-.158l-17-10.909c-.305-.196-.48-.541-.458-.903.022-.361.238-.683.564-.84l17-8.182c.274-.132.594-.132.867 0l17 8.182c.326.157.542.479.564.84.022.362-.153.707-.458.903l-17 10.909C32.376 43.856 32.188 43.909 32 43.909zM17.046 32.125L32 41.721l14.954-9.596L32 24.928 17.046 32.125z"></path><path fill="#8d6c9f" d="M32,43.909c-0.165,0-0.33-0.041-0.479-0.122C31.2,43.611,31,43.274,31,42.909V23.818 c0-0.344,0.177-0.664,0.468-0.847c0.291-0.183,0.654-0.205,0.966-0.054l17,8.182c0.326,0.157,0.542,0.479,0.564,0.84 c0.022,0.362-0.153,0.707-0.458,0.903l-17,10.909C32.376,43.856,32.188,43.909,32,43.909z M33,25.409v15.67l13.954-8.954 L33,25.409z"></path></g>\n' +
                    '                </svg>'
                let wallet_address = '<p class="my-auto ms-3 border border-1 border-gray rounded p-1">'+ i.address +'</p>'
                let block = '<div class="d-flex m-4">' + eth_svg + wallet_address +'</div>'
                wallets_block.append(block)
            }
        }
        }
    })
}

// Видалення зображення
function delete_image(){
    let check_blank_image = user_avatar[0].src.indexOf('basic.jpg')

    if (check_blank_image === -1) {
        $.ajax({
            method: "PATCH",
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({"avatar": 'delete'}),
            url: user_update_profile_url,
            success: function (data) {
                if (data.avatar == null) {
                    toastr.success('Фото було успішно видалено', 'Success')
                    user_avatar.attr('src', basic_image)
                    header_avatar.attr('src', basic_image)
                    dropdown_image.attr('src', basic_image)
                }
            }

        })
    }else{
        toastr.error('У вас і так немає зображення', 'Error')
    }
}

// Перетворення фото в base64
function imageInBase64(image){
    return new Promise((resolve) => {
        let reader = new FileReader();

        reader.onloadend = function (){
            resolve(reader.result)
        };

        reader.onerror = function (){
            toastr.error('Помилка читання файлу', 'Error')
        };

        reader.readAsDataURL(image)
    })
}

// Показ фото в полі ще до того як натиснути завантажити
async function previewImage(photo){
    let image = photo.files[0]
    if (image.type !== 'image/jpeg' && image.type !== 'image/png' && image.type !== 'image/jpg') {
        toastr.error('Дозволені лише файли типу "jpeg", "png" та "jpg"')
    }else{
        user_avatar.attr("src", URL.createObjectURL(image))
        let image_base64 = await imageInBase64(image)
}}

// Оновлення інформації про користувача
async function update_user_profile(){
    let new_username = profile_username.val()
    let new_image = user_avatar[0].src
    let new_pass = profile_password.val()
    let new_pass_repeat = profile_password_repeat.val()
    let check_image = new_image.indexOf('basic.jpg')


    if (old_username === profile_username.val()){
        new_username = null
    }

    if (check_image !== -1){
        new_image = null
    }else{
        new_image = await imageInBase64($('#upload_image')[0].files[0])
    }


    if (profile_password.val() !== profile_password_repeat.val()){
        toastr.error('Паролі не співпадають', 'Error')
        return;
    }

    if (!profile_password.val() || !profile_password_repeat){
        new_pass = null
        new_pass_repeat = null
    }

    $.ajax({
        method: 'PATCH',
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json'
        },
        url: user_update_profile_url,
        data: JSON.stringify({
                  "username": new_username,
                  "avatar": new_image,
                  "password": new_pass,
                  "repeat": new_pass_repeat
                }),
        success: function (data){
            console.log(data)
            profile_user_username.text(data.username)
            toastr.success('Профіль оновлено успішно!', 'Success')
        },
        error: function (data){
            console.log('Error', data)
            toastr.error(data.responseJSON.detail, 'Error')
        }
    })
}


// Створення гаманця
function create_wallet(){
    let wallets_block = $('#block_wallets')
    $.ajax({
        method: 'POST',
        dataType: 'json',
        processData: false,
        contentType: false,
        cache: false,
        headers: {
            'Content-Type': 'application/json'
        },
        url: wallet_create_url,
        success: function (data){
            toastr.success('Гаманець було успішно створено', 'Success')
            let eth_svg = '<svg width="35px" height="35px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n' +
                    '                    <path fill="#8d6c9f" d="M63 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C64 35.553 63.553 36 63 36zM58 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C59 35.553 58.553 36 58 36zM53 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C54 35.553 53.553 36 53 36zM11 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C12 35.553 11.552 36 11 36zM6 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C7 35.553 6.552 36 6 36zM1 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C2 35.553 1.552 36 1 36z"></path><path fill="#ace3ff" d="M15 32L32 2 49 32 32 42.909z"></path><path fill="#85cbf8" d="M32 2L49 32 32 42.909z"></path><path fill="#ace3ff" d="M15 37L32 47 49 37 32 62z"></path><path fill="#85cbf8" d="M32 47L49 37 32 62zM15 32L32 23.818 49 32 32 42.909z"></path><path fill="#7bbeeb" d="M32 23.818L49 32 32 42.909z"></path><g><path fill="#8d6c9f" d="M32,43.909c-0.188,0-0.375-0.053-0.54-0.158l-17-10.909c-0.447-0.287-0.592-0.873-0.33-1.335l17-30 c0.355-0.626,1.385-0.626,1.74,0l17,30c0.262,0.462,0.117,1.048-0.33,1.335l-17,10.909C32.376,43.856,32.188,43.909,32,43.909z M16.336,31.669L32,41.721l15.663-10.051L32,4.028L16.336,31.669z"></path><path fill="#8d6c9f" d="M32,43.909c-0.165,0-0.33-0.041-0.479-0.122C31.2,43.611,31,43.274,31,42.909V2 c0-0.454,0.306-0.851,0.745-0.967c0.441-0.116,0.901,0.079,1.125,0.474l17,30c0.262,0.462,0.117,1.048-0.33,1.335l-17,10.909 C32.376,43.856,32.188,43.909,32,43.909z M33,5.793v35.286l14.663-9.41L33,5.793z"></path><path fill="#8d6c9f" d="M32,63c-0.331,0-0.64-0.163-0.826-0.437l-17-24.909c-0.268-0.393-0.222-0.92,0.109-1.261 c0.332-0.34,0.857-0.4,1.257-0.145L32,46.812l16.46-10.562c0.399-0.257,0.926-0.196,1.257,0.145 c0.332,0.341,0.377,0.868,0.109,1.261l-17,24.909C32.64,62.837,32.33,63,32,63z M18.597,40.587L32,60.226l13.403-19.639 L32.54,48.842c-0.328,0.212-0.75,0.211-1.08,0L18.597,40.587z"></path><path fill="#8d6c9f" d="M32 63c-.098 0-.198-.015-.295-.045C31.286 62.826 31 62.438 31 62V48c0-.341.173-.657.46-.842l17-10.909c.399-.257.926-.196 1.257.145.332.341.377.868.109 1.261l-17 24.909C32.636 62.842 32.324 63 32 63zM33 48.547v10.214l12.403-18.174L33 48.547zM32 43.909c-.188 0-.375-.053-.54-.158l-17-10.909c-.305-.196-.48-.541-.458-.903.022-.361.238-.683.564-.84l17-8.182c.274-.132.594-.132.867 0l17 8.182c.326.157.542.479.564.84.022.362-.153.707-.458.903l-17 10.909C32.376 43.856 32.188 43.909 32 43.909zM17.046 32.125L32 41.721l14.954-9.596L32 24.928 17.046 32.125z"></path><path fill="#8d6c9f" d="M32,43.909c-0.165,0-0.33-0.041-0.479-0.122C31.2,43.611,31,43.274,31,42.909V23.818 c0-0.344,0.177-0.664,0.468-0.847c0.291-0.183,0.654-0.205,0.966-0.054l17,8.182c0.326,0.157,0.542,0.479,0.564,0.84 c0.022,0.362-0.153,0.707-0.458,0.903l-17,10.909C32.376,43.856,32.188,43.909,32,43.909z M33,25.409v15.67l13.954-8.954 L33,25.409z"></path></g>\n' +
                    '                </svg>'
            let wallet_address = '<p class="my-auto ms-3 border border-1 border-gray rounded p-1">'+ data.address +'</p>'
            let block = '<div class="d-flex m-4">' + eth_svg + wallet_address +'</div>'
            wallets_block.append(block)
            wallets_count.text((Number(wallets_count.text()) + 1))
        },
        error: function (data){
            toastr.error(data.responseJSON.detail, 'Error')
        }
    })
}

//Modal close

// Імпорт гаманця
function import_wallet(){
    let private_key = wallet_import.val()
    let wallets_block = $('#block_wallets')
    $.ajax({
        method: "POST",
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json'
        },
        url: wallet_import_url,
        data: JSON.stringify({
            'private_key': private_key
        }),
        success: function (data){
            toastr.success('Гаманець успішно імпортовано', 'Success')
            let eth_svg = '<svg width="35px" height="35px" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n' +
                    '                    <path fill="#8d6c9f" d="M63 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C64 35.553 63.553 36 63 36zM58 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C59 35.553 58.553 36 58 36zM53 36c-.553 0-1-.447-1-1v-2c0-.553.447-1 1-1s1 .447 1 1v2C54 35.553 53.553 36 53 36zM11 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C12 35.553 11.552 36 11 36zM6 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C7 35.553 6.552 36 6 36zM1 36c-.552 0-1-.447-1-1v-2c0-.553.448-1 1-1s1 .447 1 1v2C2 35.553 1.552 36 1 36z"></path><path fill="#ace3ff" d="M15 32L32 2 49 32 32 42.909z"></path><path fill="#85cbf8" d="M32 2L49 32 32 42.909z"></path><path fill="#ace3ff" d="M15 37L32 47 49 37 32 62z"></path><path fill="#85cbf8" d="M32 47L49 37 32 62zM15 32L32 23.818 49 32 32 42.909z"></path><path fill="#7bbeeb" d="M32 23.818L49 32 32 42.909z"></path><g><path fill="#8d6c9f" d="M32,43.909c-0.188,0-0.375-0.053-0.54-0.158l-17-10.909c-0.447-0.287-0.592-0.873-0.33-1.335l17-30 c0.355-0.626,1.385-0.626,1.74,0l17,30c0.262,0.462,0.117,1.048-0.33,1.335l-17,10.909C32.376,43.856,32.188,43.909,32,43.909z M16.336,31.669L32,41.721l15.663-10.051L32,4.028L16.336,31.669z"></path><path fill="#8d6c9f" d="M32,43.909c-0.165,0-0.33-0.041-0.479-0.122C31.2,43.611,31,43.274,31,42.909V2 c0-0.454,0.306-0.851,0.745-0.967c0.441-0.116,0.901,0.079,1.125,0.474l17,30c0.262,0.462,0.117,1.048-0.33,1.335l-17,10.909 C32.376,43.856,32.188,43.909,32,43.909z M33,5.793v35.286l14.663-9.41L33,5.793z"></path><path fill="#8d6c9f" d="M32,63c-0.331,0-0.64-0.163-0.826-0.437l-17-24.909c-0.268-0.393-0.222-0.92,0.109-1.261 c0.332-0.34,0.857-0.4,1.257-0.145L32,46.812l16.46-10.562c0.399-0.257,0.926-0.196,1.257,0.145 c0.332,0.341,0.377,0.868,0.109,1.261l-17,24.909C32.64,62.837,32.33,63,32,63z M18.597,40.587L32,60.226l13.403-19.639 L32.54,48.842c-0.328,0.212-0.75,0.211-1.08,0L18.597,40.587z"></path><path fill="#8d6c9f" d="M32 63c-.098 0-.198-.015-.295-.045C31.286 62.826 31 62.438 31 62V48c0-.341.173-.657.46-.842l17-10.909c.399-.257.926-.196 1.257.145.332.341.377.868.109 1.261l-17 24.909C32.636 62.842 32.324 63 32 63zM33 48.547v10.214l12.403-18.174L33 48.547zM32 43.909c-.188 0-.375-.053-.54-.158l-17-10.909c-.305-.196-.48-.541-.458-.903.022-.361.238-.683.564-.84l17-8.182c.274-.132.594-.132.867 0l17 8.182c.326.157.542.479.564.84.022.362-.153.707-.458.903l-17 10.909C32.376 43.856 32.188 43.909 32 43.909zM17.046 32.125L32 41.721l14.954-9.596L32 24.928 17.046 32.125z"></path><path fill="#8d6c9f" d="M32,43.909c-0.165,0-0.33-0.041-0.479-0.122C31.2,43.611,31,43.274,31,42.909V23.818 c0-0.344,0.177-0.664,0.468-0.847c0.291-0.183,0.654-0.205,0.966-0.054l17,8.182c0.326,0.157,0.542,0.479,0.564,0.84 c0.022,0.362-0.153,0.707-0.458,0.903l-17,10.909C32.376,43.856,32.188,43.909,32,43.909z M33,25.409v15.67l13.954-8.954 L33,25.409z"></path></g>\n' +
                    '                </svg>'
            let wallet_address = '<p class="my-auto ms-3 border border-1 border-gray rounded p-1">'+ data.address +'</p>'
            let block = '<div class="d-flex m-4">' + eth_svg + wallet_address +'</div>'
            wallets_block.append(block)
            wallets_count.text((Number(wallets_count.text()) + 1))
        },
        error: function (data){
            toastr.error(data.responseJSON.detail, 'Error')
        }
    })
}