install:
	poetry install --no-root

full-install:
	pip3 install --user poetry==1.2.0b2
	make install

lint:
	poetry run flake8 .
	poetry run mypy .