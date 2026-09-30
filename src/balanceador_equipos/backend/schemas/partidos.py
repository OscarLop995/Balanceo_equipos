from pydantic import BaseModel, Field, field_validator

from balanceador_equipos.models.posicion import Posicion


class SolicitudBalanceo(BaseModel):
    jugadores: list[int] = Field(min_length=16, max_length=20)
    tamano_equipo: int = Field(ge=8, le=10)

    @field_validator("jugadores")
    @classmethod
    def validar_jugadores_unicos(cls, jugadores: list[int]) -> list[int]:
        repetidos = sorted(
            {
                id_jugador
                for id_jugador in jugadores
                if jugadores.count(id_jugador) > 1
            }
        )

        if repetidos:
            raise ValueError(
                "Los jugadores no pueden repetirse. IDs repetidos: "
                f"{repetidos}."
            )

        return jugadores


class JugadorEquipoRespuesta(BaseModel):
    id: int
    nombre: str
    posicion_sugerida: Posicion


class ResultadoEquipoRespuesta(BaseModel):
    jugadores: list[JugadorEquipoRespuesta]
    puntuacion_total: float


class ResultadoBalanceoRespuesta(BaseModel):
    equipo_a: ResultadoEquipoRespuesta
    equipo_b: ResultadoEquipoRespuesta
    diferencia_puntuacion: float
