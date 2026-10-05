import time
from collections.abc import Iterator
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

import pytest

jwt = pytest.importorskip("jwt")
rsa = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.rsa")

from fastapi.testclient import TestClient  # noqa: E402

from balanceador_equipos.backend.cloudflare_access import (  # noqa: E402
    VARIABLE_AUDIENCIA,
    VARIABLE_DESACTIVAR,
    VARIABLE_DOMINIO_EQUIPO,
)
from balanceador_equipos.backend.produccion import (  # noqa: E402
    VARIABLE_FRONTEND,
    crear_aplicacion,
)

from conftest import crear_habilidades  # noqa: E402

DOMINIO = "equipo-prueba.cloudflareaccess.com"
AUDIENCIA = "aud-de-prueba"
INDICE = "<!doctype html><title>app</title>"

CLAVE_PRIVADA = rsa.generate_private_key(public_exponent=65537, key_size=2048)
OTRA_CLAVE_PRIVADA = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)


def crear_token(
    audiencia: str = AUDIENCIA,
    emisor: str = f"https://{DOMINIO}",
    expira_en: int = 300,
    clave=CLAVE_PRIVADA,
) -> str:
    ahora = int(time.time())

    return jwt.encode(
        {
            "aud": [audiencia],
            "iss": emisor,
            "iat": ahora,
            "exp": ahora + expira_en,
            "email": "usuario@example.com",
        },
        clave,
        algorithm="RS256",
    )


