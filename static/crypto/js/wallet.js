const wallets_user_url = window.location.origin + "/api/v1/wallets/current-user/" // URL для отримання всіх гаманців юзера
const transaction_by_address_url = window.location.origin + "/api/v1/wallet/transactions/" // URL для отримання всіх транзакцій по адресу
const get_private_key_url = window.location.origin + "/api/v1/wallet/private_key/" // URL для отримання приватного ключа по адресу
const send_transaction_url = window.location.origin + "/api/v1/send-transaction/" // URL для відправки транзакції

const wallet_block = $('#wallets_user_block') // Блок в який вставляється всі гаманці юзера
const transaction_body = $('#transaction_body') // Блок в який записуються всі транзакції по адресі

const submit_button = $('#submit_send_transaction') // Кнопка яка відправляє транзакцію

//--//Завантаження всіх гаманців юзера//--//
$(document).ready(function (){
    render_wallets()
})

//--//Очиска вмісту модалки коли вона закривається//--//
$('#watchTransactionsModal').on('hidden.bs.modal', function () {
    $('#transaction_body').empty(); // Очистка вмісту таблиці
});



//--//Функція яка робить запит на отримання всіх гаманців юзера//--//
function render_wallets(){
    $.ajax({
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
        url: wallets_user_url,
        success: function (data){
            console.log('Wallets', data)
            for (let i in data){
                console.log(data[i])
                new_wallet_block(data[i])
            }
        }
    })
}

//--//Функція яка відмальовує блок з даними гаманця//--//
function new_wallet_block(wallet){
    let new_block = `
        <div class="col my-auto">
            <div class="row row-cols-2 m-3 border border-1 border-dark rounded">
                <div class="col-3 image my-auto text-center">`+ ethereum_image +`</div>
                <div class="col-9 pe-5">
                    <div class="d-flex ms-3 mt-4">
                        <h5 class="m-0 p-0">Address:</h5>
                        <a style="font-size: 12px;" id="wallet_address_${wallet.id}" class="ms-2 my-auto text-break" href="https://etherscan.io/address/${wallet.address}">${wallet.address}</a>
                    </div>
                    <div class="d-flex ms-3 mt-2">
                        <h5 class="m-0 p-0">Balance:</h5>
                        <p id="wallet_balance_${wallet.id}" class="ms-2 my-auto ">${(wallet.balance).toFixed(3)} ETH</p>
                    </div>
                    <div class="text-center mt-2 mb-3">
                        <div class="d-flex justify-content-center">
                            <button onclick="get_wallet_transaction(${wallet.id})" class="btn btn-primary waves-effect waves-light m-3 ">Watch transactions</button>
                            <button data-bs-toggle="modal" onclick="send_transaction(${wallet.id})" data-bs-target="#sendTransactionsModal" class="btn btn-success waves-effect waves-light m-3">Send Transaction</button>
                        </div>
                        <a href="https://sepoliafaucet.com/" class="col-11 btn btn-light waves-effect waves-light m-3">Get 0.5 ETH</a>
                    </div>
                </div>
            </div>`
    wallet_block.append(new_block)
}

//--// Валідація чи складається це поле лише з чисел//--//
function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

