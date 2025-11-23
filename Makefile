.PHONY: install test lint format docs clean

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

lint:
	pre-commit run --all-files

format:
	black src tests
	isort src tests --profile black

.test-deps:
	python -m pip install pytest

test: .test-deps
	pytest

docs:
	mkdocs build --strict

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache build dist artifacts
