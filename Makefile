.PHONY: install playground run test

install:
	uv pip install --offline -e .

playground:
	export HOME=/Users/dineshg/Downloads/adk-workspace && export UV_OFFLINE=1 && .venv/bin/agents-cli playground --port 18081

run:
	export HOME=/Users/dineshg/Downloads/adk-workspace && export UV_OFFLINE=1 && .venv/bin/agents-cli run

test:
	export PYTHONDONTWRITEBYTECODE=1 && .venv/bin/pytest tests/unit/test_agent.py
