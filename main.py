from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException, Header
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import jwt  # PyJWT
from procesador import procesar_archivo

app = FastAPI(title="Procesador TXT->Excel - Ecualand")

# Carpetas de trabajo (efímeras: el Excel se devuelve en la misma request)
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Autenticación: reutiliza el login de Helper Ecualand (mismo JWT) ---------
# Helper emite un JWT (HS256, firmado con JWT_SECRET). Este modulo valida ESE
# mismo token con el MISMO secreto, asi los contadores NO vuelven a loguearse:
# entran por el boton de Helper, que abre esta app con el token en el fragment
# de la URL (#token=...). El fragment no viaja al servidor ni a los logs.
JWT_SECRET = os.environ.get("JWT_SECRET", "")
AUTH_DISABLED = os.environ.get("AUTH_DISABLED") == "1"  # SOLO para dev local


def get_current_user(authorization: str = Header(default=None)):
    if AUTH_DISABLED:
        return {"username": "dev", "full_name": "Desarrollo"}
    if not JWT_SECRET:
        # Falla cerrada: sin secreto no se puede validar nada.
        raise HTTPException(status_code=503, detail="Autenticacion no configurada (falta JWT_SECRET)")
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="No autenticado")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sesion expirada, volve a entrar desde Helper")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido")
    return payload


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # La pagina se sirve siempre; el JS pide el token y valida contra /api/me.
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    # Healthcheck para Railway (no expone datos).
    return {"status": "ok", "auth_configured": bool(JWT_SECRET) or AUTH_DISABLED}


@app.get("/api/me")
async def me(user=Depends(get_current_user)):
    # El frontend lo llama al cargar: confirma la sesion y saluda al usuario.
    return {"username": user.get("username"), "full_name": user.get("full_name")}


@app.post("/procesar")
async def procesar(file: UploadFile = File(...), user=Depends(get_current_user)):
    # Sanea el nombre (evita path traversal): solo el basename entra a uploads/.
    safe_name = os.path.basename(file.filename or "archivo.txt")
    path = f"uploads/{safe_name}"
    with open(path, "wb") as f:
        f.write(await file.read())

    output_path = procesar_archivo(path)

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="archivo_procesado.xlsx",
    )
