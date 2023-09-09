import asyncio
import jwt
import socketio
from propan import RabbitBroker
from config_fastapi import settings
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.parser.service import ParserService
from src.users.service import UserService

mgr = socketio.AsyncAioPikaManager(settings.RABBITMQ_URI)
sio = socketio.AsyncServer(client_manager=mgr, async_mode='asgi', cors_allowed_origins="*", logger=True)

async def get_token(cookies: list):
    for cookie in cookies:
        if cookie.startswith('Authorization='):
            return cookie.split(' ')[1].strip('"')




@sio.event
@inject
async def connect(sid, environ, user_service: UserService = Provide[Container.user_service]):
    cookies = environ.get('HTTP_COOKIE').split('; ')
    token_encoded = await get_token(cookies=cookies)
    token = jwt.decode(jwt=token_encoded, key=settings.SECRET_KEY, algorithms=['HS256'])
    user_id = token.get('user_id')
    async with sio.session(sid) as session:
        session['user_id'] = user_id
        session['avatar'] = await user_service.get_image_by_user_id(user_id)


    print('New connect')
    print(user_id)
    # user = await user_service.get_user(user_id=user_id)
    # print('USer', user)



@sio.on('my_message')
async def my_message(sid, data):
    print('Your message:', data)
    async with sio.session(sid) as session:
        await sio.emit('message', {'message': data, 'user_id': session['user_id'], 'avatar': session['avatar']})


@sio.on('fastapi')
async def conn_fastapi(sid, data):
    print('HI FASTAPI')

# @sio.on('parsing')
# @inject
# async def parse_block(sid, data, parser_service: ParserService = Provide[Container.parser_service]):
#     while True:
#         block_number = await parser_service.get_latest_block()
#         if block_number is not None:
#             async with RabbitBroker(settings.RABBITMQ_URI) as broker:
#                 await broker.publish(message=block_number, queue='parser/parser_queue')



@sio.on('get_balance')
async def get_balance(sid, data):
    print(f'Balance {sid} and {data}')

@sio.on("disconnect")
async def disconnect(sid):
    print(f"Client {sid} disconnected")

