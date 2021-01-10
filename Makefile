build:
	docker-compose down
	docker-compose build

run: build
	docker-compose up

down:
	docker-compose down

static-test:
	mypy --ignore-missing-imports ./**/*.py
	mypy --ignore-missing-imports ./**/**/*.py
	pylint ./**/*.py
	pylint ./**/**/*.py

unit-test:
	pytest

test: static-test unit-test
