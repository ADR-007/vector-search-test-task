FROM python:3.11.8

RUN pip install poetry

RUN mkdir /app
WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-dev --no-root

COPY testtask/ ./testtask/
COPY wiki_texts/ ./wiki_texts/

