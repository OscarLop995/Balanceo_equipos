from itertools import combinations

import pytest

from balanceador_equipos.balanceo.balanceador_equipos import (
    BalanceadorEquipos,
)
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion

from conftest import crear_jugador


def _plantilla(cantidad: int) -> list[Jugador]:
    return [
        crear_jugador(id=i, puntuacion=40.0 + i * 1.5)
        for i in range(1, cantidad + 1)
    ]


@pytest.mark.parametrize("tamano", [8, 9, 10])
def test_equipos_son_complementarios_y_del_tamano_correcto(
    tamano: int,
) -> None:
    jugadores = _plantilla(tamano * 2)

    distribucion = BalanceadorEquipos.balancear(jugadores, tamano)

    ids_a = {jugador.id for jugador in distribucion.equipo_a}
    ids_b = {jugador.id for jugador in distribucion.equipo_b}

    assert len(distribucion.equipo_a) == tamano
    assert len(distribucion.equipo_b) == tamano
    assert ids_a.isdisjoint(ids_b)
    assert ids_a | ids_b == {jugador.id for jugador in jugadores}


def test_puntuaciones_de_la_distribucion_son_coherentes() -> None:
    distribucion = BalanceadorEquipos.balancear(_plantilla(16), 8)

    suma_a = sum(j.puntuacion or 0 for j in distribucion.equipo_a)
    suma_b = sum(j.puntuacion or 0 for j in distribucion.equipo_b)

    assert distribucion.puntuacion_equipo_a == pytest.approx(suma_a)
    assert distribucion.puntuacion_equipo_b == pytest.approx(suma_b)
    assert distribucion.diferencia_puntuacion == pytest.approx(
        abs(suma_a - suma_b)
    )


def test_encuentra_la_diferencia_minima() -> None:
    jugadores = _plantilla(16)
    puntuaciones = [j.puntuacion or 0 for j in jugadores]
    total = sum(puntuaciones)

    minimo_esperado = min(
        abs(total - 2 * sum(combinacion))
        for combinacion in combinations(puntuaciones, 8)
    )

    distribucion = BalanceadorEquipos.balancear(jugadores, 8)

    assert distribucion.diferencia_puntuacion == pytest.approx(
        minimo_esperado
    )


def test_jugadores_identicos_con_distinto_id_no_se_pierden() -> None:
    # Antes el Equipo B se armaba por igualdad; se valida por ID.
    jugadores = [
        crear_jugador(id=i, puntuacion=50.0, nombre="Mismo nombre")
        for i in range(1, 17)
    ]

    distribucion = BalanceadorEquipos.balancear(jugadores, 8)

    assert len(distribucion.equipo_a) == 8
    assert len(distribucion.equipo_b) == 8


def test_rechaza_jugador_repetido() -> None:
    jugadores = _plantilla(15)
    jugadores.append(jugadores[0])

    with pytest.raises(ValueError, match="más de una vez"):
        BalanceadorEquipos.balancear(jugadores, 8)


def test_dos_porteros_quedan_en_equipos_distintos() -> None:
    jugadores = _plantilla(14) + [
        crear_jugador(id=100, puntuacion=90.0, posicion=Posicion.PORTERO),
        crear_jugador(id=101, puntuacion=30.0, posicion=Posicion.PORTERO),
    ]

    distribucion = BalanceadorEquipos.balancear(jugadores, 8)

    for equipo in (distribucion.equipo_a, distribucion.equipo_b):
        porteros = [
            j for j in equipo
            if j.posicion_sugerida == Posicion.PORTERO
        ]
        assert len(porteros) == 1


def test_regla_de_porteros_prevalece_sobre_el_equilibrio() -> None:
    # Sin la regla, el reparto perfecto (diferencia 0) juntaría a los dos
    # porteros: 10 + 90 + 6 * 50 = 400 contra 8 * 50 = 400.
    # Con la regla, lo mejor posible es 90 + 7 * 50 = 440 contra
    # 10 + 7 * 50 = 360, es decir, una diferencia de 80.
    jugadores = [
        crear_jugador(id=i, puntuacion=50.0) for i in range(1, 15)
    ] + [
        crear_jugador(id=100, puntuacion=10.0, posicion=Posicion.PORTERO),
        crear_jugador(id=101, puntuacion=90.0, posicion=Posicion.PORTERO),
    ]

    distribucion = BalanceadorEquipos.balancear(jugadores, 8)

    porteros_a = [
        j for j in distribucion.equipo_a
        if j.posicion_sugerida == Posicion.PORTERO
    ]
    porteros_b = [
        j for j in distribucion.equipo_b
        if j.posicion_sugerida == Posicion.PORTERO
    ]

    assert len(porteros_a) == 1
    assert len(porteros_b) == 1
    assert distribucion.diferencia_puntuacion == pytest.approx(80.0)


def test_con_tres_porteros_ningun_equipo_queda_sin_portero() -> None:
    jugadores = [
        crear_jugador(id=i, puntuacion=50.0) for i in range(1, 14)
    ] + [
        crear_jugador(id=100 + i, puntuacion=80.0, posicion=Posicion.PORTERO)
        for i in range(3)
    ]

    distribucion = BalanceadorEquipos.balancear(jugadores, 8)

    for equipo in (distribucion.equipo_a, distribucion.equipo_b):
        assert any(
            j.posicion_sugerida == Posicion.PORTERO for j in equipo
        )


@pytest.mark.parametrize("tamano", [7, 11])
def test_rechaza_tamano_invalido(tamano: int) -> None:
    with pytest.raises(ValueError):
        BalanceadorEquipos.balancear(_plantilla(tamano * 2), tamano)


def test_rechaza_cantidad_incorrecta() -> None:
    with pytest.raises(ValueError):
        BalanceadorEquipos.balancear(_plantilla(15), 8)


def test_rechaza_jugador_sin_perfil() -> None:
    jugadores = _plantilla(15)
    jugadores.append(
        Jugador(
            id=99,
            nombre="Sin perfil",
            habilidades=jugadores[0].habilidades,
            posicion_sugerida=None,
            puntuacion=None,
        )
    )

    with pytest.raises(ValueError):
        BalanceadorEquipos.balancear(jugadores, 8)
