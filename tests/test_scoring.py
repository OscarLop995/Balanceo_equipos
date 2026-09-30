import pytest

from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion
from balanceador_equipos.scoring.calculador_puntuacion import (
    CalculadorPuntuacion,
)
from balanceador_equipos.scoring.perfilador_jugador import PerfiladorJugador

from conftest import crear_habilidades


def _jugador_sin_perfil(**habilidades: int) -> Jugador:
    return Jugador(
        id=None,
        nombre="Prueba",
        habilidades=crear_habilidades(10, **habilidades),
        posicion_sugerida=None,
        puntuacion=None,
    )


@pytest.mark.parametrize("valor", [0, 37, 100])
def test_habilidades_uniformes_puntuan_igual_en_todas_las_posiciones(
    valor: int,
) -> None:
    # Los pesos de cada posición suman 1.0.
    jugador = Jugador(
        id=None,
        nombre="Prueba",
        habilidades=crear_habilidades(valor),
        posicion_sugerida=None,
        puntuacion=None,
    )

    puntuaciones = CalculadorPuntuacion.calcular(jugador)

    assert set(puntuaciones) == set(Posicion)

    for puntuacion in puntuaciones.values():
        assert puntuacion == pytest.approx(valor)


def test_perfil_de_portero() -> None:
    jugador = _jugador_sin_perfil(
        reflejos=100,
        estirada=100,
        juego_aereo=100,
        seguridad_balon=100,
        salto=100,
    )

    perfilado = PerfiladorJugador.calcular(jugador)

    assert perfilado.posicion_sugerida == Posicion.PORTERO


def test_perfil_de_defensa() -> None:
    jugador = _jugador_sin_perfil(
        marcaje=100,
        entradas=100,
        intercepciones=100,
        posicionamiento_defensivo=100,
        anticipacion=100,
    )

    perfilado = PerfiladorJugador.calcular(jugador)

    assert perfilado.posicion_sugerida == Posicion.DEFENSA


def test_perfil_de_delantero() -> None:
    jugador = _jugador_sin_perfil(
        potencia_tiro=100,
        precision_tiro=100,
        desmarque=100,
        posicionamiento_ofensivo=100,
    )

    perfilado = PerfiladorJugador.calcular(jugador)

    assert perfilado.posicion_sugerida == Posicion.DELANTERO


def test_perfilador_conserva_datos_y_usa_la_mejor_puntuacion() -> None:
    jugador = _jugador_sin_perfil(regate=90, velocidad=95)

    perfilado = PerfiladorJugador.calcular(jugador)
    puntuaciones = CalculadorPuntuacion.calcular(jugador)

    assert perfilado.nombre == jugador.nombre
    assert perfilado.habilidades == jugador.habilidades
    assert perfilado.puntuacion == max(puntuaciones.values())
