from dataclasses import dataclass
from itertools import combinations

from balanceador_equipos.balanceo.evaluador_equipo import (
    EvaluadorEquipo,
)
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion


TAMANOS_EQUIPO_VALIDOS = {8, 9, 10}


@dataclass(frozen=True)
class DistribucionEquipos:
    """
    Representa una distribución de jugadores en dos equipos.
    """

    equipo_a: tuple[Jugador, ...]
    equipo_b: tuple[Jugador, ...]
    puntuacion_equipo_a: float
    puntuacion_equipo_b: float
    diferencia_puntuacion: float


class BalanceadorEquipos:
    """
    Encuentra la distribución de jugadores que minimiza la diferencia
    de puntuación entre dos equipos, respetando la regla de porteros.
    """

    @staticmethod
    def balancear(
        jugadores: list[Jugador],
        tamano_equipo: int,
    ) -> DistribucionEquipos:
        """
        Busca exhaustivamente la mejor distribución posible.

        Args:
            jugadores: Jugadores seleccionados para el partido.
            tamano_equipo: Cantidad de jugadores por equipo.

        Returns:
            La distribución con menor diferencia de puntuación.

        Raises:
            ValueError: Si los datos de entrada no son válidos.
            RuntimeError: Si no es posible encontrar una distribución.
        """

        BalanceadorEquipos._validar_entrada(
            jugadores,
            tamano_equipo,
        )

        distribuciones = BalanceadorEquipos._generar_distribuciones(
            jugadores,
            tamano_equipo,
        )

        return BalanceadorEquipos._seleccionar_mejor_distribucion(
            distribuciones
        )

    @staticmethod
    def _generar_distribuciones(
        jugadores: list[Jugador],
        tamano_equipo: int,
    ) -> list[DistribucionEquipos]:
        """
        Genera todas las distribuciones válidas de los jugadores.

        Para evitar evaluar dos veces la misma distribución con los
        equipos invertidos, el primer jugador siempre pertenece
        al Equipo A.
        """

        cantidad_porteros_total = sum(
            jugador.posicion_sugerida == Posicion.PORTERO
            for jugador in jugadores
        )

        indices_restantes = range(1, len(jugadores))

        distribuciones: list[DistribucionEquipos] = []

        # Se trabaja con índices y no con igualdad entre jugadores para
        # que el Equipo B sea siempre el complemento exacto del Equipo A.
        for indices_complementarios in combinations(
            indices_restantes,
            tamano_equipo - 1,
        ):
            indices_a = {0, *indices_complementarios}

            equipo_a = tuple(
                jugadores[indice]
                for indice in sorted(indices_a)
            )

            equipo_b = tuple(
                jugador
                for indice, jugador in enumerate(jugadores)
                if indice not in indices_a
            )

            evaluacion_a = EvaluadorEquipo.evaluar(
                list(equipo_a)
            )

            evaluacion_b = EvaluadorEquipo.evaluar(
                list(equipo_b)
            )

            if not BalanceadorEquipos._distribucion_valida(
                cantidad_porteros_a=evaluacion_a.cantidad_porteros,
                cantidad_porteros_b=evaluacion_b.cantidad_porteros,
                cantidad_porteros_total=cantidad_porteros_total,
            ):
                continue

            diferencia = abs(
                evaluacion_a.puntuacion_total
                - evaluacion_b.puntuacion_total
            )

            distribuciones.append(
                DistribucionEquipos(
                    equipo_a=equipo_a,
                    equipo_b=equipo_b,
                    puntuacion_equipo_a=(
                        evaluacion_a.puntuacion_total
                    ),
                    puntuacion_equipo_b=(
                        evaluacion_b.puntuacion_total
                    ),
                    diferencia_puntuacion=diferencia,
                )
            )

        return distribuciones

    @staticmethod
    def _seleccionar_mejor_distribucion(
        distribuciones: list[DistribucionEquipos],
    ) -> DistribucionEquipos:
        """
        Selecciona la distribución con menor diferencia de puntuación.
        """

        if not distribuciones:
            raise RuntimeError(
                "No fue posible encontrar una distribución válida."
            )

        return min(
            distribuciones,
            key=lambda distribucion: (
                distribucion.diferencia_puntuacion
            ),
        )

    @staticmethod
    def _distribucion_valida(
        cantidad_porteros_a: int,
        cantidad_porteros_b: int,
        cantidad_porteros_total: int,
    ) -> bool:
        """
        Determina si una distribución cumple la regla de porteros.

        Con cero o un portero seleccionado no existe restricción.

        Con dos o más porteros, ambos equipos deben tener al menos
        un portero.
        """

        if cantidad_porteros_total < 2:
            return True

        return (
            cantidad_porteros_a >= 1
            and cantidad_porteros_b >= 1
        )

    @staticmethod
    def _validar_entrada(
        jugadores: list[Jugador],
        tamano_equipo: int,
    ) -> None:
        """
        Valida las condiciones necesarias para realizar el balanceo.
        """

        if tamano_equipo not in TAMANOS_EQUIPO_VALIDOS:
            raise ValueError(
                "El tamaño del equipo debe ser 8, 9 o 10."
            )

        cantidad_esperada = tamano_equipo * 2

        if len(jugadores) != cantidad_esperada:
            raise ValueError(
                f"Para equipos de {tamano_equipo} jugadores se "
                f"requieren exactamente {cantidad_esperada} jugadores."
            )

        ids_vistos: set[int] = set()

        for jugador in jugadores:
            if jugador.id is None:
                continue

            if jugador.id in ids_vistos:
                raise ValueError(
                    f"El jugador '{jugador.nombre}' "
                    "está seleccionado más de una vez."
                )

            ids_vistos.add(jugador.id)

        for jugador in jugadores:
            if jugador.posicion_sugerida is None:
                raise ValueError(
                    f"El jugador '{jugador.nombre}' "
                    "no tiene una posición sugerida."
                )

            if jugador.puntuacion is None:
                raise ValueError(
                    f"El jugador '{jugador.nombre}' "
                    "no tiene una puntuación calculada."
                )