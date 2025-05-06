activate-venv:
	source .venv/bin/activate

py-format:
	ruff format

py-lint:
	ruff check --fix

py-static:
	mypy cryptid

py-test:
	coverage run -m pytest tests/

coverage:
	make py-test
	coverage report -m --skip-empty --omit="tests/*"

py-ci:
	make py-lint py-format py-static py-test

refresh-venv:
	uv sync
	git restore --staged .
	git add pyproject.toml
	git add uv.lock