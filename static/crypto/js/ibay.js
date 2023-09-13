const product_api_url = window.location.origin + "/api/v1/products/"
const wallets_user_url = window.location.origin + "/api/v1/wallets/current-user/" // URL для отримання всіх гаманців юзера



const product_user_block = $('#product_user_block')
const order_user_block = $('#order_user_block')

const select_user_wallets = $('#modalEditUserWallets')



$(document).ready(() => {
    render_products()
    render_wallets()
})

select_user_wallets.select2({
    placeholder: 'Select your wallet',
    dropdownParent: $('#createProductModal'),
    minimumResultsForSearch: -1,
    width: '100%'
})

function render_wallets(){
    $.ajax({
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
        url: wallets_user_url,
        success: function (data){
            console.log('Wallets', data)
            for(let i in data){
                let wallet = data[i]
                let new_option = new Option(wallet.address, wallet.id, false, false);
                select_user_wallets.append(new_option).trigger('change');
            }
        }
    })
}


// $('#createProductModal').on('shown.bs.modal', function() {
//     console.log('Hello select2')
//     console.log(this)
//   $(this).find('select').each(function() {
//     var dropdownParent = $('#createProductModal');
//     if ($(this).parents('.modal.in:first').length !== 0)
//       dropdownParent = $(this).parents('.modal.in:first');
//     $(this).select2({
//       dropdownParent: dropdownParent,
//       minimumResultsForSearch: -1
//       // ...
//     });
//   });
// });


function render_products(){
    $.ajax({
        method: 'GET',
        url: product_api_url,
        success: function (data){
            console.log(data)
        }
    })
}


//--//Function for create product//--//
