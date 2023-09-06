
async def test_send_mesage(client, login_user):
    response = await client.post('/api/v1/message/', json={'content': 'Hello',
                                                    "image": None})
    assert response.status_code == 200


async def test_get_message_current_user(client, login_user):
    response = await client.get('api/v1/message/current-user/')

    assert response.status_code == 200
    print(response.json())