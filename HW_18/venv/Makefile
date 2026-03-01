-include .env
export

dev.install:
	@uv sync --locked

db.migration.new:
	@uv run python -m yoyo new -m "$(name)" -d $(DB_URL) migrations/

db.migrate:
	@uv run python -m yoyo apply -d $(DB_URL) migrations/

db.rollback:
	@uv run python -m yoyo rollback -d $(DB_URL) migrations/
