run:
	python3 manage.py runserver

watch:
	python3 manage.py watch

release:
	python3 manage.py migrate --no-input
	python3 manage.py loadcontent content/posts/

upgrade-deps:
	pip-compile --upgrade --strip-extras && pip-compile --upgrade --strip-extras --extra dev -o requirements-dev.txt

pulldb:
	-docker start pdp-postgres
	-docker exec -e PGPASSWORD -it pdp-postgres dropdb postgres -Upostgres
	heroku pg:pull DATABASE_URL "postgresql://postgres@localhost:42069/postgres"
