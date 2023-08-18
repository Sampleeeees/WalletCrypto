flower:
	fuser -k 5555/tcp
	celery -A config_celery.celery_worker.app flower
celery:
	celery -A config_celery.celery_worker worker --loglevel=info
propan:
	propan run propan_app:app
socketio:
	fuser -k 8001/tcp
	uvicorn config_socketio.socket_application:socketio_app --reload --host 127.0.0.1 --port 8001
parser:
	python config_socketio/client.py
reset_rabbitmq:
	sudo rabbitmqctl stop_app
	sudo rabbitmqctl reset
	sudo rabbitmqctl start_app
fastapi:
	uvicorn config_fastapi.main:app --reload

