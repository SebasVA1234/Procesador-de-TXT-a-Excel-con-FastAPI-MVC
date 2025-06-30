#!/bin/bash

# Activar el entorno de poetry y levantar FastAPI
echo "🔁 Iniciando servidor FastAPI en http://localhost:8000 ..."
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000