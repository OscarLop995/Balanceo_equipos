from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Habilidades:
    MIN_VALOR: ClassVar[int] = 0
    MAX_VALOR: ClassVar[int] = 100

    velocidad: int
    aceleracion: int
    resistencia: int
    fuerza: int
    agilidad: int
    equilibrio: int
    salto: int
    potencia_tiro: int
    precision_tiro: int
    pase_corto: int
    pase_largo: int
    centros: int
    control_balon: int
    regate: int
    vision_juego: int
    toma_decisiones: int
    marcaje: int
    entradas: int
    intercepciones: int
    posicionamiento_defensivo: int
    posicionamiento_ofensivo: int
    desmarque: int
    anticipacion: int
    reflejos: int
    estirada: int
    juego_aereo: int
    seguridad_balon: int

    def __post_init__(self) -> None:
        for nombre, valor in self.__dict__.items():
            if not isinstance(valor, int):
                raise TypeError(
                    f"La habilidad '{nombre}' debe ser un entero."
                )

            if not self.MIN_VALOR <= valor <= self.MAX_VALOR:
                raise ValueError(
                    f"La habilidad '{nombre}' debe estar entre "
                    f"{self.MIN_VALOR} y {self.MAX_VALOR}."
                )