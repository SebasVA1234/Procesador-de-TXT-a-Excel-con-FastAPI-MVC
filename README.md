Aquí tienes el **README** listo para copiar/pegar en tu repo 👇
*(todo en Markdown, sin dependencias externas)*

---

# Procesador de TXT a Excel con FastAPI (MVC-lite) · Docker Ready

Convierte mensajes de texto desordenados (WhatsApp/TXT) en una **tabla Excel** con encabezados organizados.
Proyecto listo para **Docker/Compose**, **Poetry** y **Uvicorn**. Incluye túnel público opcional para compartir un link temporal.

---

## ✨ Características

* **Upload TXT** desde una UI sencilla (Jinja2).
* **Parsing** a `pandas.DataFrame` y **exportación a `.xlsx`** (openpyxl).
* **FastAPI + Uvicorn** (docs en `/docs`).
* **Docker Compose** (1 comando para levantar).
* **Túnel público opcional** con Cloudflare Quick Tunnel (link temporal para compartir).
* **Opcional**: Basic Auth + enlace con **token temporal** (ver *Seguridad*).

---

## 🧱 Stack

* **Backend**: FastAPI (Python 3.12), Uvicorn, Jinja2
* **Datos/Excel**: pandas, openpyxl
* **Deps**: Poetry
* **Infra dev**: Docker + Docker Compose

---

## 📁 Estructura (MVC-lite)

```
.
├─ main.py                # App FastAPI + rutas
├─ procesador.py          # Lógica: TXT -> DataFrame -> Excel
├─ templates/
│   └─ index.html         # UI (formulario de carga)
├─ static/
│   └─ style.css          # Estilos básicos
├─ uploads/               # Archivos subidos (volumen)
├─ output/                # Excel generado (volumen)
├─ pyproject.toml         # Dependencias Poetry
├─ Dockerfile             # Imagen de la app
├─ compose.yaml           # Servicios: app (+ túnel opcional)
└─ start.sh               # Script helper (opcional)
```

---

## 🚀 Arranque rápido (Docker)

Requisitos: **Docker** y **Docker Compose v2**.

```bash
# 1) Levantar en segundo plano (build incluido)
docker compose up -d --build

# 2) Abrir
# App     → http://localhost:5000
# Docs    → http://localhost:5000/docs
```

**Ver estado y logs**

```bash
docker compose ps
docker compose logs -f app
```

**Apagar / limpiar**

```bash
docker compose down          # apaga contenedores
# Limpieza opcional de recursos no usados:
# docker system prune -af
```

> También puedes usar `./start.sh` (si está presente).

---

## 🌐 Compartir con un link (opcional)

Este repo incluye un servicio **Cloudflare Quick Tunnel** en `compose.yaml`.

1. Levanta normalmente:

```bash
docker compose up -d --build
```

2. Obtén la **URL pública** del túnel:

```bash
docker compose logs tunnel \
| sed -n 's/.*https:\/\/\([a-zA-Z0-9.-]*trycloudflare\.com\).*/https:\/\/\1/p' \
| tail -1
```

3. Comparte ese `https://<algo>.trycloudflare.com` para pruebas.

> La URL cambia **cada vez que levantas** el túnel.

**Ver logs del túnel**

```bash
docker compose logs -f tunnel
```

---

## 🔒 Seguridad (opcional)

Si vas a compartir el túnel, se recomienda proteger la app:

### 1) Variables de entorno en `compose.yaml`

```yaml
services:
  app:
    environment:
      - APP_USER=sebas          # usuario para Basic Auth
      - APP_PASS=tu_contra_segura
      - SECRET_KEY=secreto_largo_unico
      # - MAX_UPLOAD_MB=10      # opcional: limitar tamaño de upload
```

### 2) Basic Auth + Token por enlace (parche opcional en `main.py`)

El proyecto puede integrarse con:

* **Basic Auth**: acceso con usuario/contraseña.
* **Token temporal por enlace**: `?token=...` con expiración (útil para compartir un link único).

> Si activas el parche, además tendrás un endpoint admin:

```
GET /admin/new-token?minutes=60&base=<URL_TUNEL>   # requiere Basic Auth
```

Devuelve un JSON con `url` lista para compartir (incluye `?token=`).
*El código base no trae este parche activo por defecto para mantenerlo simple. Puedes integrarlo cuando lo necesites.*

---

## 📲 Acceso desde otro dispositivo en tu red

* Obtén la IP local de tu máquina:

  ```bash
  hostname -I | awk '{print $1}'
  ```
* Desde el celular/otra PC (misma red), abre: `http://IP_LOCAL:5000/`.

**VirtualBox**: usa **Bridged Adapter** para que tu VM sea visible en la red.
**Firewall (UFW)**: abre el puerto si hace falta: `sudo ufw allow 5000/tcp`.

---

## ⚙️ Desarrollo local (sin Docker)

```bash
# Instala Poetry si no lo tienes
curl -sSL https://install.python-poetry.org | python3 -

# Instala dependencias y ejecuta
poetry install
poetry run uvicorn main:app --reload --port 5000
```

---

## 🧯 Troubleshooting

* **“permission denied” al usar Docker**
  Agrega tu usuario al grupo docker y re-abre sesión:

  ```bash
  sudo usermod -aG docker $USER
  newgrp docker
  ```

* **El túnel no muestra URL**
  Revisa logs crudos:

  ```bash
  docker compose logs -f tunnel
  ```

  Espera la línea con `https://<subdominio>.trycloudflare.com`.

* **No abre desde otra PC/cel**
  Verifica IP correcta (`hostname -I`), modo **Bridged** en VirtualBox y que el puerto **5000** esté accesible.

---

## 📄 Licencia

MIT — ajusta si tu proyecto requiere otra.

**Autor:** Sebas (SebasVA1234)
**Repo:** `Procesador-de-TXT-a-Excel-con-FastAPI-MVC`

---
