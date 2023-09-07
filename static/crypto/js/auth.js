
const registration_api_url = window.location.origin + "/api/v1/registration/";

//=========// Validators //===========//
function validateEmail() {
  const input = document.querySelector("#email");
  const display = document.querySelector("#error-input-label");
  if (input.value.match(/(?:[a-z0-9+!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/gi)) {
    display.innerHTML = '';
  } else {
    display.innerHTML = input.value + ' is not a valid email';
  }
}

function validateUsername(event) {
            const inputElement = event.target;
            const inputValue = inputElement.value;

            // Перевіряємо, чи введено мінімум два слова
            const words = inputValue.split(' ');
            if (words.length < 2) {
                showError("Введіть мінімум два слова");
                return;
            }

            // Перевіряємо, чи кожне слово починається з великої літери
            for (const word of words) {
                if (!/^[A-ZА-ЯЁ][a-zа-яё]*$/.test(word)) {
                    showError("Кожне слово має починатися з великої літери");
                    return;
                }
            }

            // Все в порядку - видаляємо повідомлення про помилку
            clearError();
        }

        function showError(errorMessage) {
            const errorDiv = document.getElementById("error-username-label");
            errorDiv.textContent = errorMessage;
        }

        function clearError() {
            const errorDiv = document.getElementById("error-username-label");
            errorDiv.textContent = "";
        }

function registration(){
    let email = $("#email")
    let username = $('#username')
    let password = $('#pass')
    let repeat = $('#repeat_pass')

    let error = $('#error-label')

    if(!email.val() && !username.val() && !password.val() && !repeat.val()){
        error.text('Введіть всі поля ')
    }

    $.ajax({
        method: 'post',
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json'
        },
        url: registration_api_url,
        data: JSON.stringify({
            'email': email.val(),
            'username': username.val(),
            'password': password.val(),
            'repeat_password': repeat.val()
        }),
        success: function (data){
            console.log('Succes', data)
            if (data.message == "Акаунт успішно створений. Повідомлення про реєстрацію надіслано на пошту"){
                $('#registration-form')[0].style.display = 'none';
                $('#success-registration').text(data.message)
                $('#success-registration')[0].innerHTML = data.message + "<p style=\"font-size: 18px;\" class=\"m-22\"> Тепер вам необхідно увійти в свій аккаунт</p>\n" +
                    "                    <div class=\"container-login100-form-btn p-t-10\">\n" +
                    "\t\t\t\t\t\t<div class=\"wrap-login100-form-btn\">\n" +
                    "\t\t\t\t\t\t\t<div class=\"login100-form-bgbtn\"></div>\n" +
                    "\t\t\t\t\t\t\t<a class=\"login100-form-btn\" style=\"text-decoration: none;\" href=\"/login/\">\n" +
                    "\t\t\t\t\t\t\t\tLog in\n" +
                    "\t\t\t\t\t\t\t</a>\n" +
                    "\t\t\t\t\t\t</div>\n" +
                    "\t\t\t\t\t</div>"
                // error.text('Аккаунт успішно створено')
            }
        },
        error: function (data){
            console.log('Error', data)
            error.text(data)
            if (data.responseJSON.detail[0].msg == "value is not a valid email address: The email address is not valid. It must have exactly one @-sign."){
                error.text('Введіть вірний email')
            }else{
                error.text(data.responseJSON.detail)
            }
        }

    })

}


$("#button-registration").click(function (){
    registration()
})