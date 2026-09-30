import tkinter as tk
from collections.abc import Sequence
from tkinter import ttk

from balanceador_equipos.models.jugador import Jugador


class VentanaResultadoEquipos(tk.Toplevel):
    def __init__(
        self,
        master: tk.Misc,
        equipo_a: Sequence[Jugador],
        equipo_b: Sequence[Jugador],
    ) -> None:
        super().__init__(master)

        self.title("Equipos armados")
        self.geometry("800x500")
        self.minsize(700, 400)

        self.equipo_a = equipo_a
        self.equipo_b = equipo_b

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        contenedor_principal = ttk.Frame(
            self,
            padding=20,
        )
        contenedor_principal.pack(
            fill=tk.BOTH,
            expand=True,
        )

        titulo = ttk.Label(
            contenedor_principal,
            text="Equipos armados",
            font=("Segoe UI", 18, "bold"),
        )
        titulo.pack(
            anchor=tk.W,
            pady=(0, 20),
        )

        contenedor_equipos = ttk.Frame(
            contenedor_principal,
        )
        contenedor_equipos.pack(
            fill=tk.BOTH,
            expand=True,
        )

        marco_equipo_a = self._crear_marco_equipo(
            contenedor_equipos,
            "Equipo A",
            self.equipo_a,
        )
        marco_equipo_a.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            padx=(0, 10),
        )

        marco_equipo_b = self._crear_marco_equipo(
            contenedor_equipos,
            "Equipo B",
            self.equipo_b,
        )
        marco_equipo_b.grid(
            row=0,
            column=1,
            sticky=tk.NSEW,
            padx=(10, 0),
        )

        contenedor_equipos.columnconfigure(
            0,
            weight=1,
        )
        contenedor_equipos.columnconfigure(
            1,
            weight=1,
        )
        contenedor_equipos.rowconfigure(
            0,
            weight=1,
        )

        boton_cerrar = ttk.Button(
            contenedor_principal,
            text="Cerrar",
            command=self.destroy,
        )
        boton_cerrar.pack(
            anchor=tk.E,
            pady=(20, 0),
        )

    def _crear_marco_equipo(
        self,
        parent: ttk.Frame,
        nombre_equipo: str,
        jugadores: Sequence[Jugador],
    ) -> ttk.LabelFrame:
        marco_equipo = ttk.LabelFrame(
            parent,
            text=nombre_equipo,
            padding=10,
        )

        encabezado_nombre = ttk.Label(
            marco_equipo,
            text="Jugador",
            anchor=tk.W,
            font=("Segoe UI", 10, "bold"),
        )
        encabezado_nombre.grid(
            row=0,
            column=0,
            sticky=tk.EW,
            padx=5,
            pady=(0, 8),
        )

        encabezado_posicion = ttk.Label(
            marco_equipo,
            text="Posición",
            anchor=tk.CENTER,
            font=("Segoe UI", 10, "bold"),
        )
        encabezado_posicion.grid(
            row=0,
            column=1,
            sticky=tk.EW,
            padx=5,
            pady=(0, 8),
        )

        marco_equipo.columnconfigure(
            0,
            weight=1,
        )
        marco_equipo.columnconfigure(
            1,
            minsize=140,
        )

        for fila, jugador in enumerate(
            jugadores,
            start=1,
        ):
            self._crear_fila_jugador(
                marco_equipo,
                jugador,
                fila,
            )

        return marco_equipo

    def _crear_fila_jugador(
        self,
        parent: ttk.LabelFrame,
        jugador: Jugador,
        fila: int,
    ) -> None:
        nombre = ttk.Label(
            parent,
            text=jugador.nombre,
            anchor=tk.W,
        )
        nombre.grid(
            row=fila,
            column=0,
            sticky=tk.EW,
            padx=5,
            pady=4,
        )

        posicion = (
            jugador.posicion_sugerida.value.capitalize()
            if jugador.posicion_sugerida is not None
            else "-"
        )

        etiqueta_posicion = ttk.Label(
            parent,
            text=posicion,
            anchor=tk.CENTER,
        )
        etiqueta_posicion.grid(
            row=fila,
            column=1,
            sticky=tk.EW,
            padx=5,
            pady=4,
        )