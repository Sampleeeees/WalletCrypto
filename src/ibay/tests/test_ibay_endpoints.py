##############################################################################################
#                             POST /api/v1/product/                                          #
##############################################################################################

async def test_create_product_200(client, user_auth, image_in_base64):
     response = await client.post("/api/v1/product/", json={"name": "Product 1",
                                                            "price": 1,
                                                            "image": image_in_base64,
                                                            "wallet_id": 1})

     assert response.status_code == 200

async def test_create_product_400(client, user_auth):
    response = await client.post("/api/v1/product/", json={"name": "Product 1",
                                                            "price": 1,
                                                            "image": "",
                                                            "wallet_id": 1})

    assert response.status_code == 400

async def test_create_product_error_auth(client, image_in_base64):
    response = await client.post("/api/v1/product/", json={"name": "Product1",
                                                           "price": 1,
                                                           "image": image_in_base64,
                                                           "wallet_id": 1})

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}

##############################################################################################
#                             POST /api/v1/buy-product/                             #
##############################################################################################

async def test_buy_product_error_buy(client, user_auth):
    response = await client.post("/api/v1/buy-product/", json={"product_id": 1,
                                                               "wallet_id": 1})

    assert response.status_code == 400

    data = response.json()

    assert data == {'detail': 'Ви не можете купити товар у самого себе )'}

async def test_buy_product_error_product_id(client, user_auth):
    response = await client.post("/api/v1/buy-product/", json={"product_id": 100,
                                                               "wallet_id": 1})

    assert response.status_code == 400

    data = response.json()

    assert data == {"detail": "Товару під таким id не знайдено"}

async def test_buy_product_error_wallet_id(client, user_auth):
    response = await client.post("/api/v1/buy-product/", json={"product_id": 1,
                                                               "wallet_id": 100})

    assert response.status_code == 400

    data= response.json()

    assert data == {"detail": "Такого гаманця у вас немає"}


async def test_buy_product_error_auth(client):
    response = await client.post("/api/v1/buy-product/", json={"product_id": 1,
                                                               "wallet_id": 1})

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}


##############################################################################################
#                             GET /api/v1/products/                                         #
##############################################################################################

async def test_get_products_200(client, user_auth):
    response = await client.get("/api/v1/products/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

async def test_get_products_error_auth(client):
    response = await client.get("/api/v1/products/")

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}


##############################################################################################
#                             GET /api/v1/product-ordered/                                   #
##############################################################################################

async def test_get_order_user_200(client, user_auth):
    response = await client.get("/api/v1/product-ordered/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 0

async def test_get_order_user_error_auth(client):
    response = await client.get("/api/v1/product-ordered/")

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}