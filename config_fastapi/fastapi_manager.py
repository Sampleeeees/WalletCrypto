import socketio

from config_fastapi import settings

fastapi_mgr = socketio.AsyncAioPikaManager(settings.RABBITMQ_URI, write_only=True)