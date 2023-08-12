import asyncio
import json
from web3 import Web3
from websockets import connect

infura_ws_url = 'wss://goerli.infura.io/ws/v3/0541bae5c97049309f8d2324648c2c2c'
infura_http_url = 'https://goerli.infura.io/v3/0541bae5c97049309f8d2324648c2c2c'
web3 = Web3(Web3.HTTPProvider(infura_http_url))

# Used if you want to monitor ETH transactions to a specific address
account = '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD'

async def get_event():
    async with connect(infura_ws_url) as ws:
        await ws.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
        subscription_response = await ws.recv()
        print(subscription_response)

        while True:
            try:
                message = await ws.recv()
                response = json.loads(message)
                txHash = response['params']['result']
                tx = web3.eth.get_transaction(txHash)
                if tx.to == account:
                    print("Pending transaction found with the following details:")
                    print({
                        "hash": txHash,
                        "from": tx["from"],
                        "value": web3.from_wei(tx["value"], 'ether')
                    })
                pass
            except:
                pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(get_event())