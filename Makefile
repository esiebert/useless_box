build:
	docker-compose down
	docker-compose build

run: build
	docker-compose up

down:
	docker-compose down

test:
	mypy --ignore-missing-imports .
	pylint */*.py
