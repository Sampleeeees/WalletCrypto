const product_api_url = window.location.origin + "/api/v1/products/" // URL для отримання всіх продуктів
const wallets_user_url = window.location.origin + "/api/v1/wallets/current-user/" // URL для отримання всіх гаманців юзера
const create_product_url = window.location.origin + "/api/v1/product/" // URL для створення продукту
const orders_user_url = window.location.origin + "/api/v1/product-ordered/" //URL для всіх замовлень юзера
const buy_product_url = window.location.origin + "/api/v1/buy-product/" //URL для купівлі замовлення


const product_user_block = $('#product_user_block') // Блок з продуктами
const order_user_block = $('#order_user_block') // Блок з замовленнями користувача

const select_user_wallets = $('#modalEditUserWallets') //


//--//Виконання функцій коли викликана сторінка//--//
$(window).on('load', function (){
    render_products() // Відображення продуктів
    render_wallets() // Отримання гаманців юзера
    render_my_orders() // Відображення замовлень юзера
})

//--//Встановлюємо для поля select налаштування//--//
select_user_wallets.select2({
    placeholder: 'Select your wallet',
    dropdownParent: $('#createProductModal'),
    minimumResultsForSearch: -1,
    width: '100%'
})

//--//Запит для отримання гаманців юзера для відображення їх в списку select при створенні продукту//--//
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
                let new_option = new Option(`${wallet.address} (${wallet.balance} ETH)`, wallet.id, false, false); // Новий option з даними гамнця
                select_user_wallets.append(new_option).trigger('change'); // Додаємо option в select

            }
        }
    })
}

//--//Запит на отримання всіх замовлень користувача//--//
function render_my_orders(){
    $.ajax({
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        },
        url: orders_user_url,
        success: function (data){
            console.log('Order', data)
            for(let i in data){
                let order = data[i]
                render_order(order) // Відображення замовлення на фронт
            }
        },
        error: function (data){
            console.log('Error order', data)
        }
    })
}

//--//Функція для завантаження фото продукту яка перевіряє тип файлу//--//
function get_product_image(image){
    let product_image = image.files[0];
    let name_product_image = $('#name_image_product')
    if (product_image.type !== 'image/jpeg' && product_image.type !== 'image/png' && product_image.type !== 'image/jpg') {
        toastr.error('Дозволені лише файли типу "jpeg", "png" та "jpg"')
    }else {
        console.log(product_image)
        name_product_image.text(product_image.name)
    }}

//--//Функція для перетворення фото в base64 формат//--//
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

function buy_product(data){
    console.log(data)
}


//--//Функція для стоврення продукту з валідацією полів//--//
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
    console.log(product_name, price, wallet_id)


    $.ajax({
        method: "POST",
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json'
        },
        data: JSON.stringify({"name": product_name,
               "image": imageBase64,
               "price": price,
               "wallet_id": wallet_id}),
        url: create_product_url,
        success: function (data){
            render_product(data) // Відображення продукту на фронт
            $('#createProductModal').modal('hide') // Закриваємо автоматично модальне вікно стоврення продукту
            toastr.success('Продукт успішно створено', 'Success')
        },
        error: function (data){
            toastr.error(data.responseJSON.detail, 'Error')
        }
    })


}


//--//Відображення продукту на фронт//--//
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
                            <button onclick="buy_product(${product.id})" class="btn btn-primary waves-effect waves-light m-3 ">Buy product</button>
                        </div>
                    </div>
                </div>`
    product_user_block.append(new_product)
}

//--//Відображення замовлення на фронт//--//
function render_order(order){
    let date = new Date(order.date_send).toLocaleDateString(['en-US'], {day: 'numeric', month: 'numeric', year: "2-digit"}) + ', ' +new Date(order.date_send).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
    let date_buy = date.replace(/\//g, '.');
    let turning = function (turn){
        if (turn == null){
            return ''
        }else{
            return turn
        }
    }
    let new_order = `<div class="col my-auto">
            <div id="order_${order.id}" class="row row-cols-2 m-3 border border-1 border-dark rounded">
                <div class="col-3 image my-auto text-center">
                    <img height="120px" width="50px;" src="${order.product.image}" alt="">
                </div>
                <div class="col-9 pe-5">
                    <div class="d-flex ms-3 mt-4">
                        <h5 class="m-0 p-0">Title:</h5>
                        <p id="title_product" class="ms-2 my-auto">${order.product.name}</p>
                    </div>
                    <div class="d-flex ms-3 mt-2">
                        <h5 class="m-0 p-0">Address:</h5>
                        <a style="font-size: 10px;" href="https://sepolia.etherscan.io/tx/${order.transaction.hash}" class="ms-2 my-auto text-break">${order.transaction.hash}</a>
                    </div>
                    <div class="d-flex ms-3 mt-2">
                        <h5 class="m-0 p-0">Price:</h5>
                        <p class="ms-2 my-auto ">${order.product.price}</p>
                    </div>
                    <div class="d-flex ms-3 mt-2">
                        <h5 class="m-0 p-0">Data:</h5>
                        <p class="ms-2 my-auto">${date_buy}</p>
                    </div>
                    <div class="d-flex ms-3 mt-2">
                        <h5 class="m-0 p-0">Status:</h5>
                        <span class="${get_status_option(order.status)}">${order.status}</span>
                    </div>           
                   <div class="d-flex ms-3 mt-2 mb-2">
                        <h5 class="m-0 p-0">Turning:</h5>
                        <p class="ms-2 my-auto">${turning(order.turning)}</p>
                    </div>

                </div>
            </div>`
    order_user_block.append(new_order)
}


//--//Запит на отримання всіх продуктів та відображення на фронт//--//
function render_products(){
    $.ajax({
        method: 'GET',
        url: product_api_url,
        success: function (data){
            console.log(data)
            for(let i in data){
                let product = data[i]
                render_product(product) // Відображення продукту на фронт
            }
        }
    })
}

//--//Функція для переведення статусу замовлення у певному формат//--//
function get_status_option(status){
    if (status === 'New'){
        return 'badge bg-label-primary ms-1'
    }else if(status === 'Finish'){
        return 'badge bg-label-success ms-1'
    }else if(status === 'Failed'){
        return 'badge bg-label-danger ms-1'
    }else if (status === 'Turning'){
        return 'badge bg-label-danger ms-1'
    }else if(status === 'Delivery'){
        return 'badge bg-label-warning ms-1'
    }
}

