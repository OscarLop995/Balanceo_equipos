from dataclasses import asdict

from balanceador_equipos.backend.schemas.jugadores import (
    HabilidadesCrear,
    HabilidadesRespuesta,
    JugadorRespuesta,
)
from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.jugador import Jugador


def convertir_habilidades(datos: HabilidadesCrear) -> Habilidades:
    return Habilidades(**datos.model_dump())


def convertir_habilidades_respuesta(
    habilidades: Habilidades,
) -> HabilidadesRespuesta:
    return HabilidadesRespuesta(**asdict(habilidades))


def convertir_jugador_respuesta(jugador: Jugador) -> JugadorRespuesta:
    if jugador.id is None:
        raise ValueError(
            "No se puede convertir un jugador sin identificador "
            "en una respuesta de la API."
        )

    if jugador.posicion_sugerida is None:
        raise ValueError(
            "No se puede convertir un jugador sin posición sugerida "
            "en una respuesta de la API."
        )

    if jugador.puntuacion is None:
        raise ValueError(
            "No se puede convertir un jugador sin puntuación "
            "en una respuesta de la API."
        )

    return JugadorRespuesta(
        id=jugador.id,
        nombre=jugador.nombre,
        habilidades=convertir_habilidades_respuesta(jugador.habilidades),
        posicion_sugerida=jugador.posicion_sugerida,
        puntuacion=jugador.puntuacion,
    )