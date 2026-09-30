from balanceador_equipos.balanceo.balanceador_equipos import (
    BalanceadorEquipos,
    DistribucionEquipos,
)
from balanceador_equipos.models.jugador import Jugador


class ServicioBalanceo:
    """
    Servicio de alto nivel para realizar el balanceo de equipos.

    Encapsula la lógica necesaria para solicitar una distribución
    equilibrada sin exponer directamente los detalles del algoritmo
    de balanceo a las capas superiores.
    """

    @staticmethod
    def balancear(
        jugadores: list[Jugador],
        tamano_equipo: int,
    ) -> DistribucionEquipos:
        """
        Balancea los jugadores seleccionados en dos equipos.

        Args:
            jugadores: Jugadores seleccionados para el partido.
            tamano_equipo: Cantidad de jugadores por equipo.

        Returns:
            Distribución equilibrada de los jugadores.
        """

        return BalanceadorEquipos.balancear(
            jugadores=jugadores,
            tamano_equipo=tamano_equipo,
        )