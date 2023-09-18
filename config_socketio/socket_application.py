import socketio
from socketio import ASGIApp

from config_socketio.server import sio
from src.core.containers import Container

# функція для стоврення asgi app ля сокету та оголошення контейнеру для використання
def create_socket_app() -> ASGIApp:
    container=Container()

    socketio_app = socketio.ASGIApp(sio, socketio_path='socket.io')
    socketio_app.container = container
    return socketio_app


socketio_app = create_socket_app()