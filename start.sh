#!/bin/bash

# Levantar el backend (FastAPI)
#poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Levantar el frontend (React con Vite en el puerto 5173)
#!/bin/bash

cd frontend
npm install
npm run full