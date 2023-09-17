import jwt
import socketio
from propan import RabbitBroker

from config_fastapi import settings
from dependency_injector.wiring import inject, Provide

from config_fastapi.fastapi_manager import fastapi_mgr
from src.chats.service import ChatService
from src.core.containers import Container
from src.core.storage_bunny import BunnyStorage
from src.parser.service import ParserService
from src.users.service import UserService

mgr = socketio.AsyncAioPikaManager(settings.RABBITMQ_URI)
sio = socketio.AsyncServer(client_manager=mgr, async_mode='asgi', cors_allowed_origins="*", logger=True)


online_users = {}

# Отримання з кукісів токен
async def get_token(cookies: list):
    for cookie in cookies:
        if cookie.startswith('access_token='):
            return cookie.split(' ')[1].strip('"')


@sio.event
@inject
async def connect(sid, environ, user_service: UserService = Provide[Container.user_service]):
    cookies = environ.get('HTTP_COOKIE').split('; ') # Отримання всіх кукісів
    token_encoded = await get_token(cookies=cookies) # Отримання токену з кукіс
    token = jwt.decode(jwt=token_encoded, key=settings.SECRET_KEY, algorithms=['HS256']) #Розкодування токену
    user_id = token.get('user_id') # Отримання user_id з токену
    user = await user_service.get_user(user_id) # Отримати повні дані профілю

    print()
    print(online_users)
    print()

    if online_users.get(user_id) is None:
        online_users[user_id] = {
            'user_id': user.id,
            'avatar': user.avatar,
            'username': user.username
        }
        await sio.emit('update_users_status', list(online_users.values()))

    room_name = f"user_{user_id}"
    sio.enter_room(sid, room_name)


    async with sio.session(sid) as session:
        session['user_id'] = user_id
        session['avatar'] = await user_service.get_image_by_user_id(user_id)
        session['username'] = user.username



    print('New connect')
    print(user_id)
    # user = await user_service.get_user(user_id=user_id)
    # print('USer', user)




@sio.on('my_message')
@inject
async def my_message(sid, data,
                     bunny_storage: BunnyStorage = Provide[Container.bunny_storage],
                     chat_service: ChatService = Provide[Container.chat_service]):
    print('Your message:', data)
    if data['image']:
        image_url = await bunny_storage.upload_image_to_bunny(data['image'])
    else:
        image_url = None
    async with sio.session(sid) as session:
        await chat_service.save_message(content=data['message'], image=image_url, user_id=session['user_id'])
        await sio.emit('message', {'message': data["message"], 'image': image_url, 'user_id': session['user_id'], 'avatar': session['avatar'], 'username': session['username']})



# @sio.on('parse_block')
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
    async with sio.session(sid) as session:
        user_id = session.get('user_id')
        if user_id is not None and user_id in online_users:
            del online_users[user_id]
            await sio.emit('update_users_status', list(online_users.values()))


