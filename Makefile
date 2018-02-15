define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove all build, test, coverage and Python artifacts
	clean-build
	clean-pyc
	clean-test 

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with pylint
	pylint wallthick tests

test:
	py.test

coverage:
	clean
	py.test --cov-report term --cov-report html --cov=wallthick tests

release: ## package and upload a release
	clean 
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: ## builds source and wheel package
	clean 
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: ## install the package to the active Python's site-packages
	clean 
	python setup.py install
