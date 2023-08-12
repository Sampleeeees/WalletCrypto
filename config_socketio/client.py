import asyncio
import json
import socketio

infura_ws_url = 'wss://goerli.infura.io/ws/v3/0541bae5c97049309f8d2324648c2c2c'
sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('Connected to server')
    await sio.emit('subscribe', {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": ["newPendingTransactions"]
    })

@sio.event
async def disconnect():
    print('Disconnected from server')

@sio.event
async def message(data):
    try:
        response = json.loads(data)
        txHash = response['params']['result']
        print(f"Pending transaction: {txHash}")
        # Uncomment lines below if you want to monitor transactions to
        # a specific address
        # tx = web3.eth.get_transaction(txHash)
        # if tx.to == account:
        #     print("Pending transaction found with the following details:")
        #     print({
        #         "hash": txHash,
        #         "from": tx["from"],
        #         "value": web3.fromWei(tx["value"], 'ether')
        #     })
    except:
        pass

async def main():
    try:
        await sio.connect(infura_ws_url)
        await sio.wait()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
