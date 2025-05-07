#from fastapi import APIRouter, UploadFile, File
#from app.services.file_service import procesar_archivo_service  # Import correcto
#from app.services.file_service import procesar_archivo_service  # Import correcto
from fastapi.responses import FileResponse
import os
import uuid
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from fastapi import APIRouter
from fastapi import APIRouter, File, UploadFile
from app.services.file_service import procesar_archivo_service_proveedores, procesar_archivo_service_compras


router = APIRouter()

# Ruta para procesar pagos a proveedores
@router.post("/procesar_proveedores")
async def procesar_archivo_proveedores(file: UploadFile = File(...)):
    contenido_archivo = await file.read()
    nombre_archivo = file.filename
    with open(f"uploads/{nombre_archivo}", "wb") as f:
        f.write(contenido_archivo)
    
    # Procesar el archivo como pagos a proveedores
    result = procesar_archivo_service_proveedores(nombre_archivo)
    return {"archivo": result, "mensaje": "Archivo procesado correctamente como info de pagos a proveedores"}

# Ruta para procesar compras para coordinar
@router.post("/procesar_compras")
async def procesar_archivo_compras(file: UploadFile = File(...)):
    contenido_archivo = await file.read()
    nombre_archivo = file.filename
    with open(f"uploads/{nombre_archivo}", "wb") as f:
        f.write(contenido_archivo)
    
    # Procesar el archivo como compras para coordinar
    result = procesar_archivo_service_compras(nombre_archivo)
    return {"archivo": result, "mensaje": "Archivo procesado correctamente como info de compras para coordinar"}