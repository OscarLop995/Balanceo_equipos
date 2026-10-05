"""
Verificación de Cloudflare Access.

Cloudflare Access solo protege el tráfico que pasa por Cloudflare. Como la
aplicación también es alcanzable directamente en Railway, cada petición
debe traer el JWT firmado que Access añade en la cabecera
Cf-Access-Jwt-Assertion. Sin un token válido, la petición se rechaza.

Documentación: https://developers.cloudflare.com/cloudflare-one/identity/authorization-cookie/validating-json/
"""

import logging
import os
from dataclasses import dataclass

import jwt
from starlette.concurrency import run_in_threadpool
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

logger = logging.getLogger(__name__)

CABECERA_TOKEN = "cf-access-jwt-assertion"
COOKIE_TOKEN = "CF_Authorization"

VARIABLE_DOMINIO_EQUIPO = "CF_ACCESS_TEAM_DOMAIN"
VARIABLE_AUDIENCIA = "CF_ACCESS_AUD"
VARIABLE_DESACTIVAR = "BALANCEADOR_SIN_CLOUDFLARE_ACCESS"


@dataclass(frozen=True)
class ConfiguracionAccess:
    dominio_equipo: str
    audiencia: str

    @property
    def emisor(self) -> str:
        return f"https://{self.dominio_equipo}"

    @property
    def url_certificados(self) -> str:
        return f"{self.emisor}/cdn-cgi/access/certs"


def leer_configuracion() -> ConfiguracionAccess | None:
    """
    Lee la configuración desde variables de entorno.

    Retorna None si falta alguna variable.
    """

    # Tolera errores comunes al copiar valores: espacios, comillas,
    # mayúsculas, el esquema https:// y la barra final.
    dominio = _limpiar(os.environ.get(VARIABLE_DOMINIO_EQUIPO, "")).lower()
    audiencia = _limpiar(os.environ.get(VARIABLE_AUDIENCIA, ""))

    if not dominio or not audiencia:
        return None

    dominio = dominio.removeprefix("https://").removeprefix("http://")
    dominio = dominio.rstrip("/")

    return ConfiguracionAccess(dominio_equipo=dominio, audiencia=audiencia)


def _limpiar(valor: str) -> str:
    return valor.strip().strip("\"'").strip()


def _abreviar(valor: object) -> str:
    """Muestra solo el inicio y el final de un valor largo."""

    texto = str(valor)

    if len(texto) <= 12:
        return texto

    return f"{texto[:6]}…{texto[-4:]} ({len(texto)} caracteres)"


def describir_discrepancia(
    token: str,
    configuracion: ConfiguracionAccess,
) -> str:
    """
    Compara, sin verificar la firma, el emisor y la audiencia del token con
    la configuración. Solo para diagnóstico en los logs.
    """

    try:
        datos = jwt.decode(token, options={"verify_signature": False})
    except jwt.PyJWTError:
        return "token ilegible"

    audiencias = datos.get("aud")

    if isinstance(audiencias, str):
        audiencias = [audiencias]

    return (
        f"emisor del token={datos.get('iss')!r}, "
        f"emisor esperado={configuracion.emisor!r}; "
        f"audiencia del token={[_abreviar(a) for a in audiencias or []]}, "
        f"audiencia esperada={_abreviar(configuracion.audiencia)}"
    )


class VerificadorAccess:
    """
    Valida tokens de Cloudflare Access con las claves públicas del equipo.
    """

    def __init__(self, configuracion: ConfiguracionAccess) -> None:
        self.configuracion = configuracion
        # PyJWKClient cachea las claves y las renueva cuando rotan.
        self._cliente_claves = jwt.PyJWKClient(
            configuracion.url_certificados,
            cache_keys=True,
        )

    def verificar(self, token: str) -> dict:
        clave = self._cliente_claves.get_signing_key_from_jwt(token)

        return jwt.decode(
            token,
            clave.key,
            algorithms=["RS256"],
            audience=self.configuracion.audiencia,
            issuer=self.configuracion.emisor,
        )


def _extraer_token(scope: Scope) -> str | None:
    cabeceras = {
        nombre.decode("latin-1").lower(): valor.decode("latin-1")
        for nombre, valor in scope.get("headers", [])
    }

    token = cabeceras.get(CABECERA_TOKEN)

    if token:
        return token

    for fragmento in cabeceras.get("cookie", "").split(";"):
        nombre, _, valor = fragmento.strip().partition("=")

        if nombre == COOKIE_TOKEN and valor:
            return valor

    return None


class MiddlewareCloudflareAccess:
    """
    Rechaza toda petición HTTP sin un token válido de Cloudflare Access.

    Falla de forma segura: si no hay configuración, responde 503 salvo que
    se desactive explícitamente con BALANCEADOR_SIN_CLOUDFLARE_ACCESS=1.
    """

    def __init__(
        self,
        app: ASGIApp,
        verificador: VerificadorAccess | None = None,
    ) -> None:
        self.app = app
        self.desactivado = os.environ.get(VARIABLE_DESACTIVAR) == "1"

        if verificador is None and not self.desactivado:
            configuracion = leer_configuracion()

            if configuracion is not None:
                verificador = VerificadorAccess(configuracion)

        self.verificador = verificador

        if self.desactivado:
            logger.warning(
                "Cloudflare Access DESACTIVADO: la aplicación es pública."
            )
        elif self.verificador is None:
            logger.error(
                "Faltan %s y/o %s: se rechazarán todas las peticiones.",
                VARIABLE_DOMINIO_EQUIPO,
                VARIABLE_AUDIENCIA,
            )

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http" or self.desactivado:
            await self.app(scope, receive, send)
            return

        if self.verificador is None:
            respuesta = PlainTextResponse(
                "Cloudflare Access no está configurado en el servidor.",
                status_code=503,
            )
            await respuesta(scope, receive, send)
            return

        token = _extraer_token(scope)

        if token is None:
            await PlainTextResponse("Acceso denegado.", status_code=403)(
                scope, receive, send
            )
            return

        try:
            # La primera vez descarga las claves públicas (E/S bloqueante).
            await run_in_threadpool(self.verificador.verificar, token)
        except jwt.PyJWTError as error:
            # WARNING para que aparezca en los logs de Railway: uvicorn no
            # configura un handler para los loggers de la aplicación.
            logger.warning(
                "Token de Cloudflare Access rechazado (%s): %s | %s",
                type(error).__name__,
                error,
                describir_discrepancia(token, self.verificador.configuracion),
            )
            await PlainTextResponse("Acceso denegado.", status_code=403)(
                scope, receive, send
            )
            return

        await self.app(scope, receive, send)
