from typing import Final

from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion
from balanceador_equipos.scoring.matriz_pesos import MATRIZ_PESOS


PUNTUACION_MINIMA: Final = 0.0
PUNTUACION_MAXIMA: Final = 100.0


class CalculadorPuntuacion:
    """
    Calcula la puntuación de un jugador para cada posición
    utilizando la matriz de pesos definida para cada posición.
    """

    @staticmethod
    def calcular(jugador: Jugador) -> dict[Posicion, float]:
        """
        Calcula la puntuación del jugador para todas las posiciones.

        Args:
            jugador: Jugador cuya puntuación se desea calcular.

        Returns:
            Diccionario con la puntuación del jugador para cada posición.
        """

        return {
            posicion: CalculadorPuntuacion._calcular_para_posicion(
                jugador.habilidades,
                posicion,
            )
            for posicion in Posicion
        }

    @staticmethod
    def _calcular_para_posicion(
        habilidades: Habilidades,
        posicion: Posicion,
    ) -> float:
        """
        Calcula la puntuación ponderada para una posición específica.
        """

        pesos = MATRIZ_PESOS[posicion]

        puntuacion = sum(
            getattr(habilidades, habilidad) * peso
            for habilidad, peso in pesos.items()
        )

        return max(
            PUNTUACION_MINIMA,
            min(PUNTUACION_MAXIMA, puntuacion),
        )