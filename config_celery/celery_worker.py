from celery import Celery

from config_fastapi import settings

app = Celery('config_celery',
             broker=settings.RABBITMQ_URI,
             backend='rpc://',
             include=['config_celery.tasks'])

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TIMEZONE='Europe/Oslo',
    CELERY_ENABLE_UTC=True,
    CELERY_IGNORE_RESULT=True,
    CELERYBEAT_SCHEDULE={
        'random_delivery': {
            'task': 'config_celery.tasks.random_delivery',
            'schedule': 5.0,
        },
    }
)


