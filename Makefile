migrations:
	@echo "Creating migrations"
	@python manage.py makemigrations

migrate:
	@echo "Migrating"
	@python manage.py migrate

requirements:
	@echo "Installing requirements"
	rm -f requirements.txt
	@pip freeze > requirements.txt

build:
	@echo "Building"
	@docker compose build --no-cache

up:
	@echo "Starting"
	@docker compose up

down:
	@echo "Stopping"
	@docker compose down

demo: build up

clean: down
	@echo "Cleaning"
	@docker image prune -f

release:
	@echo "Creating tag $(v)"
	@git tag $(v)
	@echo "Pushing tag $(v)"
	@git push origin $(v)


version:
	@echo "Updating version.txt with latest tag"
	@TAG=$(shell git describe --tags --abbrev=0) && \
	echo "Latest tag: $$TAG" && \
	echo $$TAG > version.txt && \
	echo "version.txt updated with tag $$TAG"


admin:
	@echo "Creating superuser"
	@python manage.py createsuperuser
