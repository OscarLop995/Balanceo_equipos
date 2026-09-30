from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.scoring.calculador_puntuacion import (
    CalculadorPuntuacion,
)
from balanceador_equipos.scoring.determinador_posicion import (
    DeterminadorPosicion,
)


class PerfiladorJugador:
    """
    Calcula y completa la información derivada de un jugador:
    posición sugerida y puntuación general.
    """

    @staticmethod
    def calcular(jugador: Jugador) -> Jugador:
        """
        Calcula la posición sugerida y la puntuación del jugador
        a partir de sus habilidades.

        Args:
            jugador: Jugador cuyo perfil se desea calcular.

        Returns:
            Un nuevo Jugador con posición sugerida y puntuación calculadas.
        """

        puntuaciones = CalculadorPuntuacion.calcular(jugador)

        posicion_sugerida = DeterminadorPosicion.determinar(
            puntuaciones
        )

        puntuacion = puntuaciones[posicion_sugerida]

        return Jugador(
            id=jugador.id,
            nombre=jugador.nombre,
            habilidades=jugador.habilidades,
            posicion_sugerida=posicion_sugerida,
            puntuacion=puntuacion,
        )