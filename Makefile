activate-venv:
	source .venv/bin/activate

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
	git restore --staged .
	git add pyproject.toml
	git add uv.lock