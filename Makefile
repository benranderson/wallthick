init:
	pip install -r requirements/prod.txt

setup-dev:
	pip install -r requirements/dev.txt

test:
	py.test --cov-report term --cov-report html --cov=wallthick tests
