from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from procesador import procesar_archivo

app = FastAPI()

# Crear carpetas si no existen
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Configuración de templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Página principal (formulario HTML)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint de procesamiento
@app.post("/procesar")
async def procesar(file: UploadFile = File(...)):
    # Guardar archivo temporal
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    # Llamar a la función que procesa el archivo
    output_path = procesar_archivo(path)

    # Retornar el archivo Excel generado
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="archivo_procesado.xlsx"
    )
