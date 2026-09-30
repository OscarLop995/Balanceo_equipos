import tkinter as tk
from tkinter import messagebox, ttk

from balanceador_equipos.balanceo.servicio_balanceo import ServicioBalanceo
from balanceador_equipos.interfaz.ventana_resultado_equipos import (
    VentanaResultadoEquipos,
)
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.jugadores.servicio_jugadores import ServicioJugadores


class VentanaNuevoPartido(tk.Toplevel):
    TAMANOS_EQUIPO = (8, 9, 10)

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)

        self.title("Nuevo partido")
        self.geometry("700x650")
        self.resizable(True, True)

        self.jugadores = ServicioJugadores.obtener_todos()
        self.jugadores_seleccionados: set[int] = set()

        self.tamano_equipo = tk.IntVar(
            value=self.TAMANOS_EQUIPO[0]
        )

        self.variables_jugadores: dict[int, tk.BooleanVar] = {}

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
            text="Nuevo partido",
            font=("Segoe UI", 16, "bold"),
        )
        titulo.pack(
            anchor=tk.W,
            pady=(0, 15),
        )

        self._crear_seleccion_tamano(
            contenedor_principal
        )

        self._crear_lista_jugadores(
            contenedor_principal
        )

        self._crear_resumen(
            contenedor_principal
        )

        self._crear_botones(
            contenedor_principal
        )

        self._actualizar_estado()

    def _crear_seleccion_tamano(
        self,
        parent: ttk.Frame,
    ) -> None:
        marco_tamano = ttk.LabelFrame(
            parent,
            text="Jugadores por equipo",
            padding=10,
        )
        marco_tamano.pack(
            fill=tk.X,
            pady=(0, 15),
        )

        for indice, tamano in enumerate(
            self.TAMANOS_EQUIPO
        ):
            radio = ttk.Radiobutton(
                marco_tamano,
                text=str(tamano),
                value=tamano,
                variable=self.tamano_equipo,
                command=self._cambio_tamano_equipo,
            )
            radio.grid(
                row=0,
                column=indice,
                padx=15,
            )

        marco_tamano.columnconfigure(
            0,
            weight=1,
        )
        marco_tamano.columnconfigure(
            1,
            weight=1,
        )
        marco_tamano.columnconfigure(
            2,
            weight=1,
        )

    def _crear_lista_jugadores(
        self,
        parent: ttk.Frame,
    ) -> None:
        marco_jugadores = ttk.LabelFrame(
            parent,
            text="Jugadores disponibles",
            padding=10,
        )
        marco_jugadores.pack(
            fill=tk.BOTH,
            expand=True,
            pady=(0, 15),
        )

        canvas = tk.Canvas(
            marco_jugadores,
            highlightthickness=0,
            borderwidth=0,
        )

        scrollbar = ttk.Scrollbar(
            marco_jugadores,
            orient=tk.VERTICAL,
            command=canvas.yview,
        )

        contenedor = ttk.Frame(canvas)

        canvas.configure(
            yscrollcommand=scrollbar.set,
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=contenedor,
            anchor=tk.NW,
        )

        contenedor.bind(
            "<Configure>",
            lambda _event: canvas.configure(
                scrollregion=canvas.bbox("all")
            ),
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                canvas_window,
                width=event.width,
            ),
        )

        canvas.bind(
            "<Enter>",
            lambda _event: canvas.bind_all(
                "<MouseWheel>",
                lambda event: self._desplazar_jugadores(
                    canvas,
                    event,
                ),
            ),
        )

        canvas.bind(
            "<Leave>",
            lambda _event: canvas.unbind_all(
                "<MouseWheel>"
            ),
        )

        canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        self._crear_encabezados_jugadores(
            contenedor
        )

        for fila, jugador in enumerate(
            self.jugadores,
            start=1,
        ):
            self._crear_fila_jugador(
                contenedor,
                jugador,
                fila,
            )

    def _crear_encabezados_jugadores(
        self,
        parent: ttk.Frame,
    ) -> None:
        encabezados = (
            ("", 0),
            ("Jugador", 1),
            ("Puntuación", 2),
            ("Posición", 3),
        )

        for texto, columna in encabezados:
            encabezado = ttk.Label(
                parent,
                text=texto,
                anchor=tk.CENTER,
                font=("Segoe UI", 10, "bold"),
            )
            encabezado.grid(
                row=0,
                column=columna,
                sticky=tk.NSEW,
                padx=5,
                pady=5,
            )

        parent.columnconfigure(
            0,
            minsize=40,
        )
        parent.columnconfigure(
            1,
            weight=1,
        )
        parent.columnconfigure(
            2,
            minsize=100,
        )
        parent.columnconfigure(
            3,
            minsize=140,
        )

    def _crear_fila_jugador(
        self,
        parent: ttk.Frame,
        jugador: Jugador,
        fila: int,
    ) -> None:
        if jugador.id is None:
            raise RuntimeError(
                "No se puede seleccionar un jugador sin identificador."
            )

        variable = tk.BooleanVar(
            value=False
        )

        self.variables_jugadores[jugador.id] = variable

        checkbutton = ttk.Checkbutton(
            parent,
            variable=variable,
            command=lambda: self._cambio_seleccion(
                jugador
            ),
        )
        checkbutton.grid(
            row=fila,
            column=0,
            padx=5,
            pady=4,
        )

        nombre = ttk.Label(
            parent,
            text=jugador.nombre,
            anchor=tk.W,
        )
        nombre.grid(
            row=fila,
            column=1,
            sticky=tk.EW,
            padx=5,
            pady=4,
        )

        puntuacion = (
            f"{jugador.puntuacion:.2f}"
            if jugador.puntuacion is not None
            else "-"
        )

        etiqueta_puntuacion = ttk.Label(
            parent,
            text=puntuacion,
            anchor=tk.CENTER,
        )
        etiqueta_puntuacion.grid(
            row=fila,
            column=2,
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
            column=3,
            padx=5,
            pady=4,
        )

    def _crear_resumen(
        self,
        parent: ttk.Frame,
    ) -> None:
        self.etiqueta_seleccion = ttk.Label(
            parent,
            text="",
            font=("Segoe UI", 10, "bold"),
        )
        self.etiqueta_seleccion.pack(
            anchor=tk.W,
            pady=(0, 15),
        )

    def _crear_botones(
        self,
        parent: ttk.Frame,
    ) -> None:
        marco_botones = ttk.Frame(parent)
        marco_botones.pack(
            fill=tk.X,
        )

        boton_cancelar = ttk.Button(
            marco_botones,
            text="Cancelar",
            command=self.destroy,
        )
        boton_cancelar.pack(
            side=tk.RIGHT,
        )

        self.boton_armar = ttk.Button(
            marco_botones,
            text="Armar equipos",
            command=self._armar_equipos,
            state=tk.DISABLED,
        )
        self.boton_armar.pack(
            side=tk.RIGHT,
            padx=(0, 10),
        )

    def _cambio_tamano_equipo(self) -> None:
        self._actualizar_estado()

    def _cambio_seleccion(
        self,
        jugador: Jugador,
    ) -> None:
        if jugador.id is None:
            return

        variable = self.variables_jugadores[jugador.id]

        if variable.get():
            self.jugadores_seleccionados.add(
                jugador.id
            )
        else:
            self.jugadores_seleccionados.discard(
                jugador.id
            )

        self._actualizar_estado()

    def _cantidad_requerida(self) -> int:
        return self.tamano_equipo.get() * 2

    def _obtener_jugadores_seleccionados(
        self,
    ) -> list[Jugador]:
        return [
            jugador
            for jugador in self.jugadores
            if jugador.id in self.jugadores_seleccionados
        ]

    def _actualizar_estado(self) -> None:
        seleccionados = len(
            self.jugadores_seleccionados
        )
        requeridos = self._cantidad_requerida()

        self.etiqueta_seleccion.configure(
            text=(
                f"Jugadores seleccionados: "
                f"{seleccionados} / {requeridos}"
            )
        )

        estado_boton = (
            tk.NORMAL
            if seleccionados == requeridos
            else tk.DISABLED
        )

        self.boton_armar.configure(
            state=estado_boton
        )

    def _desplazar_jugadores(
        self,
        canvas: tk.Canvas,
        event: tk.Event,
    ) -> None:
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units",
        )

    def _armar_equipos(self) -> None:
        jugadores_seleccionados = (
            self._obtener_jugadores_seleccionados()
        )

        tamano_equipo = self.tamano_equipo.get()

        if len(jugadores_seleccionados) != (
            tamano_equipo * 2
        ):
            messagebox.showwarning(
                "Selección incompleta",
                (
                    "Debes seleccionar exactamente "
                    f"{tamano_equipo * 2} jugadores."
                ),
                parent=self,
            )
            return

        try:
            distribucion = ServicioBalanceo.balancear(
                jugadores=jugadores_seleccionados,
                tamano_equipo=tamano_equipo,
            )
        except (
            TypeError,
            ValueError,
            RuntimeError,
        ) as error:
            messagebox.showerror(
                "Error al armar equipos",
                str(error),
                parent=self,
            )
            return

        VentanaResultadoEquipos(
            self,
            equipo_a=distribucion.equipo_a,
            equipo_b=distribucion.equipo_b,
        )