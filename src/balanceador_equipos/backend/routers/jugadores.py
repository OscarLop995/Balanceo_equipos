from fastapi import APIRouter, HTTPException

from balanceador_equipos.backend.mappers.jugadores import (
    convertir_habilidades,
    convertir_jugador_respuesta,
)
from balanceador_equipos.backend.schemas.jugadores import (
    JugadorActualizar,
    JugadorCrear,
    JugadorRespuesta,
)
from balanceador_equipos.jugadores.servicio_jugadores import ServicioJugadores
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.scoring.perfilador_jugador import PerfiladorJugador

router = APIRouter(
    prefix="/jugadores",
    tags=["Jugadores"],
)


@router.get("")
def obtener_jugadores() -> list[JugadorRespuesta]:
    jugadores = ServicioJugadores.obtener_todos()

    return [
        convertir_jugador_respuesta(jugador)
        for jugador in jugadores
    ]


@router.post("")
def crear_jugador(datos: JugadorCrear) -> JugadorRespuesta:
    try:
        jugador = Jugador(
            id=None,
            nombre=datos.nombre,
            habilidades=convertir_habilidades(datos.habilidades),
            posicion_sugerida=None,
            puntuacion=None,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    jugador_perfilado = PerfiladorJugador.calcular(jugador)
    jugador_guardado = ServicioJugadores.registrar(jugador_perfilado)

    return convertir_jugador_respuesta(jugador_guardado)


@router.put("/{id_jugador}")
def actualizar_jugador(
    id_jugador: int,
    datos: JugadorActualizar,
) -> JugadorRespuesta:
    jugador = ServicioJugadores.obtener_por_id(id_jugador)

    if jugador is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe un jugador con el identificador {id_jugador}.",
        )

    try:
        jugador_actualizado = ServicioJugadores.actualizar(
            jugador=jugador,
            nombre=datos.nombre,
            habilidades=convertir_habilidades(datos.habilidades),
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return convertir_jugador_respuesta(jugador_actualizado)
