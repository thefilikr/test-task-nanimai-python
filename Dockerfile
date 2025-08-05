FROM python:3.11-slim

WORKDIR /app

# Установим системные зависимости
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Копируем poetry и зависимости
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копируем исходный код
COPY . .

# Открываем порты для HTTP и gRPC
EXPOSE 8000 50051
