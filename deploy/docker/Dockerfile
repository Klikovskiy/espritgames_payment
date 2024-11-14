# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app_espritgames

# Отключае копировангие лишних файлов и буферизацию консоли
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV PYTHONPATH="/app_espritgames/backend:${PYTHONPATH}"

# Копируем файлы проекта
COPY . .

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi