from pathlib import Path

import pytest

from balanceador_equipos.jugadores.servicio_jugadores import ServicioJugadores
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion
from balanceador_equipos.persistencia import (
    actualizar_jugador,
    guardar_jugador,
    inicializar_base_datos,
    obtener_jugador,
    obtener_jugadores,
    obtener_ruta_base_datos,
)

from conftest import crear_habilidades, crear_jugador


def test_usa_la_base_de_datos_temporal(base_datos_temporal: Path) -> None:
    assert obtener_ruta_base_datos() == base_datos_temporal
    assert base_datos_temporal.exists()


def test_inicializar_es_idempotente() -> None:
    inicializar_base_datos()
    inicializar_base_datos()

    assert obtener_jugadores() == []


def test_guardar_y_leer_conserva_todos_los_datos() -> None:
    original = Jugador(
        id=None,
        nombre="Ana",
        habilidades=crear_habilidades(20, velocidad=99, reflejos=1),
        posicion_sugerida=Posicion.EXTREMO,
        puntuacion=72.5,
    )

    id_jugador = guardar_jugador(original)
    leido = obtener_jugador(id_jugador)

    assert leido is not None
    assert leido.id == id_jugador
    assert leido.nombre == original.nombre
    assert leido.habilidades == original.habilidades
    assert leido.posicion_sugerida == original.posicion_sugerida
    assert leido.puntuacion == original.puntuacion


def test_obtener_jugador_inexistente() -> None:
    assert obtener_jugador(12345) is None


def test_obtener_jugadores_ordenados_por_id() -> None:
    ids = [
        guardar_jugador(crear_jugador(id=None, puntuacion=50.0, nombre=n))
        for n in ("A", "B", "C")
    ]

    assert [j.id for j in obtener_jugadores()] == ids


def test_guardar_sin_perfil_falla() -> None:
    jugador = Jugador(
        id=None,
        nombre="Ana",
        habilidades=crear_habilidades(),
        posicion_sugerida=None,
        puntuacion=None,
    )

    with pytest.raises(ValueError):
        guardar_jugador(jugador)


def test_actualizar_jugador_inexistente_falla() -> None:
    with pytest.raises(ValueError, match="No existe"):
        actualizar_jugador(crear_jugador(id=999, puntuacion=50.0))


def test_actualizar_solo_nombre_conserva_perfil() -> None:
    registrado = ServicioJugadores.registrar(
        crear_jugador(id=None, puntuacion=61.0, posicion=Posicion.DEFENSA)
    )

    actualizado = ServicioJugadores.actualizar(
        jugador=registrado,
        nombre="Nuevo nombre",
        habilidades=registrado.habilidades,
    )

    assert actualizado.nombre == "Nuevo nombre"
    assert actualizado.posicion_sugerida == Posicion.DEFENSA
    assert actualizado.puntuacion == 61.0
    assert ServicioJugadores.obtener_por_id(registrado.id or 0) == actualizado


def test_actualizar_habilidades_recalcula_perfil() -> None:
    registrado = ServicioJugadores.registrar(
        crear_jugador(id=None, puntuacion=61.0, posicion=Posicion.DEFENSA)
    )

    habilidades_portero = crear_habilidades(
        10,
        reflejos=100,
        estirada=100,
        juego_aereo=100,
        seguridad_balon=100,
    )

    actualizado = ServicioJugadores.actualizar(
        jugador=registrado,
        nombre=registrado.nombre,
        habilidades=habilidades_portero,
    )

    assert actualizado.posicion_sugerida == Posicion.PORTERO
    assert actualizado.puntuacion != 61.0
    assert ServicioJugadores.obtener_por_id(registrado.id or 0) == actualizado
