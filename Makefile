install:
	pip install -r requirements.txt

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	python manage.py test

shell:
	python manage.py shell

dbshell:
	python manage.py dbshell

backup:
	python manage.py dumpdata > db_backup.json
