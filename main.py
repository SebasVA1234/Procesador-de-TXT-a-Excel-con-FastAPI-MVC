# main.py (reemplaza si el tuyo tiene "...")
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

# Templates y estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/procesar")
async def procesar(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    output_path = procesar_archivo(path)

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="archivo_procesado.xlsx"
    )
