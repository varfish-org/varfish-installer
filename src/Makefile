.PHONY: help
help:
	@echo "make lint - run linting"
	@echo "make black-lint - run black linting"
	@echo "make flake8-lint - run flake8 linting"
	@echo "make pyright-lint - run pyright linting"
	@echo "make isort-lint - run isort linting"
	@echo "make format - run formatting"
	@echo "make black-format - run black formatting"
	@echo "make isort-format - run isort formatting"
	@echo "make test - run tests"

.PHONY: lint
lint: black-lint flake8-lint pyright-lint isort-lint

.PHONY: black-lint
black-lint:
	black --check .

.PHONY: flake8-lint
flake8-lint:
	flake8 --max-line-length 100 .

.PHONY: pyright-lint
pyright-lint:
	pyright .

.PHONY: isort-lint
isort-lint:
	isort --check .

.PHONY: format
format: isort-format black-format

.PHONY: black-format
black-format:
	black .

.PHONY: isort-format
isort-format:
	isort .

.PHONY: test
test:
	pytest -vvv .
