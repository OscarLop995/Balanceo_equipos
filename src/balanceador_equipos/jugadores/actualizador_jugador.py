from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.persistencia import actualizar_jugador
from balanceador_equipos.scoring.perfilador_jugador import (
    PerfiladorJugador,
)


class ActualizadorJugador:
    """
    Gestiona la actualización de un jugador y determina si es necesario
    recalcular su posición sugerida y puntuación.
    """

    @staticmethod
    def actualizar(
        jugador: Jugador,
        nombre: str,
        habilidades: Habilidades,
    ) -> Jugador:
        """
        Actualiza un jugador.

        Si las habilidades cambiaron, recalcula la posición sugerida
        y la puntuación. Si únicamente cambió el nombre, conserva
        los valores calculados anteriormente.

        Args:
            jugador: Jugador existente.
            nombre: Nuevo nombre del jugador.
            habilidades: Nuevas habilidades del jugador.

        Returns:
            Jugador actualizado.
        """

        habilidades_cambiaron = (
            jugador.habilidades != habilidades
        )

        jugador_actualizado = Jugador(
            id=jugador.id,
            nombre=nombre,
            habilidades=habilidades,
            posicion_sugerida=jugador.posicion_sugerida,
            puntuacion=jugador.puntuacion,
        )

        if habilidades_cambiaron:
            jugador_actualizado = PerfiladorJugador.calcular(
                jugador_actualizado
            )

        actualizar_jugador(jugador_actualizado)

        return jugador_actualizado