@pytest.fixture
def frontend(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text(INDICE, encoding="utf-8")
    (dist / "assets" / "app.js").write_text("console.log(1)", encoding="utf-8")
    (dist / "balon.svg").write_text("<svg/>", encoding="utf-8")
    (tmp_path / "secreto.txt").write_text("NO DEBE VERSE", encoding="utf-8")

    monkeypatch.setenv(VARIABLE_FRONTEND, str(dist))

    return dist


@pytest.fixture
def access_configurado(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(VARIABLE_DOMINIO_EQUIPO, DOMINIO)
    monkeypatch.setenv(VARIABLE_AUDIENCIA, AUDIENCIA)
    monkeypatch.delenv(VARIABLE_DESACTIVAR, raising=False)

    # Evita descargar las claves de Cloudflare: se usa la clave del test.
    monkeypatch.setattr(
        jwt.PyJWKClient,
        "get_signing_key_from_jwt",
        lambda self, token: SimpleNamespace(key=CLAVE_PRIVADA.public_key()),
    )


@pytest.fixture
def cliente(frontend: Path, access_configurado: None) -> Iterator[TestClient]:
    with TestClient(crear_aplicacion()) as cliente:
        yield cliente


def _con_token(token: str | None = None) -> dict[str, str]:
    return {"Cf-Access-Jwt-Assertion": token or crear_token()}


# ---------- Cloudflare Access ----------


def test_sin_configuracion_rechaza_todo(
    frontend: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(VARIABLE_DOMINIO_EQUIPO, raising=False)
    monkeypatch.delenv(VARIABLE_AUDIENCIA, raising=False)
    monkeypatch.delenv(VARIABLE_DESACTIVAR, raising=False)

    with TestClient(crear_aplicacion()) as cliente:
        assert cliente.get("/").status_code == 503
        assert cliente.get("/api/jugadores").status_code == 503


def test_desactivado_explicitamente_permite_el_acceso(
    frontend: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(VARIABLE_DESACTIVAR, "1")

    with TestClient(crear_aplicacion()) as cliente:
        assert cliente.get("/").status_code == 200
        assert cliente.get("/api/jugadores").status_code == 200


def test_sin_token_da_403(cliente: TestClient) -> None:
    assert cliente.get("/").status_code == 403
    assert cliente.get("/api/jugadores").status_code == 403


def test_token_valido_en_cabecera(cliente: TestClient) -> None:
    assert cliente.get("/", headers=_con_token()).status_code == 200
    assert cliente.get("/api/jugadores", headers=_con_token()).status_code == 200


def test_token_valido_en_cookie(cliente: TestClient) -> None:
    respuesta = cliente.get(
        "/",
        headers={"Cookie": f"otra=1; CF_Authorization={crear_token()}"},
    )

    assert respuesta.status_code == 200


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(crear_token(audiencia="otra-app"), id="audiencia"),
        pytest.param(crear_token(emisor="https://otro.cloudflareaccess.com"), id="emisor"),
        pytest.param(crear_token(expira_en=-60), id="expirado"),
        pytest.param(crear_token(clave=OTRA_CLAVE_PRIVADA), id="firma"),
        pytest.param("no-es-un-jwt", id="malformado"),
    ],
)
def test_token_invalido_da_403(cliente: TestClient, token: str) -> None:
    assert cliente.get("/", headers=_con_token(token)).status_code == 403


@pytest.mark.parametrize(
    ("dominio", "audiencia"),
    [
        (f"https://{DOMINIO}/", AUDIENCIA),
        (f"  {DOMINIO.upper()}  ", f" {AUDIENCIA} "),
        (f'"{DOMINIO}"', f"'{AUDIENCIA}'"),
    ],
)
def test_tolera_errores_de_formato_en_las_variables(
    frontend: Path,
    access_configurado: None,
    monkeypatch: pytest.MonkeyPatch,
    dominio: str,
    audiencia: str,
) -> None:
    monkeypatch.setenv(VARIABLE_DOMINIO_EQUIPO, dominio)
    monkeypatch.setenv(VARIABLE_AUDIENCIA, audiencia)

    with TestClient(crear_aplicacion()) as cliente:
        assert cliente.get("/", headers=_con_token()).status_code == 200


def test_el_log_explica_la_discrepancia(
    cliente: TestClient,
    caplog: pytest.LogCaptureFixture,
) -> None:
    token = crear_token(audiencia="a" * 64)

    with caplog.at_level("WARNING"):
        respuesta = cliente.get("/", headers=_con_token(token))

    assert respuesta.status_code == 403
    assert "InvalidAudienceError" in caplog.text
    assert "aaaaaa…aaaa (64 caracteres)" in caplog.text
    assert "audiencia esperada=aud-de…ueba (13 caracteres)" in caplog.text
    assert f"emisor esperado='https://{DOMINIO}'" in caplog.text
    # El AUD completo nunca se escribe en el log.
    assert "a" * 64 not in caplog.text


# ---------- Servicio de la web y la API ----------


def test_api_montada_bajo_api(cliente: TestClient) -> None:
    datos = {"nombre": "Ana", "habilidades": asdict(crear_habilidades())}

    creado = cliente.post("/api/jugadores", json=datos, headers=_con_token())
    listado = cliente.get("/api/jugadores", headers=_con_token())

    assert creado.status_code == 200
    assert [j["nombre"] for j in listado.json()] == ["Ana"]


def test_documentacion_de_la_api_no_se_publica(cliente: TestClient) -> None:
    # Sin docs en la raíz: "/docs" es una ruta más de React.
    respuesta = cliente.get("/docs", headers=_con_token())

    assert respuesta.text == INDICE


@pytest.mark.parametrize(
    "ruta",
    ["/", "/partidos/nuevo", "/jugadores/3/editar", "/ruta/inexistente"],
)
def test_rutas_de_react_devuelven_index(cliente: TestClient, ruta: str) -> None:
    respuesta = cliente.get(ruta, headers=_con_token())

    assert respuesta.status_code == 200
    assert respuesta.text == INDICE
    assert respuesta.headers["cache-control"] == "no-cache"


def test_sirve_archivos_estaticos(cliente: TestClient) -> None:
    assert cliente.get("/assets/app.js", headers=_con_token()).text == "console.log(1)"
    assert cliente.get("/balon.svg", headers=_con_token()).text == "<svg/>"


def test_recurso_inexistente_da_404(cliente: TestClient) -> None:
    assert cliente.get("/assets/nope.js", headers=_con_token()).status_code == 404


@pytest.mark.parametrize(
    "ruta",
    ["/..%2Fsecreto.txt", "/%2E%2E/secreto.txt", "/assets/..%2F..%2Fsecreto.txt"],
)
def test_no_permite_salir_de_la_carpeta_del_frontend(
    cliente: TestClient,
    ruta: str,
) -> None:
    respuesta = cliente.get(ruta, headers=_con_token())

    assert "NO DEBE VERSE" not in respuesta.text


def test_frontend_no_compilado_da_503(
    tmp_path: Path,
    access_configurado: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(VARIABLE_FRONTEND, str(tmp_path / "no-existe"))

    with TestClient(crear_aplicacion()) as cliente:
        assert cliente.get("/", headers=_con_token()).status_code == 503
