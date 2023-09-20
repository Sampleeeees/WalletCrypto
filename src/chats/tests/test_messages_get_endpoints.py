
async def test_create_message(client, user_auth):
     response = await client.post('/api/v1/message/', json={"content": "Hello world",
                                                            "image": "None"})

     assert response.status_code == 200

     data = response.json()
