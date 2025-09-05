# Dockerfile (reemplaza el tuyo)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir "poetry==1.8.3"

WORKDIR /app

# Dependencias primero (mejor cache)
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --without dev

# Código
COPY . .

# Carpetas que usas
RUN mkdir -p uploads output

ENV PORT=5000
EXPOSE 5000

# Railway pondrá $PORT; usa fallback 5000 para local
CMD ["bash","-lc","poetry run uvicorn main:app --host 0.0.0.0 --port ${PORT:-5000}"]
# CMD ["bash","-lc","poetry run python main.py"]