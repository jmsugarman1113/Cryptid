py-format:
	ruff format

py-lint:
	ruff check

py-static:
	mypy

py-ci:
	make py-format py-lint py-static

refresh-venv:
	uv sync