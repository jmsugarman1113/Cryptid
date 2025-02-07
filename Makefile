activate-venv:
	source .venv/bin/activate

py-format:
	ruff format

py-lint:
	ruff check --fix

py-static:
	mypy cryptid

py-test:
	pytest tests/

py-ci:
	make py-lint py-format py-static py-test

refresh-venv:
	uv sync
	git restore --staged .
	git add pyproject.toml
	git add uv.lock