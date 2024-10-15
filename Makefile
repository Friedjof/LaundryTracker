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

version:
	@echo "Creating tag $(v)"
	@git tag $(v)
	@echo "Pushing tag $(v)"
	@git push origin $(v)