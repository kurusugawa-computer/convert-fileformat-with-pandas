ifndef TARGET
	export TARGET:=convpandas
endif
.PHONY: lint format  publish init test

init:
	pip install poetry --upgrade
	poetry install

test:
	poetry run pytest tests

format:
	poetry run autoflake  --in-place --remove-all-unused-imports  --ignore-init-module-imports --recursive ${TARGET}
	poetry run black ${TARGET}
	poetry run isort --verbose --recursive ${TARGET}

lint:
	poetry run mypy ${TARGET}
	poetry run flake8 ${TARGET}

publish:
	poetry publish --build
