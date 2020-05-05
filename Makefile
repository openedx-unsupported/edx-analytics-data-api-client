ROOT = $(shell echo "$$PWD")
COVERAGE = $(ROOT)/build/coverage
PACKAGE = analyticsclient

validate: test.requirements test quality

test.requirements:
	pip install -q -r requirements/test.txt

test:
	pytest  $(PACKAGE)    --cov-branch \
		--cov-report=html:$(COVERAGE)/html/ \
		--cov-report=xml:$(COVERAGE)/coverage.xml \
		--cov=$(PACKAGE)

quality:
	pycodestyle --config=.pycodestyle $(PACKAGE)
	pylint --rcfile=.pylintrc $(PACKAGE)

	# Ignore module level docstrings and all test files
	# TODO: Quality changes to not ignore D203,D212,D401,D406,D407,D412,D413,D417
	pydocstyle --ignore=D100,D104,D203,D212,D401,D406,D407,D412,D413,D417 --match='(?!test).*py' $(PACKAGE)

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -q pip-tools
	pip-compile --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --upgrade -o requirements/tox.txt requirements/tox.in
	pip-compile --upgrade -o requirements/test.txt requirements/test.in
