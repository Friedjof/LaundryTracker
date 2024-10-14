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
