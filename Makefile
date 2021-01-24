build:
	docker-compose down
	docker-compose build

run: build
	docker-compose up --scale consumer=3 --scale producer=2

down:
	docker-compose down

static-test:
	# MyPy unfortunately has to be run on each service separately,
	# otherwise it will complain about the duplicate modules (tests/__init__.py)
	mypy --ignore-missing-imports ./common/**/*.py
	mypy --ignore-missing-imports ./consumer/**/*.py
	mypy --ignore-missing-imports ./producer/**/*.py
	pylint ./**/*.py
	pylint ./**/**/*.py

unit-test:
	# Pytest needs to be called on each service separately,
	# otherwise it will complain about not being able to import
	# the test files. Interestingly, the last folder in alphabetical order
	# gets to fail, but calling from inside the folder has no issues.
	pytest ./consumer
	pytest ./producer

test: static-test unit-test
