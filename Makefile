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

logs:
	@echo "Showing logs"
	@docker compose logs -f

restart: down up

demo: build up

clean: down
	@echo "Cleaning"
	@docker image prune -f

release:
	@echo "Creating release"
	ifndef v
		$(error v is not defined)
	endif
	@echo "Checkout main"
	@git checkout main
	@echo "Pulling main"
	@git pull origin main
	@echo "Create version.txt"
	echo $(v) > version.txt
	@echo "Committing version.txt"
	@git add version.txt
	@git commit -m "Bump version to $(v)"
	@echo "Pushing version.txt"
	@git push origin main
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

shell:
	@echo "Starting shell"
	@python manage.py shell

redis:
	@echo "Starting redis"
	docker compose -f redis.yml up -d

redis-down:
	@echo "Stopping redis"
	docker compose -f redis.yml down
