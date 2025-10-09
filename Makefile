build:
	./build.sh

install:
	uv pip install --system -e .

migrate:
	uv run python task_manager/manage.py migrate --noinput

collectstatic:
	uv run python task_manager/manage.py collectstatic --noinput

render-start:
	gunicorn task_manager.wsgi
