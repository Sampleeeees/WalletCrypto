const logout_user_user = window.location.origin + "/api/v1/logout/"
const user_basic_profile_url = window.location.origin + "/api/v1/user/profile/"

const socket = io('ws://127.0.0.1:8000', {path: '/ws/socket.io'});

const header_basic_avatar = $("#header_avatar")
const basic_dropdown_image = $('#dropdown_image')
const user_basic_nickname = $('#user_basic_username')
const user_id = $('#user_id')

let eventSent = false;




socket.on('connect', () => {
    console.log('connected')
})

socket.on('send_txn', (data) => {
    console.log(data)
    let wallet = $('#wallet_balance_'+ data.wallet_id)
    let wallet_balance = wallet.text()
    console.log("Balance:",wallet_balance)
    console.log(wallet, wallet_balance)
    toastr.info(`${data.message}.<br> <p style="font-size: 12px;">${data.address}</p> <br> <a style="font-size: 12px;" href="https://sepolia.etherscan.io/tx/${data.txn_hash}">Посилання на транзакцію</a>`)
    let new_balance = parseFloat(wallet_balance) - data.value
    wallet.text(new_balance.toFixed(3))
})

socket.on('get_txn', (data) => {
    console.log('GET', data)
    let wallet = $('#wallet_balance_'+ data.wallet_id)
    let wallet_balance = wallet.text()
    toastr.info(`${data.message}.<br> <p style="font-size: 12px;">${data.address}</p> <br> <a style="font-size: 12px;" href="https://sepolia.etherscan.io/tx/${data.txn_hash}">Посилання на транзакцію</a>`)
    let new_balance = parseFloat(wallet_balance) + data.value
    wallet.text(new_balance.toFixed(3))
})

socket.on("update_wallet_balance", (data) => {
    let wallet = $("#wallet_balance_" + data.wallet_id)
    wallet.text((data.balance).toFixed(3))
})

socket.on('disconnect', () => {
    console.log('disconnect')
})

window.addEventListener('load', () => {
    const loader = document.querySelector('.loader');

    loader.classList.add('loader-hidden');

    loader.addEventListener('transitionend', () => {
        loader.remove()
    })
})

$(window).on('load', function (){
    toastr.options = {
      "closeButton": true,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-bottom-right",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut"
    }})

$(document).ready(function (){
    load_basic_user_profile()
})

function load_basic_user_profile(){
    $.ajax({
        method: 'GET',
        headers: {
            "Content-Type": 'application/json'
        },
        url: user_basic_profile_url,
        success: function (data){
            console.log(data)
            user_basic_nickname.text(data.username)
            user_id.text(data.id)
            if(data.avatar){
                basic_dropdown_image.attr('src', data.avatar)
                header_basic_avatar.attr('src', data.avatar)
            }
        }
    })
}



function logout_user(){
    $.ajax({
        method: "POST",
        url: logout_user_user,
        success: function (){
            window.location.reload()
        }
    })
}