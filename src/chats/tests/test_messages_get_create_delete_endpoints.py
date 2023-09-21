##############################################################################################
#                             GET /api/v1/message/current-user/                              #
##############################################################################################
# Тест на отримання повідомлення авторизованого користувача
async def test_get_current_user_message(client, user_auth):

    response = await client.get('/api/v1/message/current-user/')

    assert response.status_code == 200

    data = response.json()

    assert [{'image': 'https://cryptowallet.b-cdn.net/basic.jpg',
             'id': 1,
             'date_send': '2023-09-16T13:53:57.004610',
             'user_id': 1,
             'content': 'Test message'}] == data

# Тест на отримання помилки про те що ми не авторизовані для отримання повідомлення
async def test_get_current_user_message_error_auth(client):
    response = await client.get("/api/v1/message/current-user/")

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data


##############################################################################################
#                             GET /api/v1/message/{msg_id}/                                  #
##############################################################################################

# Тест на отримання повідомлення по id для адміністратора
async def test_get_message_by_id_200(client, admin_auth):

    response = await client.get("/api/v1/message/1/")

    assert response.status_code == 200

    data = response.json()

    assert {'image': 'https://cryptowallet.b-cdn.net/basic.jpg',
             'id': 1,
             'date_send': '2023-09-16T13:53:57.004610',
             'user_id': 1,
             'content': 'Test message'} == data


# Тест на отримання помилки про те що повідомлення під таким id не знайдено
async def test_get_message_by_id_400(client, admin_auth):

    response = await client.get("/api/v1/message/1000/")

    assert response.status_code == 404

    data = response.json()

    assert {'detail': 'Повідомлення під таким id не знайдено'}


# Тест на отримання помилки що ви не є адміністратором
async def test_get_permission_message_by_id(client, user_auth):

    response = await client.get("/api/v1/message/1/")

    assert response.status_code == 400

    data = response.json()

    assert {"detail": "Ви не маєте прав доступу"} == data

# Тест на отримання помилки що ми не авторизовані
async def test_get_message_by_id_error_auth(client):

    response = await client.get("/api/v1/message/1/")

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data

##############################################################################################
#                             POST /api/v1/message/                                          #
##############################################################################################
# Тест для створення повідомлення
async def test_create_message(client, user_auth):
     response = await client.post('/api/v1/message/', json={"content": "Hello world",
                                                            "image": "None"})

     assert response.status_code == 200

# Тест на отримання помилки про те що не авторизований користувач створити повідомлення не зможе
async def test_create_message_error_auth(client):
    response = await client.post('/api/v1/message/', json={'content': 'Hello', 'image': None})

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data

##############################################################################################
#                             GET /api/v1/messages/                                          #
##############################################################################################

# Тест на отримання повідомлень з бд
async def test_get_messages(client, user_auth):

    response = await client.get("/api/v1/messages/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

# Тест на отримання помилки про те що не авторизований користувач не отримає всіх повідомлень
async def test_get_all_messages_error_auth(client):
    response = await client.get('/api/v1/messages/')

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data


##############################################################################################
#                             DELETE /api/v1/message/{msg_d}/                                #
##############################################################################################
# Тест на видалення повідомлення авторизованим користувачем яке існує
async def test_delete_message_by_id_200(client, user_auth):
    response = await client.delete("/api/v1/message/1/")

    assert response.status_code == 200

    data = response.json()

    assert {'detail': 'Повідомлення видалено'} == data


# Тест на видалення повідомлення авторизованим користувачем якого не існує
async def test_delete_message_by_id_400(client, user_auth):
    response = await client.delete("/api/v1/message/100/")

    assert response.status_code == 404

    data = response.json()

    assert {'detail': 'Повідомлення під таким id не знайдено'} == data

# Тест де отримаємо помилку про те що юзер не авторизований
async def test_delete_message_by_id_error_auth(client):

    response = await client.delete("/api/v1/message/1/")

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data
