ROOT = $(shell echo "$$PWD")
COVERAGE = $(ROOT)/build/coverage
PACKAGE = analyticsclient

validate: test.requirements test quality

test.requirements:
	pip install -q -r requirements/test.txt

test:
	nosetests --with-coverage --cover-inclusive --cover-branches \
		--cover-html --cover-html-dir=$(COVERAGE)/html/ \
		--cover-xml --cover-xml-file=$(COVERAGE)/coverage.xml \
		--cover-package=$(PACKAGE) $(PACKAGE)/

quality:
	pep8 --config=.pep8 $(PACKAGE)
	pylint --rcfile=.pylintrc $(PACKAGE)

	# Ignore module level docstrings and all test files
	pep257 --ignore=D100,D104,D203 --match='(?!test).*py' $(PACKAGE)

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -q pip-tools
	pip-compile --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --upgrade -o requirements/test.txt requirements/test.in
