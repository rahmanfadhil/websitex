clean:
	rm -rf static/dist

run:
	docker-compose up -d

stop:
	docker-compose down

test:
	docker-compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test web pytest --pdbcls=IPython.terminal.debugger:TerminalPdb

test-coverage:
	docker-compose run --rm -e DJANGO_SETTINGS_MODULE=config.settings.test web pytest --cov=apps/ --cov-report=html

shell:
	docker-compose run --rm web python manage.py shell -i ipython

makemigrations:
	docker-compose run --rm web python manage.py makemigrations

migrate:
	docker-compose run --rm web python manage.py migrate

createsuperuser:
	docker-compose run --rm web python manage.py createsuperuser

push:
	docker build -t rahmanfadhil/websitex:$(version) --target production .
	docker push rahmanfadhil/websitex:$(version)

.PHONY: clean run stop test test-debug shell makemigrations migrate createsuperuser
