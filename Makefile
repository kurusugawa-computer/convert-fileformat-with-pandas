ifndef TARGET
	export TARGET:=convpandas
	export TEST_TARGET:=tests
endif
.PHONY: lint format  publish init test

init:
	pip install poetry --upgrade
	poetry install

test:
	poetry run pytest tests

format:
	poetry run autoflake  --in-place --remove-all-unused-imports  --ignore-init-module-imports --recursive ${TARGET} ${TEST_TARGET}
	poetry run black ${TARGET} ${TEST_TARGET}
	poetry run isort --verbose  ${TARGET} ${TEST_TARGET}

lint:
	poetry run mypy ${TARGET} ${TEST_TARGET}
	poetry run flake8 ${TARGET}

publish:
	poetry publish --build
