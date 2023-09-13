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
                let new_option = new Option(`${wallet.address} (${wallet.balance} ETH)`, wallet.id, false, false);
                select_user_wallets.append(new_option).trigger('change');

            }
        }
    })
}

function get_product_image(image){
    let product_image = image.files[0];
    let name_product_image = $('#name_image_product')
    if (product_image.type !== 'image/jpeg' && product_image.type !== 'image/png' && product_image.type !== 'image/jpg') {
        toastr.error('Дозволені лише файли типу "jpeg", "png" та "jpg"')
    }else {
        console.log(product_image)
        name_product_image.text(product_image.name)
    }}

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

async function create_product(){
    let product_image = $('#product_image')[0].files[0]
    let product_name = $('#name_product').val()
    let wallet_id = select_user_wallets.val()
    let price = $("#price_product").val()
    let validate_price_product = function(price) {
      return /^(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/.test(price);
    }


    //--//Якщо всі поля пусті//--//
    if(!product_name && !wallet_id && product_image === undefined && !validate_price_product(price)){
        toastr.error('Заповніть поля даними', 'Error')
        return;
    }

    //--//Якщо поле ціни не пройшло валідацію//--//
    if(!validate_price_product(price)){
        toastr.error('Невірний формат ціни', 'Error')
        return;
    }

    //--//Якщо поле назви пусте//--//
    if(!product_name){
        toastr.error('Напишіть назву продукту', 'Error')
        return;
    }

    //--//Якщ не обрано гаманець//--//
    if(!wallet_id){
        toastr.error('Оберіть гаманець', 'Error')
        return;
    }

    //--//Якщо не завантажена картинка//--//
    if (product_image === undefined){
        toastr.error('Додайте якусь картинку', 'Error')
        return;
    }

    let imageBase64 = await imageInBase64(product_image) //Отримання картинки в base64 форматі

    console.log(imageBase64)


    // $.ajax({
    //     method: "POST",
    //     dataType: 'json',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     data: {"name": product_name,
    //            "image": imageBase64,
    //            "price": price,
    //            "wallet_id": wallet_id},
    //     success: function (data){
    //         toastr.success('Продукт успішно створено', 'Success')
    //     },
    //     error: function (data){
    //         toastr.error(data.responseJSON.detail, 'Error')
    //     }
    // })


}

function render_product(product){
    let new_product = `<div class="col my-auto">
                <div class="row row-cols-2 m-3 border border-1 border-dark rounded">
                    <div class="col-3 image my-auto text-center">
                        <img height="auto" width="50px;" src="${product.image}" alt="">
                    </div>
                    <div class="col-9 pe-5">
                        <div class="d-flex ms-3 mt-4">
                            <h5 class="m-0 p-0">Title:</h5>
                            <p id="product_${product.id}" class="ms-2 my-auto text-break">${product.name}</p>
                        </div>
                        <div class="d-flex ms-3 mt-2">
                            <h5 class="m-0 p-0">Address:</h5>
                            <a style="font-size: 12px;" class="ms-2 my-auto text-break" href="https://etherscan.io/address/${product.wallet.address}">${product.wallet.address}</a>
                        </div>
                        <div class="d-flex ms-3 mt-2">
                            <h5 class="m-0 p-0">Price:</h5>
                            <p class="ms-2 my-auto ">${product.price}</p>
                        </div>
                        <div class="text-start mt-2 mb-3">
                            <button class="btn btn-primary waves-effect waves-light m-3 ">Buy product</button>
                        </div>
                    </div>
                </div>`
    product_user_block.append(new_product)
}

// function show_preview_chat_image(image){
//     let modal_image = image;
//     if (modal_image){
//         const reader = new FileReader();
//
//         reader.onload = function (event) {
//             const modal_image_result = event.target.result;
//             // Assuming check_image is an <img> element
//             $('#check_image').attr('src', modal_image_result);
//         };
//
//         reader.readAsDataURL(modal_image);
//     }
// }


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
            for(let i in data){
                let product = data[i]
                render_product(product)
            }
        }
    })
}


//--//Function for create product//--//
