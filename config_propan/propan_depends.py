import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_propan.propan_app import app
from src.core.containers import Container

# функція для створення propan з container для використання  dependency_injector
def create_propan():
    container = Container()
    propan_app = app
    propan_app.container = container
    return propan_app

app = create_propan()