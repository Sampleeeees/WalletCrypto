const wallets_user_url = window.location.origin + "/api/v1/wallets/current-user/"
const transaction_by_address_url = window.location.origin + "/api/v1/wallet/transactions/"

const wallet_block = $('#wallets_user_block')
const transaction_body = $('#transaction_body')


$(document).ready(function (){
    render_wallets()
})

$('#watchTransactionsModal').on('hidden.bs.modal', function () {
    // Очистіть вміст таблиці
    $('#transaction_body').empty();
});

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
                        <p class="ms-2 my-auto ">${wallet.balance}</p>
                    </div>
                    <div class="text-center mt-2 mb-3">
                        <div class="d-flex justify-content-center">
                            <button onclick="get_wallet_transaction(${wallet.id})" data-bs-toggle="modal" data-bs-target="#watchTransactionsModal" class="btn btn-primary waves-effect waves-light m-3 ">Watch transactions</button>
                            <button class="btn btn-success waves-effect waves-light m-3">Send Transaction</button>
                        </div>
                        <button class="col-11 btn btn-light waves-effect waves-light m-3">Get 0.5 ETH</button>
                    </div>
                </div>
            </div>`
    wallet_block.append(new_block)
}


function get_wallet_transaction(wallet_id){
    let address = $('#wallet_address_'+ wallet_id)[0]
    console.log(address.text)
    $.ajax({
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        url: transaction_by_address_url + address.text,
        success: function (data){
            console.log(data)
            for(let i in data){
                let txn = data[i]
                let new_transaction = `<tr>
                        <td>
                          <p>${txn.hash}</p>
                        </td>
                        <td>${txn.from_send}</td>
                        <td>${txn.to_send}</td>
                        <td>${txn.value} Eth</td>
                        <td>6 secs</td>
                        <td>${txn.txn_fee} Eth</td>
                        <td><span class="badge bg-label-success me-1">${txn.status}</span></td>
                      </tr>`
                transaction_body.append(new_transaction)
            }
        },
        error: function (data){
            console.log('Error', data)
        }
    })
}


function clear_modal(){
    transaction_body.remove()
}