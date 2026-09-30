import tkinter as tk
from tkinter import ttk

from balanceador_equipos.interfaz.tabla_jugadores import TablaJugadores
from balanceador_equipos.interfaz.ventana_nuevo_partido import (
    VentanaNuevoPartido,
)
from balanceador_equipos.interfaz.ventana_registrar_jugador import (
    VentanaRegistrarJugador,
)
from balanceador_equipos.jugadores.servicio_jugadores import ServicioJugadores
from balanceador_equipos.models.jugador import Jugador


class VentanaPrincipal(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)

        self.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=20,
        )

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        titulo = ttk.Label(
            self,
            text="Balanceador de equipos",
            font=("Segoe UI", 18, "bold"),
        )
        titulo.pack(
            anchor=tk.W,
            pady=(0, 20),
        )

        marco_acciones = ttk.Frame(self)
        marco_acciones.pack(
            fill=tk.X,
            pady=(0, 20),
        )

        self.boton_registrar = ttk.Button(
            marco_acciones,
            text="Registrar jugador",
            command=self._abrir_registro_jugador,
        )
        self.boton_registrar.pack(
            side=tk.LEFT,
        )

        self.boton_nuevo_partido = ttk.Button(
            marco_acciones,
            text="Nuevo partido",
            command=self._abrir_nuevo_partido,
        )
        self.boton_nuevo_partido.pack(
            side=tk.LEFT,
            padx=(10, 0),
        )

        marco_jugadores = ttk.LabelFrame(
            self,
            text="Jugadores registrados",
            padding=10,
        )
        marco_jugadores.pack(
            fill=tk.BOTH,
            expand=True,
        )

        self.marco_jugadores = marco_jugadores

        self._actualizar_tabla_jugadores()

    def _abrir_registro_jugador(self) -> None:
        VentanaRegistrarJugador(
            self,
            self._actualizar_tabla_jugadores,
        )

    def _abrir_edicion_jugador(
        self,
        jugador: Jugador,
    ) -> None:
        VentanaRegistrarJugador(
            self,
            self._actualizar_tabla_jugadores,
            jugador,
        )

    def _abrir_nuevo_partido(self) -> None:
        VentanaNuevoPartido(self)

    def _actualizar_tabla_jugadores(self) -> None:
        for widget in self.marco_jugadores.winfo_children():
            widget.destroy()

        jugadores = ServicioJugadores.obtener_todos()

        self.tabla_jugadores = TablaJugadores(
            self.marco_jugadores,
            jugadores,
            self._abrir_edicion_jugador,
        )

        self.tabla_jugadores.pack(
            fill=tk.BOTH,
            expand=True,
        )