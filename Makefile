ifndef SOURCE_FILES
	export SOURCE_FILES:=convpandas
endif
ifndef TEST_FILES
	export TEST_FILES:=tests
endif

.PHONY: init lint format validate test

format:
	uv run ruff format ${SOURCE_FILES} ${TEST_FILES}
	uv run ruff check ${SOURCE_FILES} ${TEST_FILES} --fix-only --exit-zero

lint:
	uv run ruff check ${SOURCE_FILES}
	# テストコードはチェックを緩和する
	# pygrep-hooks, flake8-datetimez, line-too-long, flake8-annotations, unused-noqa
	uv run ruff check ${TEST_FILES} --ignore PGH,DTZ,E501,ANN,RUF100
	uv run mypy ${SOURCE_FILES} ${TEST_FILES}


test:
	uv run pytest tests
