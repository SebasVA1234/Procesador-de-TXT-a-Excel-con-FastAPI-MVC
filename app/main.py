from fastapi import FastAPI
from app.controller.file_controller import router
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 🟡 Permitir conexión desde React (frontend en localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>API de Procesamiento de TXT</h1>
    <p>Usa la <a href='/docs'>documentación interactiva</a> para probar el sistema.</p>
    """

# Crear carpetas si no existen
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Incluir las rutas del controlador
app.include_router(router, prefix="/archivo", tags=["Procesamiento TXT"])
#sip