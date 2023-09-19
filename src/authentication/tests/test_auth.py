# async def test_user_registration(client):
#     """Успішна реєстрація нового користувача"""
#     response = await client.post("/api/v1/registration/", json={"email": "rubetsdima100@gmail.com",
#                                                                 "password": "Qwerty123",
#                                                                 "repeat_password": "Qwerty123",
#                                                                 "username": "Rubets Dima"})
#     print(response.json())
#     assert response.status_code == 201
#     data = response.json()
#     assert data == {'message': 'Акаунт успішно створений. Повідомлення про реєстрацію надіслано на пошту',
#                     'detail': {'id': 1, 'username': 'Rubets Dima', 'email': 'rubetsdima100@gmail.com'}}
#
#
# async def test_fail_user_registration(client):
#     """Помилка: Така пошта вже зареєстрована в системі"""
#     response = await client.post("/api/v1/registration/", json={"email": "rubetsdima100@gmail.com",
#                                                                 "password": "Qwerty123",
#                                                                 "repeat_password": "Qwerty123",
#                                                                 "username": "Rubets Dima"})
#     print(response.json())
#     assert response.status_code == 400
#
# async def test_login_200(client):
#     """Успішна авторизація користувача"""
#     response = await client.post("/api/v1/login/", json={'email': "rubetsdima100@gmail.com",
#                                                          "password": "Qwerty123"})
#
#     assert response.status_code == 200
#     data = response.json()
#     assert data == {
#                       "detail": "Successfully authorization",
#                       "user_id": 1,
#                       "username": "Rubets Dima",
#                       "email": "rubetsdima100@gmail.com"
#                     }, 'Дані не пройшли авторизації '
#
# async def test_login_400(client):
#     """Помилка: Такого email не знайдено в системі"""
#     response = await client.post("/api/v1/login/", json={'email': "rubetsdima@gmail.com",
#                                                          "password": "Qwerty123"})
#
#     assert response.status_code == 400
#     print(response.json())
#     assert response.json() == {'detail': 'Такий email не існує в системі'}
#
#
# async def test_incorrect_email_registration(client):
#     """Перевірка введення невалідного email"""
#     response = await client.post("/api/v1/registration/", json={"email": "fail_type_email",
#                                                                 "password": "Qwerty123",
#                                                                 "repeat_password": "Qwerty123",
#                                                                 "username": "John Doe"
#                                                                 })
#     assert response.status_code == 422
#
# async def test_incorrect_password_length_registration(client):
#     """Перевірка невірної довжини паролю (8 <= x <+ 20)"""
#
#     # Пароль менше 8 символів
#     response_until_8 = await client.post("/api/v1/registration/", json={"email": "user_test@example.com",
#                                                                 "password": "qq",
#                                                                 "repeat_password": "qq",
#                                                                 "username": "John Doe"
#                                                                 })
#     assert response_until_8.status_code == 400
#     assert response_until_8.json() == {"detail": "Пароль повинен містити від 8 до 20 символів"}
#
#     # Пароль більше 20 символів
#     response_over_20 = await client.post("/api/v1/registration/", json={"email": "user_test@example.com",
#                                                                         "password": "qwertyuiop12345678901",
#                                                                         "repeat_password": "qwertyuiop12345678901",
#                                                                         "username": "John Doe"
#                                                                         })
#     assert response_over_20.status_code == 400
#     assert response_over_20.json() == {"detail": "Пароль повинен містити від 8 до 20 символів"}
#
#
# async def test_incorrect_password_digit_registration(client):
#     """Перевірка що у пароля немає цифри"""
#
#     response = await client.post("/api/v1/registration/", json={"email": "user_test@example.com",
#                                                                         "password": "Qwertyasd",
#                                                                         "repeat_password": "Qwertyasd",
#                                                                         "username": "John Doe"
#                                                                         })
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Пароль повинен містити принаймні одну цифру"}
#
# async def test_incorrect_password_lower_registration(client):
#     """Перевіка щоб у пароля була мінімум 1 літера в нижньому регістрі"""
#
#     response = await client.post("/api/v1/registration/", json={"email": "user_test@example.com",
#                                                                 "password": "QWERTY123",
#                                                                 "repeat_password": "QWERTY123",
#                                                                 "username": "John Doe"
#                                                                 })
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Пароль повинен містити принаймні одну літеру в нижньому регістрі"}
#
# async def test_incorrect_password_upper_registration(client):
#     """Перевірка щоб у пароля була мінімум 1 літера у верхньому регістрі"""
#
#     response = await client.post("/api/v1/registration/", json={"email": "user_test@example.com",
#                                                                 "password": "qwerty123",
#                                                                 "repeat_password": "qwerty123",
#                                                                 "username": "John Doe"
#                                                                 })
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Пароль повинен містити принаймні одну літеру в верхньому регістрі"}
#
#
# async def test_incorrect_password_check_registartion(client):
#     """Перевірка на співпадіння паролів"""
#
#     response = await client.post("/api/v1/registration/", json={"email": "user_test@example.com",
#                                                                 "password": "Qwerty123",
#                                                                 "repeat_password": "Qwerty1234",
#                                                                 "username": "John Doe"
#                                                                 })
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Паролі не співпадають"}
#
#
# async def test_password_login_400(client):
#     """Перевірка чи увів вірний пароль від акаунту"""
#
#     response = await client.post("/api/v1/login/", json={"email": "rubetsdima100@gmail.com", "password": "Qwerty1234"})
#
#     assert response.status_code == 400
#     assert response.json() == {'detail': 'Не вірний пароль'}
#
