##############################################################################################
#                             POST /api/v1/wallet/etherscan/{address}                        #
##############################################################################################

async def test_get_address_on_etherscan(client, user_auth):
    response = await client.post("/api/v1/wallet/etherscan/?address=0xaecd391a5f45f9dcf089f815b0547da82993c9ab")

    assert response.status_code == 200

    data = response.json()

    assert {"url": "https://etherscan.io/address/0xaecd391a5f45f9dcf089f815b0547da82993c9ab"} == data

async def test_get_address_on_etherscan_error_auth(client):
    response = await client.post("/api/v1/wallet/etherscan/?address=0xaecd391a5f45f9dcf089f815b0547da82993c9ab")

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data

##############################################################################################
#                             POST /api/v1/wallet/                                           #
##############################################################################################


##############################################################################################
#                             POST /api/v1/wallet/import/                                    #
##############################################################################################

# async def test_import_wallet(client, user_auth):
#     response = await client.post("/api/v1/wallet/import/", json={'private_key': "0x101c54e85776f8f5509d8b65cc5e762a18ad3f5f8a067811a486b5d595d8bc87"})
#
#     assert response.status_code == 200

async def test_import_wallet_error_auth(client):

    response = await client.post("/api/v1/wallet/import/", json={'private_key': "0x101c54e85776f8f5509d8b65cc5e762a18ad3f5f8a067811a486b5d595d8bc87"})

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data

##############################################################################################
#                             POST /api/v1/message/balance/{address}                         #
##############################################################################################

# async def test_get_balance(client, user_auth):
#
#     response = await client.post("/api/v1/wallet/balance/", json={"address": "0x07f4ac16AaAd7B561F0f9C1dE1CACAA18f2c61d9"})
#
#     assert response.status_code == 200

async def test_get_balance_error_auth(client):

    response = await client.post("/api/v1/wallet/balance/", json={'address': "0x07f4ac16AaAd7B561F0f9C1dE1CACAA18f2c61d9"})

    assert response.status_code == 403

    data = response.json()

    assert {'detail': 'Not authenticated'} == data
