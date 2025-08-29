FROM python:3.12-slim

ENV PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3

RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Instalar dependencias con Poetry (sin crear venv)
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Copiar el código
COPY . /app

# Asegurar carpetas usadas por tu app
RUN mkdir -p uploads output

EXPOSE 5000
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","5000","--reload"]
