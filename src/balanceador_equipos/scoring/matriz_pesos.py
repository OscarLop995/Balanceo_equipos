from dataclasses import fields
from math import isclose
from types import MappingProxyType
from typing import Final

from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.posicion import Posicion


MATRIZ_PESOS: Final = MappingProxyType({
    Posicion.PORTERO: MappingProxyType({
        "velocidad": 0.01,
        "aceleracion": 0.01,
        "resistencia": 0.01,
        "fuerza": 0.05,
        "agilidad": 0.01,
        "equilibrio": 0.03,
        "salto": 0.08,
        "potencia_tiro": 0.01,
        "precision_tiro": 0.01,
        "pase_corto": 0.03,
        "pase_largo": 0.03,
        "centros": 0.01,
        "control_balon": 0.03,
        "regate": 0.01,
        "vision_juego": 0.03,
        "toma_decisiones": 0.04,
        "marcaje": 0.01,
        "entradas": 0.01,
        "intercepciones": 0.01,
        "posicionamiento_defensivo": 0.03,
        "posicionamiento_ofensivo": 0.01,
        "desmarque": 0.01,
        "anticipacion": 0.05,
        "reflejos": 0.16,
        "estirada": 0.16,
        "juego_aereo": 0.08,
        "seguridad_balon": 0.07,
    }),

    Posicion.DEFENSA: MappingProxyType({
        "velocidad": 0.03,
        "aceleracion": 0.03,
        "resistencia": 0.05,
        "fuerza": 0.06,
        "agilidad": 0.03,
        "equilibrio": 0.03,
        "salto": 0.03,
        "potencia_tiro": 0.01,
        "precision_tiro": 0.01,
        "pase_corto": 0.04,
        "pase_largo": 0.05,
        "centros": 0.02,
        "control_balon": 0.03,
        "regate": 0.01,
        "vision_juego": 0.05,
        "toma_decisiones": 0.05,
        "marcaje": 0.08,
        "entradas": 0.07,
        "intercepciones": 0.07,
        "posicionamiento_defensivo": 0.09,
        "posicionamiento_ofensivo": 0.01,
        "desmarque": 0.01,
        "anticipacion": 0.06,
        "reflejos": 0.01,
        "estirada": 0.01,
        "juego_aereo": 0.04,
        "seguridad_balon": 0.02
    }),

    Posicion.MEDIOCAMPISTA: MappingProxyType({
        "velocidad": 0.04,
        "aceleracion": 0.04,
        "resistencia": 0.06,
        "fuerza": 0.03,
        "agilidad": 0.04,
        "equilibrio": 0.04,
        "salto": 0.01,
        "potencia_tiro": 0.03,
        "precision_tiro": 0.03,
        "pase_corto": 0.08,
        "pase_largo": 0.06,
        "centros": 0.03,
        "control_balon": 0.06,
        "regate": 0.04,
        "vision_juego": 0.07,
        "toma_decisiones": 0.06,
        "marcaje": 0.03,
        "entradas": 0.03,
        "intercepciones": 0.03,
        "posicionamiento_defensivo": 0.03,
        "posicionamiento_ofensivo": 0.03,
        "desmarque": 0.03,
        "anticipacion": 0.03,
        "reflejos": 0.01,
        "estirada": 0.01,
        "juego_aereo": 0.02,
        "seguridad_balon": 0.03,
    }),

    Posicion.EXTREMO: MappingProxyType({
        "velocidad": 0.09,
        "aceleracion": 0.09,
        "resistencia": 0.05,
        "fuerza": 0.02,
        "agilidad": 0.07,
        "equilibrio": 0.05,
        "salto": 0.02,
        "potencia_tiro": 0.04,
        "precision_tiro": 0.04,
        "pase_corto": 0.03,
        "pase_largo": 0.02,
        "centros": 0.05,
        "control_balon": 0.06,
        "regate": 0.07,
        "vision_juego": 0.04,
        "toma_decisiones": 0.04,
        "marcaje": 0.01,
        "entradas": 0.01,
        "intercepciones": 0.02,
        "posicionamiento_defensivo": 0.01,
        "posicionamiento_ofensivo": 0.03,
        "desmarque": 0.06,
        "anticipacion": 0.02,
        "reflejos": 0.01,
        "estirada": 0.01,
        "juego_aereo": 0.02,
        "seguridad_balon": 0.02,
    }),

    Posicion.DELANTERO: MappingProxyType({
        "velocidad": 0.05,
        "aceleracion": 0.07,
        "resistencia": 0.04,
        "fuerza": 0.05,
        "agilidad": 0.04,
        "equilibrio": 0.04,
        "salto": 0.04,
        "potencia_tiro": 0.07,
        "precision_tiro": 0.09,
        "pase_corto": 0.03,
        "pase_largo": 0.02,
        "centros": 0.02,
        "control_balon": 0.05,
        "regate": 0.05,
        "vision_juego": 0.03,
        "toma_decisiones": 0.04,
        "marcaje": 0.01,
        "entradas": 0.01,
        "intercepciones": 0.01,
        "posicionamiento_defensivo": 0.01,
        "posicionamiento_ofensivo": 0.04,
        "desmarque": 0.06,
        "anticipacion": 0.03,
        "reflejos": 0.01,
        "estirada": 0.01,
        "juego_aereo": 0.03,
        "seguridad_balon": 0.05,
    }),
})


def _validar_matriz_pesos() -> None:
    """
    Valida la estructura y consistencia de la matriz de pesos.
    """

    posiciones_esperadas = set(Posicion)
    posiciones_actuales = set(MATRIZ_PESOS)

    if posiciones_actuales != posiciones_esperadas:
        raise ValueError(
            "La matriz de pesos no contiene exactamente todas las posiciones."
        )

    habilidades_esperadas = {
        field.name for field in fields(Habilidades)
    }

    for posicion, pesos in MATRIZ_PESOS.items():
        habilidades_actuales = set(pesos)

        if habilidades_actuales != habilidades_esperadas:
            raise ValueError(
                f"La posición '{posicion.value}' no contiene exactamente "
                "las 27 habilidades definidas en Habilidades."
            )

        for habilidad, peso in pesos.items():
            if peso <= 0:
                raise ValueError(
                    f"El peso de '{habilidad}' para la posición "
                    f"'{posicion.value}' debe ser mayor que 0."
                )

        suma = sum(pesos.values())

        if not isclose(suma, 1.0, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(
                f"Los pesos de la posición '{posicion.value}' "
                f"deben sumar 1.0, pero suman {suma:.10f}."
            )


_validar_matriz_pesos()