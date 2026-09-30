from balanceador_equipos.jugadores.actualizador_jugador import (
    ActualizadorJugador,
)
from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.persistencia import (
    guardar_jugador,
    obtener_jugador,
    obtener_jugadores,
)


class ServicioJugadores:
    """
    Servicio de alto nivel para gestionar los jugadores registrados.
    """

    @staticmethod
    def registrar(jugador: Jugador) -> Jugador:
        """
        Registra un nuevo jugador.

        Args:
            jugador: Jugador que se desea registrar.

        Returns:
            El mismo jugador con el ID asignado por la base de datos.
        """

        id_jugador = guardar_jugador(jugador)

        return Jugador(
            id=id_jugador,
            nombre=jugador.nombre,
            habilidades=jugador.habilidades,
            posicion_sugerida=jugador.posicion_sugerida,
            puntuacion=jugador.puntuacion,
        )

    @staticmethod
    def obtener_todos() -> list[Jugador]:
        """
        Obtiene todos los jugadores registrados.

        Returns:
            Lista de jugadores registrados.
        """

        return obtener_jugadores()

    @staticmethod
    def obtener_por_id(id_jugador: int) -> Jugador | None:
        """
        Obtiene un jugador por su ID.

        Args:
            id_jugador: ID del jugador buscado.

        Returns:
            El jugador, o None si no existe.
        """

        return obtener_jugador(id_jugador)

    @staticmethod
    def actualizar(
        jugador: Jugador,
        nombre: str,
        habilidades: Habilidades,
    ) -> Jugador:
        """
        Actualiza los datos de un jugador.

        Si cambian las habilidades, recalcula automáticamente
        su posición sugerida y puntuación.

        Si únicamente cambia el nombre, conserva los valores
        derivados existentes.

        Args:
            jugador: Jugador que se desea actualizar.
            nombre: Nuevo nombre.
            habilidades: Nuevas habilidades.

        Returns:
            Jugador actualizado.
        """

        return ActualizadorJugador.actualizar(
            jugador=jugador,
            nombre=nombre,
            habilidades=habilidades,
        )