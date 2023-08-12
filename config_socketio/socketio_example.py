import asyncio
import socketio

sio = socketio.AsyncClient(logger=True)

@sio.event
async def connect():
    print('connection established')

@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('wss://mainnet.infura.io/ws/v3/0541bae5c97049309f8d2324648c2c2c')
    await sio.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')
    subscribe = await sio.wait()
    print(subscribe)

if __name__ == '__main__':
    asyncio.run(main())