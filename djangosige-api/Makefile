COMMAND=python manage.py

r:
	${COMMAND} runserver

m:
	${COMMAND} migrate

mm:
	${COMMAND} makemigrations

t:
	pytest --cov --cov-report html

s:
	${COMMAND} shell
	python manage.py shell

dbs:
	${COMMAND} dbshell

bkp:
	${COMMAND} dumpdata > db_backup.json
