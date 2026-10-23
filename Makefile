GITLEAKS_VERSION := v8.30.1
GITLEAKS_DOCKER_CONFIG ?=

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

.PHONY: gitleaks

gitleaks:
	@if command -v gitleaks >/dev/null 2>&1; then \
		gitleaks git --redact=100 --verbose --log-opts="-m HEAD" .; \
	elif command -v docker >/dev/null 2>&1; then \
		if [ -n "${GITLEAKS_DOCKER_CONFIG}" ]; then \
			mkdir -p "${GITLEAKS_DOCKER_CONFIG}"; \
			export DOCKER_CONFIG="${GITLEAKS_DOCKER_CONFIG}"; \
		fi; \
		docker run --rm \
			-v "$$(pwd):$$(pwd):ro" \
			-v "$$(git rev-parse --path-format=absolute --git-common-dir):$$(git rev-parse --path-format=absolute --git-common-dir):ro" \
			-w "$$(pwd)" ghcr.io/gitleaks/gitleaks:${GITLEAKS_VERSION} git --redact=100 --verbose --log-opts="-m HEAD" .; \
	else \
		echo "gitleaksまたはdockerをインストールしてください。" >&2; \
		exit 127; \
	fi
