py-format:
	ruff format

py-lint:
	ruff check --select I --fix
	ruff check

py-static:
	mypy cryptid

py-ci:
	make py-lint py-format py-static

refresh-venv:
	uv sync