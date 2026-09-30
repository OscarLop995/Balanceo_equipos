from dataclasses import dataclass

from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.posicion import Posicion


@dataclass(frozen=True)
class Jugador:
    id: int | None
    nombre: str
    habilidades: Habilidades
    posicion_sugerida: Posicion | None
    puntuacion: float | None

    def __post_init__(self) -> None:
        nombre_limpio = self.nombre.strip()

        if not nombre_limpio:
            raise ValueError(
                "El nombre del jugador no puede estar vacío."
            )

        if nombre_limpio != self.nombre:
            raise ValueError(
                "El nombre del jugador no puede comenzar ni terminar "
                "con espacios."
            )

        if self.puntuacion is not None and not (
            0.0 <= self.puntuacion <= 100.0
        ):
            raise ValueError(
                "La puntuación del jugador debe estar entre 0 y 100."
            )

        if (
            self.puntuacion is None
            and self.posicion_sugerida is not None
        ):
            raise ValueError(
                "Un jugador con posición sugerida debe tener puntuación."
            )

        if (
            self.puntuacion is not None
            and self.posicion_sugerida is None
        ):
            raise ValueError(
                "Un jugador con puntuación debe tener posición sugerida."
            )