"""
Aplicación de producción: un único servicio que sirve la web y la API.

- /api/...  → API existente (balanceador_equipos.backend.main:app)
- /...      → frontend compilado (frontend/dist), con fallback a index.html
              para las rutas de React Router.

Toda petición pasa antes por Cloudflare Access.

Ejecutar con:
    uvicorn balanceador_equipos.backend.produccion:app
"""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from balanceador_equipos.backend.cloudflare_access import (
    MiddlewareCloudflareAccess,
)
from balanceador_equipos.backend.main import app as api
from balanceador_equipos.persistencia import inicializar_base_datos

VARIABLE_FRONTEND = "BALANCEADOR_FRONTEND_DIST"

RUTA_FRONTEND_POR_DEFECTO = (
    Path(__file__).resolve().parents[3] / "frontend" / "dist"
)


def obtener_ruta_frontend() -> Path:
    ruta = os.environ.get(VARIABLE_FRONTEND)

    return Path(ruta) if ruta else RUTA_FRONTEND_POR_DEFECTO


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI) -> AsyncIterator[None]:
    # El lifespan de una sub-aplicación montada no se ejecuta,
    # así que la base de datos se inicializa aquí.
    inicializar_base_datos()
    yield


def crear_aplicacion() -> FastAPI:
    aplicacion = FastAPI(
        title="Balanceador de equipos",
        lifespan=ciclo_de_vida,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    aplicacion.mount("/api", api)

    @aplicacion.get("/{ruta:path}", include_in_schema=False)
    def servir_frontend(ruta: str) -> FileResponse:
        raiz = obtener_ruta_frontend().resolve()
        indice = raiz / "index.html"

        if not indice.is_file():
            raise HTTPException(
                status_code=503,
                detail="El frontend no está compilado.",
            )

        if ruta:
            archivo = (raiz / ruta).resolve()

            # Evita salir de la carpeta del frontend (p. ej. "../../").
            if archivo.is_relative_to(raiz) and archivo.is_file():
                return FileResponse(archivo)

            # Un recurso estático inexistente no debe devolver index.html.
            if ruta.startswith("assets/"):
                raise HTTPException(status_code=404)

        # index.html no se cachea para que cada despliegue se vea al instante.
        return FileResponse(
            indice,
            headers={"Cache-Control": "no-cache"},
        )

    aplicacion.add_middleware(MiddlewareCloudflareAccess)

    return aplicacion


app = crear_aplicacion()
