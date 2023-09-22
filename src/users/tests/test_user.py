##############################################################################################
#                             GET /api/v1/users/                                             #
##############################################################################################

async def test_get_users_200(client, user_auth):
    response = await client.get("/api/v1/users/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3

##############################################################################################
#                             GET /api/v1/user/profile/                                      #
##############################################################################################

async def test_get_user_profile_200(client, user_auth):
    response = await client.get("/api/v1/user/profile/")

    assert response.status_code == 200

    data = response.json()

    assert data == {'id': 1, 'username': 'Test Test', 'email': 'user@test.com', 'avatar': None}

async def test_get_admin_profile_200(client, admin_auth):
    response = await client.get("/api/v1/user/profile/")

    assert response.status_code == 200

    data = response.json()

    assert data == {'id': 2, 'username': 'Admin Admin', 'email': 'admin@admin.com', 'avatar': None}

async def test_get_user_profile_error_auth(client):
    response = await client.get("/api/v1/user/profile/")

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}


##############################################################################################
#                             GET /api/v1/user/{user_id}                                     #
##############################################################################################

async def test_get_user_profile_by_id_1(client, user_auth):
    response = await client.get("/api/v1/user/1/")

    assert response.status_code == 200

    data = response.json()

    assert data == {'id': 1, 'username': 'Test Test', 'email': 'user@test.com', 'avatar': None}


async def test_get_user_profile_by_id_2(client, user_auth):
    response = await client.get("/api/v1/user/2/")

    assert response.status_code == 200

    data = response.json()

    assert data == {'id': 2, 'username': 'Admin Admin', 'email': 'admin@admin.com', 'avatar': None}


##############################################################################################
#                             PATCH /api/v1/user/                                            #
##############################################################################################

async def test_patch_user_error_auth(client, image_in_base64):
    response = await client.patch("/api/v1/user/", json={"username": "John Doe",
                                                         "avatar": image_in_base64,
                                                         "password": "Qwerty123",
                                                         "repeat": "Qwerty123"
                                                         })

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}


async def test_patch_only_user_avatar(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                         "avatar": None
                                                         })
    assert response.status_code == 200

    data = response.json()

    assert data == {'id': 1, 'username': 'Test Test', 'email': 'user@test.com', 'avatar': None}

async def test_patch_only_user_username(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                        "username": "John Doe"
                                                    })
    assert response.status_code == 200

    data = response.json()

    assert data == {'id': 1, 'username': 'John Doe', 'email': 'user@test.com', 'avatar': None}

async def test_patch_only_user_password(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                         "password": "Qwerty123",
                                                         "repeat": "Qwerty123"
                                                         })
    assert response.status_code == 200

    data = response.json()

    assert data == {'id': 1, 'username': 'John Doe', 'email': 'user@test.com', 'avatar': None}

async def test_patch_only_user_password_400(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                         "password": "Qwerty123",
                                                         "repeat": "Qwerty13"
                                                         })
    assert response.status_code == 400

    data = response.json()

    assert data == {'detail': 'Паролі не співпадають'}

async def test_patch_only_user_password_400_1(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                         "password": "qwerty123",
                                                         "repeat": "qwerty123"
                                                         })
    assert response.status_code == 400

    data = response.json()

    assert data == {'detail': 'Пароль повинен містити принаймні одну літеру в верхньому регістрі'}

async def test_patch_only_user_password_400_2(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                         "password": "Qwerty",
                                                         "repeat": "Qwerty"
                                                         })
    assert response.status_code == 400

    data = response.json()

    assert data == {'detail': 'Пароль повинен містити від 8 до 20 символів'}

async def test_patch_only_user_password_400_3(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                         "password": "Qwertyqwerty",
                                                         "repeat": "Qwertyqwerty"
                                                         })
    assert response.status_code == 400

    data = response.json()

    assert data == {'detail': 'Пароль повинен містити принаймні одну цифру'}

async def test_patch_only_user_password_400_4(client, user_auth):
    response = await client.patch("/api/v1/user/", json={
                                                         "password": "12345678",
                                                         "repeat": "12345678"
                                                         })
    assert response.status_code == 400

    data = response.json()

    assert data == {'detail': 'Пароль повинен містити принаймні одну літеру в нижньому регістрі'}


async def test_patch_all_user_data(client, user_auth, image_in_base64):
    response = await client.patch("/api/v1/user/", json={"username": "Dima Rubets",
                                                         "avatar": image_in_base64,
                                                         "password": "Qwerty123",
                                                         "repeat": "Qwerty123"
                                                         })

    assert response.status_code == 200

##############################################################################################
#                             DELETE /api/v1/user/{user_id}                                  #
##############################################################################################

async def test_delete_admin_user_by_id_400(client, admin_auth):
    response = await client.delete("/api/v1/user/100/")

    assert response.status_code == 404

    data = response.json()

    assert data == {'detail': "Такого користувача не знайдено"}

async def test_delete_user_user_by_id(client, user_auth):
    response = await client.delete("/api/v1/user/2/")

    assert response.status_code == 400

    data = response.json()

    assert data == {'detail': "Ви не маєте прав доступу"}

async def test_delete_user_error_auth(client):
    response = await client.delete("/api/v1/user/2/")

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}


async def test_delete_admin_user_by_id_200(client, admin_auth):
    response = await client.delete("/api/v1/user/2/")

    assert response.status_code == 200

    data = response.json()

    assert data == {'detail': "Користувача видалено"}



##############################################################################################
#                             DELETE /api/v1/user/                                           #
##############################################################################################

async def test_delete_self_user_error_auth(client):
    response = await client.delete("/api/v1/user/")

    assert response.status_code == 403

    data = response.json()

    assert data == {"detail": "Not authenticated"}


# async def test_delete_user(client, user_auth):
#     response = await client.delete("/api/v1/user/")
#
#     assert response.status_code == 200
#
#     data = response.json()
#
#     assert data == {"detail": "Користувача видалено"}








