from collections.abc import Sequence

from balanceador_equipos.backend.schemas.partidos import (
    JugadorEquipoRespuesta,
    ResultadoBalanceoRespuesta,
    ResultadoEquipoRespuesta,
)
from balanceador_equipos.models.jugador import Jugador


def convertir_jugador_equipo_respuesta(
    jugador: Jugador,
) -> JugadorEquipoRespuesta:
    if jugador.id is None:
        raise ValueError(
            "No se puede convertir un jugador sin identificador "
            "en una respuesta de equipo."
        )

    if jugador.posicion_sugerida is None:
        raise ValueError(
            "No se puede convertir un jugador sin posición sugerida "
            "en una respuesta de equipo."
        )

    return JugadorEquipoRespuesta(
        id=jugador.id,
        nombre=jugador.nombre,
        posicion_sugerida=jugador.posicion_sugerida,
    )


def convertir_resultado_balanceo(
    equipo_a: Sequence[Jugador],
    equipo_b: Sequence[Jugador],
    puntuacion_equipo_a: float,
    puntuacion_equipo_b: float,
    diferencia_puntuacion: float,
) -> ResultadoBalanceoRespuesta:
    jugadores_equipo_a = [
        convertir_jugador_equipo_respuesta(jugador)
        for jugador in equipo_a
    ]

    jugadores_equipo_b = [
        convertir_jugador_equipo_respuesta(jugador)
        for jugador in equipo_b
    ]

    return ResultadoBalanceoRespuesta(
        equipo_a=ResultadoEquipoRespuesta(
            jugadores=jugadores_equipo_a,
            puntuacion_total=puntuacion_equipo_a,
        ),
        equipo_b=ResultadoEquipoRespuesta(
            jugadores=jugadores_equipo_b,
            puntuacion_total=puntuacion_equipo_b,
        ),
        diferencia_puntuacion=diferencia_puntuacion,
    )