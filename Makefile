
flower:
	fuser -k 5555/tcp
	celery -A config_celery.celery_worker.app flower


celery:
	celery -A config_celery.celery_app worker --loglevel=info


propan:
	propan run config_propan.propan_depends:app --reload


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
	uvicorn config_fastapi.main:app --reload --workers 2

asyncapi_docs:
	python src/chats/asyncapi/generator.py
	sudo ag asyncapi_docs.yaml @asyncapi/html-template -o static/async_api --force-write
	sudo mv static/async_api/index.html templates/chat/asyncapi
	sudo chmod 746 templates/chat/asyncapi/index.html
	python src/chats/asyncapi/html_fixer.py



