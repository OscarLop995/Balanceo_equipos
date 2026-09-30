import pytest

from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion

from conftest import crear_habilidades


def test_habilidades_validas() -> None:
    habilidades = crear_habilidades(0, velocidad=100)

    assert habilidades.velocidad == 100
    assert habilidades.regate == 0


@pytest.mark.parametrize("valor", [-1, 101])
def test_habilidad_fuera_de_rango(valor: int) -> None:
    with pytest.raises(ValueError):
        crear_habilidades(velocidad=valor)


def test_habilidad_no_entera() -> None:
    with pytest.raises(TypeError):
        crear_habilidades(velocidad=50.5)  # type: ignore[arg-type]


@pytest.mark.parametrize("nombre", ["", "   ", " Ana", "Ana "])
def test_nombre_invalido(nombre: str) -> None:
    with pytest.raises(ValueError):
        Jugador(
            id=None,
            nombre=nombre,
            habilidades=crear_habilidades(),
            posicion_sugerida=None,
            puntuacion=None,
        )


def test_puntuacion_y_posicion_deben_ir_juntas() -> None:
    with pytest.raises(ValueError):
        Jugador(
            id=None,
            nombre="Ana",
            habilidades=crear_habilidades(),
            posicion_sugerida=Posicion.DEFENSA,
            puntuacion=None,
        )

    with pytest.raises(ValueError):
        Jugador(
            id=None,
            nombre="Ana",
            habilidades=crear_habilidades(),
            posicion_sugerida=None,
            puntuacion=50.0,
        )


@pytest.mark.parametrize("puntuacion", [-0.1, 100.1])
def test_puntuacion_fuera_de_rango(puntuacion: float) -> None:
    with pytest.raises(ValueError):
        Jugador(
            id=None,
            nombre="Ana",
            habilidades=crear_habilidades(),
            posicion_sugerida=Posicion.DEFENSA,
            puntuacion=puntuacion,
        )
