import os
import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from dataclasses import astuple, fields
from pathlib import Path

from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.models.posicion import Posicion


VARIABLE_ENTORNO_BASE_DATOS = "BALANCEADOR_DB"

# La ruta se resuelve desde la raíz del proyecto y no desde el directorio
# de trabajo, para que la GUI y la API usen siempre la misma base de datos.
RUTA_BASE_DATOS_POR_DEFECTO = (
    Path(__file__).resolve().parents[2] / "data" / "jugadores.db"
)

# Los nombres de columna provienen de los campos de Habilidades, que son
# identificadores fijos del código; nunca de datos del usuario.
COLUMNAS_HABILIDADES: tuple[str, ...] = tuple(
    campo.name for campo in fields(Habilidades)
)

COLUMNAS_JUGADOR: tuple[str, ...] = (
    "nombre",
    *COLUMNAS_HABILIDADES,
    "posicion_sugerida",
    "puntuacion",
)


def obtener_ruta_base_datos() -> Path:
    """
    Retorna la ruta de la base de datos.

    Puede sobrescribirse con la variable de entorno BALANCEADOR_DB.
    """

    ruta = os.environ.get(VARIABLE_ENTORNO_BASE_DATOS)

    if ruta:
        return Path(ruta)

    return RUTA_BASE_DATOS_POR_DEFECTO


@contextmanager
def _conectar() -> Iterator[sqlite3.Connection]:
    """
    Abre una conexión, confirma la transacción al terminar
    (o la revierte ante un error) y cierra siempre la conexión.
    """

    with closing(sqlite3.connect(obtener_ruta_base_datos())) as conexion:
        conexion.row_factory = sqlite3.Row

        with conexion:
            yield conexion


def inicializar_base_datos() -> None:
    """
    Crea la base de datos y la tabla de jugadores si no existen.
    """

    obtener_ruta_base_datos().parent.mkdir(parents=True, exist_ok=True)

    columnas_habilidades = ",\n".join(
        f"{columna} INTEGER NOT NULL"
        for columna in COLUMNAS_HABILIDADES
    )

    with _conectar() as conexion:
        conexion.execute(
            f"""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                {columnas_habilidades},
                posicion_sugerida TEXT NOT NULL,
                puntuacion REAL NOT NULL
            )
            """
        )


def _validar_datos_derivados(jugador: Jugador, accion: str) -> None:
    if jugador.posicion_sugerida is None:
        raise ValueError(
            f"No se puede {accion} un jugador sin posición sugerida."
        )

    if jugador.puntuacion is None:
        raise ValueError(
            f"No se puede {accion} un jugador sin puntuación."
        )


def _valores_jugador(jugador: Jugador) -> tuple[object, ...]:
    """
    Retorna los valores del jugador en el orden de COLUMNAS_JUGADOR.
    """

    assert jugador.posicion_sugerida is not None

    return (
        jugador.nombre,
        *astuple(jugador.habilidades),
        jugador.posicion_sugerida.value,
        jugador.puntuacion,
    )


def _fila_a_jugador(fila: sqlite3.Row) -> Jugador:
    return Jugador(
        id=fila["id"],
        nombre=fila["nombre"],
        habilidades=Habilidades(
            **{
                columna: fila[columna]
                for columna in COLUMNAS_HABILIDADES
            }
        ),
        posicion_sugerida=Posicion(fila["posicion_sugerida"]),
        puntuacion=fila["puntuacion"],
    )


def guardar_jugador(jugador: Jugador) -> int:
    """
    Guarda un jugador y retorna el ID asignado por la base de datos.
    """

    _validar_datos_derivados(jugador, "guardar")

    columnas = ", ".join(COLUMNAS_JUGADOR)
    marcadores = ", ".join("?" for _ in COLUMNAS_JUGADOR)

    with _conectar() as conexion:
        cursor = conexion.execute(
            f"INSERT INTO jugadores ({columnas}) VALUES ({marcadores})",
            _valores_jugador(jugador),
        )

        id_jugador = cursor.lastrowid

    if id_jugador is None:
        raise RuntimeError(
            "No fue posible obtener el ID del jugador guardado."
        )

    return id_jugador


def obtener_jugadores() -> list[Jugador]:
    """
    Obtiene todos los jugadores registrados en la base de datos.
    """

    columnas = ", ".join(("id", *COLUMNAS_JUGADOR))

    with _conectar() as conexion:
        filas = conexion.execute(
            f"SELECT {columnas} FROM jugadores ORDER BY id"
        ).fetchall()

    return [_fila_a_jugador(fila) for fila in filas]


def obtener_jugador(id_jugador: int) -> Jugador | None:
    """
    Obtiene un jugador por su ID, o None si no existe.
    """

    columnas = ", ".join(("id", *COLUMNAS_JUGADOR))

    with _conectar() as conexion:
        fila = conexion.execute(
            f"SELECT {columnas} FROM jugadores WHERE id = ?",
            (id_jugador,),
        ).fetchone()

    if fila is None:
        return None

    return _fila_a_jugador(fila)


def actualizar_jugador(jugador: Jugador) -> None:
    """
    Actualiza un jugador existente utilizando su ID.
    """

    if jugador.id is None:
        raise ValueError(
            "No se puede actualizar un jugador sin ID."
        )

    _validar_datos_derivados(jugador, "actualizar")

    asignaciones = ", ".join(
        f"{columna} = ?" for columna in COLUMNAS_JUGADOR
    )

    with _conectar() as conexion:
        cursor = conexion.execute(
            f"UPDATE jugadores SET {asignaciones} WHERE id = ?",
            (*_valores_jugador(jugador), jugador.id),
        )

        filas_afectadas = cursor.rowcount

    if filas_afectadas == 0:
        raise ValueError(
            f"No existe un jugador con ID {jugador.id}."
        )
