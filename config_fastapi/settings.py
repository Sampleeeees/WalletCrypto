import os
import environ

PROJECT_NAME = 'CryptoWallet' # Назва проекту
SERVER_HOST = os.environ.get("SERVER_HOST") # Хост сервера


SECRET_KEY = b"arubsyb872378t^*TG8y68&*&&*8y8yg9POB)*896ft7CR^56dfYUv" # Секретний ключ для fastapi

ALGORITHM = "HS256" # Алгоритм шифрування

env = environ.Env() # Підключення environment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Базова папка проекту

environ.Env.read_env(os.path.join(BASE_DIR, '.env')) # Місце знаходження env файлу


API_V1 = "/api/v1" # Префікс для api endpoints

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # Час дії access токену

# URL бази даних проекту
DATABASE_URI = f'postgresql+asyncpg://{env("POSTGRES_USER")}:' \
               f'{env("POSTGRES_PASSWORD")}@' \
               f'{env("POSTGRES_HOST")}:5432/' \
               f'{env("POSTGRES_DB")}'

# URL тестової бази даних
DATABASE_TEST_URI = f'postgresql+asyncpg://{env("POSTGRES_USER")}:' \
                    f'{env("POSTGRES_PASSWORD")}@' \
                    f'{env("POSTGRES_HOST")}:5432/' \
                    f'{env("POSTGRES_DB_TEST")}'

# Список модулів для wiring в container
APPS_SERVICE =[
    'config',
    'config_celery.tasks',
    'config_propan',
    'config_socketio',
    'src.core',
    'src.authentication',
    'src.chats',
    'src.delivery',
    'src.ibay',
    'src.parser',
    'src.users',
    'src.wallets',
]


EMAILS_FROM_NAME = "CryptoWallet" # Заголовок листа на пошту
EMAIL_TEMPLATES_DIR = 'src/email-templates/build' # місце темплейту листа

# Email
SMTP_TLS = env("SMTP_TLS")
SMTP_PORT = env("SMTP_PORT")
SMTP_HOST = env("SMTP_HOST")
SMTP_USER = env("SMTP_USER")
SMTP_PASSWORD = env("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = env("EMAILS_FROM_EMAIL")

# URL Rabbitmq
RABBITMQ_URI=f'amqp://{env("RABBITMQ_USER")}:' \
               f'{env("RABBITMQ_PASSWORD")}@' \
               f'{env("RABBITMQ_HOST")}:' \
               f'{env("RABBITMQ_PORT")}'

#INFURA
INFURA_URI = env("INFURA_URI")
INFURA_URI_HTTP = env("INFURA_URI_HTTP")

# Список origins
ORIGINS = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001"
]

# Bunny.net для збереження фото
BUNNY_API_KEY = env("BUNNY_API_KEY")
BUNNY_STORAGE_NAME = env("BUNNY_STORAGE_NAME")
BUNNY_STORAGE_REGION = env("BUNNY_STORAGE_REGION")

MORALIS_API_KEY = env("MORALIS_API_KEY")