PORT ?= 8000
HOST ?= 127.0.0.1

.PHONY: build install migrate collectstatic setup render-start run start

build:
	./build.sh

install:
	uv pip install --system -e . && uv pip install --system rollbar
	uv pip install coverage

migrate:
	uv run python manage.py migrate --noinput

collectstatic:
	uv run python manage.py collectstatic --noinput

# Prepare DB and static files for CI
setup: migrate collectstatic

render-start:
	gunicorn task_manager.wsgi

# Run Django dev server locally
run:
	uv run python manage.py runserver $(HOST):$(PORT)

# Alias for convenience
start: run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

lint:
	uv run ruff check task_manager

lint-fix:
	uv run ruff check task_manager --fix

test:
	uv run python manage.py test

test-coverage:
	uv run python -m coverage run manage.py test
	uv run python -m coverage xml -o coverage.xml
