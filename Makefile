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

COMMON_CONSTRAINTS_TXT=requirements/common_constraints.txt
.PHONY: $(COMMON_CONSTRAINTS_TXT)
$(COMMON_CONSTRAINTS_TXT):
	wget -O "$(@)" https://raw.githubusercontent.com/edx/edx-lint/master/edx_lint/files/common_constraints.txt || touch "$(@)"

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: $(COMMON_CONSTRAINTS_TXT)
	## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -qr requirements/pip-tools.txt
	pip-compile --allow-unsafe --rebuild --upgrade -o requirements/pip.txt requirements/pip.in
	pip-compile --allow-unsafe --upgrade -o requirements/pip-tools.txt requirements/pip-tools.in
	pip install -qr requirements/pip.txt
	pip install -qr requirements/pip-tools.txt
	pip-compile --allow-unsafe --upgrade -o requirements/base.txt requirements/base.in
	pip-compile --allow-unsafe --upgrade -o requirements/tox.txt requirements/tox.in
	pip-compile --allow-unsafe --upgrade -o requirements/test.txt requirements/test.in
