from dataclasses import fields
from pathlib import Path

import pytest

from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion
from balanceador_equipos.persistencia import (
    VARIABLE_ENTORNO_BASE_DATOS,
    inicializar_base_datos,
)


def crear_habilidades(valor: int = 50, **cambios: int) -> Habilidades:
    """
    Crea habilidades con el mismo valor para todas, salvo las indicadas.
    """

    valores = {campo.name: valor for campo in fields(Habilidades)}
    valores.update(cambios)

    return Habilidades(**valores)


def crear_jugador(
    id: int | None,
    puntuacion: float,
    posicion: Posicion = Posicion.MEDIOCAMPISTA,
    nombre: str | None = None,
) -> Jugador:
    """
    Crea un jugador ya perfilado, sin pasar por el cálculo de puntuación.
    """

    return Jugador(
        id=id,
        nombre=nombre or f"Jugador {id}",
        habilidades=crear_habilidades(),
        posicion_sugerida=posicion,
        puntuacion=puntuacion,
    )


@pytest.fixture(autouse=True)
def base_datos_temporal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """
    Redirige todas las pruebas a una base de datos temporal para no
    tocar nunca data/jugadores.db.
    """

    ruta = tmp_path / "jugadores_test.db"
    monkeypatch.setenv(VARIABLE_ENTORNO_BASE_DATOS, str(ruta))
    inicializar_base_datos()

    return ruta
