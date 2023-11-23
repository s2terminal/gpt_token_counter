FROM python:3.10-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN git config --global --add safe.directory /app

RUN pip install poetry \
  && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install

# prod
FROM builder AS prod
ENV NICEGUI_ENV="production"

COPY ./gpt_token_counter ./gpt_token_counter

# https://cloud.google.com/run/docs/issues?hl=ja#home
CMD HOME=/root poetry run python gpt_token_counter/main.py
