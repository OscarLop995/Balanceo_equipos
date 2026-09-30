from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from balanceador_equipos.backend.routers.jugadores import (
    router as jugadores_router,
)
from balanceador_equipos.backend.routers.partidos import (
    router as partidos_router,
)
from balanceador_equipos.persistencia import inicializar_base_datos


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI) -> AsyncIterator[None]:
    inicializar_base_datos()
    yield


app = FastAPI(
    title="Balanceador de equipos API",
    version="0.1.0",
    lifespan=ciclo_de_vida,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio() -> dict[str, str]:
    return {"mensaje": "API del Balanceador de equipos"}


app.include_router(jugadores_router)
app.include_router(partidos_router)