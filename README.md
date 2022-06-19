# file_storage

[![Maintainability](https://api.codeclimate.com/v1/badges/7364174229c0f6805dd8/maintainability)](https://codeclimate.com/github/depocoder/file_storage/maintainability)
[![linter check](https://github.com/depocoder/file_storage/actions/workflows/linter.yml/badge.svg)](https://github.com/depocoder/file_storage/actions/workflows/linter.yml)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Store your data on your self-hosted cloud

Start a project with:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up
```

If you want to develop in docker with autoreload, use this command:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up
```

This command exposes application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```


## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

## Migrations

If you want to migrate your database, you should run following commands:
```bash
# To run all migrations untill the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:
```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml --project-directory . down
```

For running tests on your local machine.
1. you need to start a database.

I prefer doing it with docker:
```
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=file_storage" -e "POSTGRES_USER=file_storage" -e "POSTGRES_DB=file_storage" postgres:13.6-bullseye
```


2. Run the pytest.
```bash
pytest -vv .
```
