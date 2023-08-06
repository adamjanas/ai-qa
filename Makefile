PATH  := $(PATH)
SHELL := /bin/bash

black:
	poetry run black .

ruff:
	poetry run ruff check . --fix
lint:
	make black
	make ruff