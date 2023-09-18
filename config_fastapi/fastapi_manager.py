import socketio

from config_fastapi import settings

# fastapi менеджер для відправлення emit клієнту
fastapi_mgr = socketio.AsyncAioPikaManager(url=settings.RABBITMQ_URI, write_only=True)