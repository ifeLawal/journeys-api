lint:
	flake8 --ignore=E402,E501,E712,W503,E203
	black --check .

format:
	black --exclude=journeys/static --exclude=journeys/templates .
	isort --skip=journeys/static --skip=journeys/templates -rc .

shell:
	python manage.py shell