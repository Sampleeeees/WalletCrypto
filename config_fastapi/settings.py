import os
import environ

PROJECT_NAME = 'CryptoWallet'
SERVER_HOST = os.environ.get("SERVER_HOST")


SECRET_KEY = b"arubsyb872378t^*TG8y68&*&&*8y8yg9POB)*896ft7CR^56dfYUv"

ALGORITHM = "HS256"

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


API_V1 = "/api/v1"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

DATABASE_URI = f'postgresql+asyncpg://{env("POSTGRES_USER")}:' \
               f'{env("POSTGRES_PASSWORD")}@' \
               f'{env("POSTGRES_HOST")}:5432/' \
               f'{env("POSTGRES_DB")}'

DATABASE_TEST_URI = f'postgresql+asyncpg://{env("POSTGRES_USER")}:' \
                    f'{env("POSTGRES_PASSWORD")}@' \
                    f'{env("POSTGRES_HOST")}:5432/' \
                    f'{env("POSTGRES_DB_TEST")}'

APPS_SERVICE = [
    "src.chats",
    "src.delivery",
    "src.ibay",
    "src.users",
    "src.wallets",
    'src.authentication'
]

EMAILS_FROM_NAME = "CryptoWallet"
EMAIL_TEMPLATES_DIR = 'src/email-templates/build'

# Email
SMTP_TLS = env("SMTP_TLS")
SMTP_PORT = env("SMTP_PORT")
SMTP_HOST = env("SMTP_HOST")
SMTP_USER = env("SMTP_USER")
SMTP_PASSWORD = env("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = env("EMAILS_FROM_EMAIL")

RABBITMQ_URI=f'ampq://{env("RABBITMQ_USER")}:' \
               f'{env("RABBITMQ_PASSWORD")}@' \
               f'{env("RABBITMQ_HOST")}:' \
               f'{env("RABBITMQ_PORT")}'

INFURA_URI = env("INFURA_URI")