from balanceador_equipos.models.posicion import Posicion


class DeterminadorPosicion:
    """
    Determina la posición sugerida a partir de las
    puntuaciones calculadas para cada posición.
    """

    @staticmethod
    def determinar(
        puntuaciones: dict[Posicion, float],
    ) -> Posicion:
        """
        Retorna la posición con mayor puntuación.

        Args:
            puntuaciones: Puntuación del jugador para cada posición.

        Returns:
            La posición con mayor puntuación.
        """

        return max(
            puntuaciones,
            key=lambda posicion: puntuaciones[posicion],
        )