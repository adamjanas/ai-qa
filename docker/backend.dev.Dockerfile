FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN pip3 install poetry

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false

RUN poetry install

COPY ./backend /code/backend