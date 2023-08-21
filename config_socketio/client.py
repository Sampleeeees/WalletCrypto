import asyncio

import socketio


sio_client = socketio.AsyncClient()


@sio_client.event
async def connect():
    print('connection established')

@sio_client.event
async def my_message(data):
    print('message received with ', data)
    await sio_client.emit('my response', {'response': 'my response'})

@sio_client.on('event')
async def handler_envent(data):
    print('I read you data')

@sio_client.event
async def disconnect():
    print('disconnected from server')



async def main():
    await sio_client.connect('http://127.0.0.1:8001')
    # await sio_client.emit('event', 'Hello')
    await sio_client.emit('test', 'Woah')
    # await sio_client.emit('testing', 'Woah')

    #await sio_client.wait()

if __name__ == '__main__':
    asyncio.run(main())