//--/ Отримання private key з запиту на endpoint /--//
async function get_private_key(address) {
    try {
        const response = await $.ajax({
            method: "GET",
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json'
            },
            data: { address: address },
            url: get_private_key_url,
        });

        console.log(response);
        return response; // Повертаємо значення приватного ключа
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

//--//Функція для відправки транзакції//--//
async function send_transaction(element){
    let wallet_address = $('#wallet_address_'+element)[0] //Отримання гаманця який відображеється в блоку
    let address_to_send = $('#address_to_send') // Отримання адресу на який потрібно відправити
    let value = $('#value_send') // Отримання скільки юзер хоче відправити
    let private_key = await get_private_key(wallet_address.text) // Отримання приватного ключа з запиту до нового api endpoint



    submit_button.off('click') //Видаляємо всю історію з минулого кліку на кнопку

    submit_button.on('click', function (){

        //--//Якщо поле з адресою пусте//--//
        if (!address_to_send.val()){
            toastr.error('Поле send to не можу бути пустим', 'Error')
            return;
        }

        //--//Якщо поле з value пусте//--//
        if (!value.val()){
            toastr.error('Поле value не можу бути пустим', 'Error')
            return;
        }

        //--//Чи містить поле value тільки цифри//--//
        if(!isNumber(value.val())){
            toastr.error('Невірний формат поля value', 'Error')
            return;
        }

        //--//Відправка POST запиту на бек для відправки транзакції//--//
        $.ajax({
            method: 'POST',
            dataType: 'json',
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({"from_send": wallet_address.text,
                "to_send": address_to_send.val().trim(),
                "value": value.val(),
                "private_key": private_key}),
            url: send_transaction_url,
            success: function (data){
                toastr.success('Транзакція пройшла успішно', 'Success')
                $('#sendTransactionsModal').modal('hide')
                $('#getTransactionsModal').modal('show')
                $('#txn_url')[0].href = `https://sepolia.etherscan.io/tx/${data}`
            },
            error: function (data){
                console.log(data)
                toastr.error(data.responseJSON.detail, 'Error')
            }

        })
    })
}

//--//Отримання всіх транзакцій по адресі//--//
function get_wallet_transaction(wallet_id){
    let address = $('#wallet_address_'+ wallet_id)[0]
    $.ajax({
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        url: transaction_by_address_url + address.text,
        success: function (data){
            console.log(data)
            let table_head = $('#transaction_head')
            if (data.length !== 0){
                $('#watchTransactionsModal').modal('show');
                for(let i = data.length - 1; i >= 0; i--){
                let txn = data[i]
                let new_transaction = `<tr>
                        <td title="${txn.hash}" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px;">
                          ${txn.hash}
                        </td>
                        <td style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px;">${txn.from_send}</td>
                        <td style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px;">${txn.to_send}</td>
                        <td style="${convert_class_font_size(txn.value)} white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px;">${convert_value(txn.value)} Eth</td>
                        <td style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100px;">${getElapsedTime(data[i].date_send)}</td>
                        <td style="font-size: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px;">${parseFloat(txn.txn_fee).toFixed(12)} Eth</td>
                        <td><span class="${get_status_option(txn.status)}">${txn.status}</span></td>
                      </tr>`
                transaction_body.append(new_transaction)
            }
            }else{
                toastr.warning('У цього гаманця немає жодної транзакції', 'Warning')
                console.log('Goodbye')
            }
        },
        error: function (data){
            console.log('Error', data)
        }
    })
}


//--//Функція для перетворення часу//--//
function getElapsedTime(dateString) {
  const currentDate = new Date();
  const sentDate = new Date(dateString);
  const timeDifference = currentDate - sentDate;
  const secondsDifference = Math.floor(timeDifference / 1000);

  if (secondsDifference < 60) {
    return `${secondsDifference} secs`;
  } else if (secondsDifference < 3600) {
    const minutes = Math.floor(secondsDifference / 60);
    return `${minutes} min`;
  } else if (secondsDifference < 86400) {
    const hours = Math.floor(secondsDifference / 3600);
    return `${hours} hours`;
  } else {
    const days = Math.floor(secondsDifference / 86400);
    return `${days} days`;
  }
}


function convert_value(value){
    let fixed_value = value.toFixed(12)
    let str_fixed_value = fixed_value.toString()
    if(str_fixed_value.startsWith("0.000000")){
        return fixed_value
    }else{
        return value
    }
}

function convert_class_font_size(value){
    let fixed_value = value.toFixed(12)
    let str_fixed_value = fixed_value.toString()
    if(str_fixed_value.startsWith("0.000000")) {
        return "font-size: 10px;"
    }
}


function get_status_option(status){
    if (status === 'Pending'){
        return 'badge bg-label-warning me-1'
    }else if(status === 'Success'){
        return 'badge bg-label-success me-1'
    }else if(status === 'Failed'){
        return 'badge bg-label-danger me-1'
    }
}
