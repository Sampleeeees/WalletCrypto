from propan import RabbitBroker, PropanApp
from config_fastapi import settings

broker = RabbitBroker(settings.RABBITMQ_URI)

app = PropanApp(broker)

