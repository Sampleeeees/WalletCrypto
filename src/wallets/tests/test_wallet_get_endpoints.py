##############################################################################################
#                             GET /api/v1/wallets/                                           #
##############################################################################################

async def test_get_all_wallets(client):
    response = await client.get("/api/v1/wallets/")

    assert response.status_code == 200

    data = response.json()

    assert [{'id': 1,
             'address': '0xF0265774D447A2329776EAf6a1A362D76ea17d34',
             'balance': 0.0,
             'private_key': '0x77642556********************************************************'}
            ] == data


##############################################################################################
#                             GET /api/v1/wallets/current-user/                              #
##############################################################################################

async def test_get_current_user_wallets(client, user_auth):
    response = await client.get("/api/v1/wallets/current-user/")

    assert response.status_code == 200

    data = response.json()

    assert [{'id': 1,
             'address': '0xF0265774D447A2329776EAf6a1A362D76ea17d34',
             'balance': 0.0,
             'private_key': '0x77642556********************************************************'}
            ] == data

async def test_get_current_user_wallet_error_auth(client):

    response = await client.get('/api/v1/wallets/current-user/')

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data

##############################################################################################
#                             GET /api/v1/wallet/transactions/{address}                      #
##############################################################################################


##############################################################################################
#                             GET /api/v1/wallet/transaction/{txn_hash}                      #
##############################################################################################


##############################################################################################
#                             GET /api/v1/wallet/{private_key                                #
##############################################################################################


