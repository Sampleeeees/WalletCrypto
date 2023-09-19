
async def test_user_messages(client, user_auth):
    response = await client.post("/api/v1/message/current-user/")

    assert response.status_code == 200