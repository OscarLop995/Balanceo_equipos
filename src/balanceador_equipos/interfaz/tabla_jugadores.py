from pathlib import Path
import tkinter as tk
from tkinter import ttk
from typing import Callable, Literal

from balanceador_equipos.models.jugador import Jugador


class TablaJugadores(ttk.Frame):
    COLUMNAS = ("nombre", "puntuacion", "posicion", "accion")

    ANCHOS_COLUMNAS = {
        "nombre": 300,
        "puntuacion": 120,
        "posicion": 180,
        "accion": 100,
    }

    def __init__(
        self,
        master: tk.Misc,
        jugadores: list[Jugador],
        al_actualizar: Callable[[Jugador], None],
    ) -> None:
        super().__init__(master)

        self.al_actualizar = al_actualizar

        ruta_icono = (
            Path(__file__).parent
            / "recursos"
            / "edit.png"
        )

        self.icono_editar = tk.PhotoImage(
            file=ruta_icono
        ).subsample(3, 3)

        self._crear_tabla()
        self.mostrar_jugadores(jugadores)

    def _crear_tabla(self) -> None:
        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            borderwidth=0,
        )

        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
        )

        self.contenedor = ttk.Frame(
            self.canvas
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.contenedor,
            anchor=tk.NW,
        )

        self.contenedor.bind(
            "<Configure>",
            self._actualizar_scrollregion,
        )

        self.canvas.bind(
            "<Configure>",
            self._ajustar_ancho_contenedor,
        )

        self.canvas.bind(
            "<Enter>",
            lambda _event: self.canvas.bind_all(
                "<MouseWheel>",
                self._desplazar,
            ),
        )

        self.canvas.bind(
            "<Leave>",
            lambda _event: self.canvas.unbind_all(
                "<MouseWheel>"
            ),
        )

        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        self._crear_encabezados()

    def _crear_encabezados(self) -> None:
        encabezados = {
            "nombre": "Nombre",
            "puntuacion": "Puntuación",
            "posicion": "Posición",
            "accion": "Acción",
        }

        for columna, texto in encabezados.items():
            encabezado = ttk.Label(
                self.contenedor,
                text=texto,
                anchor="center",
                font=("Segoe UI", 10, "bold"),
                relief=tk.SOLID,
                borderwidth=1,
            )

            indice_columna = self.COLUMNAS.index(columna)

            encabezado.grid(
                row=0,
                column=indice_columna,
                sticky=tk.NSEW,
            )

            self.contenedor.columnconfigure(
                indice_columna,
                minsize=self.ANCHOS_COLUMNAS[columna],
                weight=1,
            )

    def mostrar_jugadores(
        self,
        jugadores: list[Jugador],
    ) -> None:
        for fila, jugador in enumerate(
            jugadores,
            start=1,
        ):
            posicion = (
                jugador.posicion_sugerida.value.capitalize()
                if jugador.posicion_sugerida is not None
                else "-"
            )

            puntuacion = (
                f"{jugador.puntuacion:.2f}"
                if jugador.puntuacion is not None
                else "-"
            )

            self._crear_celda(
                texto=jugador.nombre,
                fila=fila,
                columna=0,
                anchor="w",
            )

            self._crear_celda(
                texto=puntuacion,
                fila=fila,
                columna=1,
                anchor="center",
            )

            self._crear_celda(
                texto=posicion,
                fila=fila,
                columna=2,
                anchor="center",
            )

            self._crear_boton_editar(
                jugador=jugador,
                fila=fila,
            )

    def _crear_celda(
        self,
        texto: str,
        fila: int,
        columna: int,
        anchor: Literal["w", "center"],
    ) -> None:
        celda = tk.Label(
            self.contenedor,
            text=texto,
            anchor=anchor,
            font=("Segoe UI", 10),
            padx=8,
            relief=tk.SOLID,
            borderwidth=1,
        )

        celda.grid(
            row=fila,
            column=columna,
            sticky=tk.NSEW,
        )

    def _crear_boton_editar(
        self,
        jugador: Jugador,
        fila: int,
    ) -> None:
        boton = ttk.Button(
            self.contenedor,
            image=self.icono_editar,
            width=3,
            command=lambda: self.al_actualizar(jugador),
        )

        boton.grid(
            row=fila,
            column=3,
            sticky=tk.NSEW,
            padx=1,
            pady=1,
        )

    def _desplazar(
        self,
        event: tk.Event,
    ) -> None:
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units",
        )

    def _actualizar_scrollregion(
        self,
        _event: tk.Event,
    ) -> None:
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _ajustar_ancho_contenedor(
        self,
        event: tk.Event,
    ) -> None:
        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width,
        )