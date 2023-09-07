
const login_api_url = window.location.origin + "/api/v1/login/";

let regex = new RegExp('[a-z0-9]+@[a-z]+\.edu\.[a-z]{2,3}');

function validateEmail() {
  const input = document.querySelector("#email");
  const display = document.querySelector("#error-input-label");
  if (input.value.match(/(?:[a-z0-9+!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/gi)) {
    display.innerHTML = '';
  } else {
    display.innerHTML = input.value + ' is not a valid email';
  }
}

function login(){
    let email = $("#email")
    let password = $("#password")
    let error_label = $("#error-label")
    console.log(email.val(), password.val())

    if(!email.val() && !password.val()){
        error_label.text('Поле email та password не може бути пустим')
        return
    }
    else if(!email.val()){
        error_label.text('Поле email не може бути пустим')
        return;
    }

    else if(!password.val()){
        error_label.text("Поле password не може бути пустим")
        return;
    }

    $.ajax({
        method: 'post',
        dataType: 'json',
        headers: {
            "Content-Type": 'application/json',
        },
        url: login_api_url,
        data: JSON.stringify({
            'email': email.val(),
            'password': password.val()
        }),
        success: function (data){
            console.log("success", data.detail);
            if(data.detail == "Successfully authorization"){
                 location.reload()
            }
            },
        error: function (data){
            console.log('Error', data.responseJSON);
            error_label.text(data.responseJSON.detail)
        }
    })

}

// Логін при натисненні на кнопку
$("#login-button").click(function (){
    login()
})

// Логін при натиснені на enter
$(document).keydown(function(e) {
    if (e.keyCode === 13) {
      login()
    }
})




/*==================================================================
[ Focus input ]*/
$('.input100').each(function(){
    $(this).on('blur', function(){
        if($(this).val().trim() != "") {
            $(this).addClass('has-val');
        }
        else {
            $(this).removeClass('has-val');
        }
    })
})
  

