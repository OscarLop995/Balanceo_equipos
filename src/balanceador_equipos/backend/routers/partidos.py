from fastapi import APIRouter, HTTPException

from balanceador_equipos.backend.mappers.partidos import (
    convertir_resultado_balanceo,
)
from balanceador_equipos.backend.schemas.partidos import (
    SolicitudBalanceo,
    ResultadoBalanceoRespuesta,
)
from balanceador_equipos.balanceo.servicio_balanceo import ServicioBalanceo
from balanceador_equipos.jugadores.servicio_jugadores import ServicioJugadores
from balanceador_equipos.models.jugador import Jugador

router = APIRouter(
    prefix="/partidos",
    tags=["Partidos"],
)


@router.post(
    "/balancear",
    response_model=ResultadoBalanceoRespuesta,
)
def balancear_partido(
    solicitud: SolicitudBalanceo,
) -> ResultadoBalanceoRespuesta:
    cantidad_jugadores_requerida = solicitud.tamano_equipo * 2

    if len(solicitud.jugadores) != cantidad_jugadores_requerida:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Para equipos de {solicitud.tamano_equipo} jugadores "
                f"se requieren exactamente "
                f"{cantidad_jugadores_requerida} jugadores."
            ),
        )

    jugadores: list[Jugador] = []

    for id_jugador in solicitud.jugadores:
        jugador = ServicioJugadores.obtener_por_id(id_jugador)

        if jugador is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No existe un jugador con el identificador "
                    f"{id_jugador}."
                ),
            )

        jugadores.append(jugador)

    try:
        distribucion = ServicioBalanceo.balancear(
            jugadores=jugadores,
            tamano_equipo=solicitud.tamano_equipo,
        )
    except (ValueError, RuntimeError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return convertir_resultado_balanceo(
        equipo_a=distribucion.equipo_a,
        equipo_b=distribucion.equipo_b,
        puntuacion_equipo_a=distribucion.puntuacion_equipo_a,
        puntuacion_equipo_b=distribucion.puntuacion_equipo_b,
        diferencia_puntuacion=distribucion.diferencia_puntuacion,
    )