from collections.abc import Iterator
from dataclasses import asdict

import pytest
from fastapi.testclient import TestClient

from balanceador_equipos.backend.main import app

from conftest import crear_habilidades


@pytest.fixture
def cliente() -> Iterator[TestClient]:
    with TestClient(app) as cliente:
        yield cliente


def _datos_jugador(nombre: str, valor: int = 50) -> dict:
    return {
        "nombre": nombre,
        "habilidades": asdict(crear_habilidades(valor)),
    }


def _crear_jugadores(cliente: TestClient, cantidad: int) -> list[int]:
    ids = []

    for i in range(cantidad):
        respuesta = cliente.post(
            "/jugadores",
            json=_datos_jugador(f"Jugador {i}", 40 + i),
        )
        assert respuesta.status_code == 200
        ids.append(respuesta.json()["id"])

    return ids


def test_inicio(cliente: TestClient) -> None:
    assert cliente.get("/").status_code == 200


def test_crear_y_listar_jugador(cliente: TestClient) -> None:
    respuesta = cliente.post("/jugadores", json=_datos_jugador("Ana"))

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["nombre"] == "Ana"
    assert cuerpo["puntuacion"] == pytest.approx(50.0)

    listado = cliente.get("/jugadores").json()
    assert [j["id"] for j in listado] == [cuerpo["id"]]


@pytest.mark.parametrize("nombre", ["", " Ana"])
def test_crear_jugador_con_nombre_invalido_da_422(
    cliente: TestClient,
    nombre: str,
) -> None:
    respuesta = cliente.post("/jugadores", json=_datos_jugador(nombre))

    assert respuesta.status_code == 422


def test_crear_jugador_con_habilidad_fuera_de_rango(
    cliente: TestClient,
) -> None:
    datos = _datos_jugador("Ana")
    datos["habilidades"]["velocidad"] = 150

    assert cliente.post("/jugadores", json=datos).status_code == 422


def test_actualizar_jugador(cliente: TestClient) -> None:
    id_jugador = _crear_jugadores(cliente, 1)[0]

    respuesta = cliente.put(
        f"/jugadores/{id_jugador}",
        json=_datos_jugador("Renombrado", 70),
    )

    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Renombrado"
    assert respuesta.json()["puntuacion"] == pytest.approx(70.0)


def test_actualizar_jugador_inexistente_da_404(cliente: TestClient) -> None:
    respuesta = cliente.put("/jugadores/999", json=_datos_jugador("X"))

    assert respuesta.status_code == 404


def test_actualizar_con_nombre_invalido_da_422(cliente: TestClient) -> None:
    id_jugador = _crear_jugadores(cliente, 1)[0]

    respuesta = cliente.put(
        f"/jugadores/{id_jugador}",
        json=_datos_jugador("Ana "),
    )

    assert respuesta.status_code == 422


def test_balancear_partido(cliente: TestClient) -> None:
    ids = _crear_jugadores(cliente, 16)

    respuesta = cliente.post(
        "/partidos/balancear",
        json={"jugadores": ids, "tamano_equipo": 8},
    )

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    ids_a = {j["id"] for j in cuerpo["equipo_a"]["jugadores"]}
    ids_b = {j["id"] for j in cuerpo["equipo_b"]["jugadores"]}
    assert len(ids_a) == len(ids_b) == 8
    assert ids_a | ids_b == set(ids)


def test_balancear_con_ids_repetidos_da_422(cliente: TestClient) -> None:
    ids = _crear_jugadores(cliente, 15)

    respuesta = cliente.post(
        "/partidos/balancear",
        json={"jugadores": ids + [ids[0]], "tamano_equipo": 8},
    )

    assert respuesta.status_code == 422


def test_balancear_con_cantidad_incorrecta_da_400(
    cliente: TestClient,
) -> None:
    ids = _crear_jugadores(cliente, 18)

    respuesta = cliente.post(
        "/partidos/balancear",
        json={"jugadores": ids, "tamano_equipo": 8},
    )

    assert respuesta.status_code == 400


def test_balancear_con_jugador_inexistente_da_404(
    cliente: TestClient,
) -> None:
    ids = _crear_jugadores(cliente, 15)

    respuesta = cliente.post(
        "/partidos/balancear",
        json={"jugadores": ids + [9999], "tamano_equipo": 8},
    )

    assert respuesta.status_code == 404
