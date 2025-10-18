PORT ?= 8000
HOST ?= 127.0.0.1

.PHONY: build install migrate collectstatic render-start run start

build:
	./build.sh

install:
	uv pip install --system -e . && uv pip install --system rollbar

migrate:
	uv run python task_manager/manage.py migrate --noinput

collectstatic:
	uv run python task_manager/manage.py collectstatic --noinput

render-start:
	gunicorn task_manager.wsgi

# Run Django dev server locally
run:
	uv run python task_manager/manage.py runserver $(HOST):$(PORT)

# Alias for convenience
start: run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi
