from dataclasses import dataclass

from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion


@dataclass(frozen=True)
class EvaluacionEquipo:
    """
    Representa los resultados de evaluación de un equipo.
    """

    puntuacion_total: float
    cantidad_porteros: int


class EvaluadorEquipo:
    """
    Evalúa las características relevantes de un equipo
    para el proceso de balanceo.
    """

    @staticmethod
    def evaluar(jugadores: list[Jugador]) -> EvaluacionEquipo:
        """
        Calcula la puntuación total y cantidad de porteros de un equipo.

        Args:
            jugadores: Jugadores que conforman el equipo.

        Returns:
            Evaluación del equipo.
        """

        puntuacion_total = 0.0
        cantidad_porteros = 0

        for jugador in jugadores:
            if jugador.puntuacion is None:
                raise ValueError(
                    f"El jugador '{jugador.nombre}' "
                    "no tiene una puntuación calculada."
                )

            puntuacion_total += jugador.puntuacion

            if jugador.posicion_sugerida == Posicion.PORTERO:
                cantidad_porteros += 1

        return EvaluacionEquipo(
            puntuacion_total=puntuacion_total,
            cantidad_porteros=cantidad_porteros,
        )