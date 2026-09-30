import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from balanceador_equipos.jugadores.servicio_jugadores import ServicioJugadores
from balanceador_equipos.models.habilidades import Habilidades
from balanceador_equipos.models.jugador import Jugador
from balanceador_equipos.scoring.perfilador_jugador import PerfiladorJugador


class VentanaRegistrarJugador(tk.Toplevel):
    HABILIDADES = (
        (
            "Características físicas",
            (
                ("velocidad", "Velocidad"),
                ("aceleracion", "Aceleración"),
                ("resistencia", "Resistencia"),
                ("fuerza", "Fuerza"),
                ("agilidad", "Agilidad"),
                ("equilibrio", "Equilibrio"),
                ("salto", "Salto"),
            ),
        ),
        (
            "Tiro y pase",
            (
                ("potencia_tiro", "Potencia de tiro"),
                ("precision_tiro", "Precisión de tiro"),
                ("pase_corto", "Pase corto"),
                ("pase_largo", "Pase largo"),
                ("centros", "Centros"),
            ),
        ),
        (
            "Control y ataque",
            (
                ("control_balon", "Control de balón"),
                ("regate", "Regate"),
                ("vision_juego", "Visión de juego"),
                ("toma_decisiones", "Toma de decisiones"),
                ("posicionamiento_ofensivo", "Posicionamiento ofensivo"),
                ("desmarque", "Desmarque"),
                ("anticipacion", "Anticipación"),
            ),
        ),
        (
            "Defensa",
            (
                ("marcaje", "Marcaje"),
                ("entradas", "Entradas"),
                ("intercepciones", "Intercepciones"),
                (
                    "posicionamiento_defensivo",
                    "Posicionamiento defensivo",
                ),
            ),
        ),
        (
            "Portero",
            (
                ("reflejos", "Reflejos"),
                ("estirada", "Estirada"),
                ("juego_aereo", "Juego aéreo"),
                ("seguridad_balon", "Seguridad de balón"),
            ),
        ),
    )

    VALOR_INICIAL_HABILIDAD = "50"
    MIN_VALOR_HABILIDAD = 0
    MAX_VALOR_HABILIDAD = 100

    def __init__(
        self,
        master: tk.Misc,
        al_guardar: Callable[[], None],
        jugador: Jugador | None = None,
    ) -> None:
        super().__init__(master)

        self.al_guardar = al_guardar
        self.jugador = jugador
        self.es_edicion = jugador is not None

        self.title(
            "Actualizar jugador" if self.es_edicion else "Registrar jugador"
        )
        self.geometry("650x700")
        self.resizable(False, True)

        self.campos_habilidades: dict[str, ttk.Entry] = {}

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        contenedor_principal = ttk.Frame(self, padding=20)
        contenedor_principal.pack(fill=tk.BOTH, expand=True)

        titulo = ttk.Label(
            contenedor_principal,
            text=(
                "Actualizar jugador"
                if self.es_edicion
                else "Registrar jugador"
            ),
            font=("Segoe UI", 16, "bold"),
        )
        titulo.pack(anchor=tk.W, pady=(0, 15))

        self._crear_datos_jugador(contenedor_principal)
        self._crear_formulario_habilidades(contenedor_principal)
        self._crear_botones(contenedor_principal)

    def _crear_datos_jugador(self, parent: ttk.Frame) -> None:
        marco_datos = ttk.LabelFrame(
            parent,
            text="Información del jugador",
            padding=15,
        )
        marco_datos.pack(fill=tk.X, pady=(0, 15))

        etiqueta_nombre = ttk.Label(
            marco_datos,
            text="Nombre:",
        )
        etiqueta_nombre.grid(
            row=0,
            column=0,
            sticky=tk.W,
            padx=(0, 10),
        )

        self.campo_nombre = ttk.Entry(marco_datos)
        self.campo_nombre.grid(
            row=0,
            column=1,
            sticky=tk.EW,
        )

        marco_datos.columnconfigure(1, weight=1)

        if self.jugador is not None:
            self.campo_nombre.insert(0, self.jugador.nombre)

    def _crear_formulario_habilidades(self, parent: ttk.Frame) -> None:
        marco_habilidades = ttk.LabelFrame(
            parent,
            text="Habilidades",
            padding=10,
        )
        marco_habilidades.pack(
            fill=tk.BOTH,
            expand=True,
        )

        canvas = tk.Canvas(
            marco_habilidades,
            highlightthickness=0,
            borderwidth=0,
        )

        scrollbar = ttk.Scrollbar(
            marco_habilidades,
            orient=tk.VERTICAL,
            command=canvas.yview,
        )

        contenedor_habilidades = ttk.Frame(canvas)

        canvas.configure(
            yscrollcommand=scrollbar.set,
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=contenedor_habilidades,
            anchor=tk.NW,
        )

        contenedor_habilidades.bind(
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
                lambda event: self._desplazar_habilidades(
                    canvas,
                    event,
                ),
            ),
        )

        canvas.bind(
            "<Leave>",
            lambda _event: canvas.unbind_all("<MouseWheel>"),
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

        self._crear_campos_habilidades(contenedor_habilidades)

    def _desplazar_habilidades(
        self,
        canvas: tk.Canvas,
        event: tk.Event,
    ) -> None:
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units",
        )

    def _crear_campos_habilidades(
        self,
        parent: ttk.Frame,
    ) -> None:
        for fila, (categoria, habilidades) in enumerate(
            self.HABILIDADES
        ):
            marco_categoria = ttk.LabelFrame(
                parent,
                text=categoria,
                padding=10,
            )
            marco_categoria.grid(
                row=fila,
                column=0,
                sticky=tk.EW,
                padx=5,
                pady=(0, 10),
            )

            for indice, (nombre, etiqueta) in enumerate(habilidades):
                columna = indice % 2
                fila_campo = indice // 2

                marco_campo = ttk.Frame(marco_categoria)
                marco_campo.grid(
                    row=fila_campo,
                    column=columna,
                    sticky=tk.EW,
                    padx=5,
                    pady=4,
                )

                etiqueta_habilidad = ttk.Label(
                    marco_campo,
                    text=f"{etiqueta}:",
                )
                etiqueta_habilidad.pack(side=tk.LEFT)

                campo = ttk.Entry(
                    marco_campo,
                    width=6,
                    justify=tk.CENTER,
                )

                valor_inicial = self._obtener_valor_inicial_habilidad(
                    nombre
                )
                campo.insert(0, valor_inicial)

                campo.pack(side=tk.RIGHT)

                self.campos_habilidades[nombre] = campo

            marco_categoria.columnconfigure(0, weight=1)
            marco_categoria.columnconfigure(1, weight=1)

        parent.columnconfigure(0, weight=1)

    def _obtener_valor_inicial_habilidad(self, nombre: str) -> str:
        if self.jugador is None:
            return self.VALOR_INICIAL_HABILIDAD

        valor = getattr(self.jugador.habilidades, nombre)
        return str(valor)

    def _crear_botones(self, parent: ttk.Frame) -> None:
        marco_botones = ttk.Frame(parent)
        marco_botones.pack(
            fill=tk.X,
            pady=(15, 0),
        )

        boton_cancelar = ttk.Button(
            marco_botones,
            text="Cancelar",
            command=self.destroy,
        )
        boton_cancelar.pack(side=tk.RIGHT)

        boton_guardar = ttk.Button(
            marco_botones,
            text="Actualizar" if self.es_edicion else "Guardar",
            command=self._guardar_jugador,
        )
        boton_guardar.pack(
            side=tk.RIGHT,
            padx=(0, 10),
        )

    def _validar_formulario(self) -> dict[str, int] | None:
        nombre = self.campo_nombre.get()

        if not nombre:
            messagebox.showerror(
                "Datos inválidos",
                "El nombre del jugador no puede estar vacío.",
                parent=self,
            )
            self.campo_nombre.focus_set()
            return None

        if nombre != nombre.strip():
            messagebox.showerror(
                "Datos inválidos",
                (
                    "El nombre del jugador no puede comenzar ni "
                    "terminar con espacios."
                ),
                parent=self,
            )
            self.campo_nombre.focus_set()
            return None

        habilidades: dict[str, int] = {}

        for nombre_habilidad, campo in self.campos_habilidades.items():
            valor = campo.get()

            if not valor:
                messagebox.showerror(
                    "Datos inválidos",
                    (
                        f"La habilidad '{nombre_habilidad}' "
                        "no puede estar vacía."
                    ),
                    parent=self,
                )
                campo.focus_set()
                return None

            try:
                valor_entero = int(valor)
            except ValueError:
                messagebox.showerror(
                    "Datos inválidos",
                    (
                        f"La habilidad '{nombre_habilidad}' "
                        "debe ser un número entero."
                    ),
                    parent=self,
                )
                campo.focus_set()
                return None

            if not (
                self.MIN_VALOR_HABILIDAD
                <= valor_entero
                <= self.MAX_VALOR_HABILIDAD
            ):
                messagebox.showerror(
                    "Datos inválidos",
                    (
                        f"La habilidad '{nombre_habilidad}' debe estar "
                        f"entre {self.MIN_VALOR_HABILIDAD} y "
                        f"{self.MAX_VALOR_HABILIDAD}."
                    ),
                    parent=self,
                )
                campo.focus_set()
                return None

            habilidades[nombre_habilidad] = valor_entero

        return habilidades

    def _guardar_jugador(self) -> None:
        habilidades_validadas = self._validar_formulario()

        if habilidades_validadas is None:
            return

        try:
            habilidades = Habilidades(**habilidades_validadas)

            if self.jugador is None:
                jugador = Jugador(
                    id=None,
                    nombre=self.campo_nombre.get(),
                    habilidades=habilidades,
                    posicion_sugerida=None,
                    puntuacion=None,
                )

                jugador = PerfiladorJugador.calcular(jugador)

                posicion_sugerida = jugador.posicion_sugerida
                puntuacion = jugador.puntuacion

                if posicion_sugerida is None:
                    raise RuntimeError(
                        "No fue posible determinar la posición "
                        "sugerida del jugador."
                    )

                if puntuacion is None:
                    raise RuntimeError(
                        "No fue posible calcular la puntuación "
                        "del jugador."
                    )

                ServicioJugadores.registrar(jugador)

                mensaje = (
                    f"El jugador '{jugador.nombre}' fue registrado "
                    "correctamente.\n\n"
                    f"Posición sugerida: "
                    f"{posicion_sugerida.value.capitalize()}\n"
                    f"Puntuación: {puntuacion:.2f}"
                )
            else:
                jugador_actualizado = ServicioJugadores.actualizar(
                    jugador=self.jugador,
                    nombre=self.campo_nombre.get(),
                    habilidades=habilidades,
                )

                posicion_sugerida = (
                    jugador_actualizado.posicion_sugerida
                )
                puntuacion = jugador_actualizado.puntuacion

                if posicion_sugerida is None:
                    raise RuntimeError(
                        "No fue posible determinar la posición "
                        "sugerida del jugador."
                    )

                if puntuacion is None:
                    raise RuntimeError(
                        "No fue posible calcular la puntuación "
                        "del jugador."
                    )

                mensaje = (
                    f"El jugador '{jugador_actualizado.nombre}' "
                    "fue actualizado correctamente.\n\n"
                    f"Posición sugerida: "
                    f"{posicion_sugerida.value.capitalize()}\n"
                    f"Puntuación: {puntuacion:.2f}"
                )

        except (
            TypeError,
            ValueError,
            RuntimeError,
            sqlite3.Error,
        ) as error:
            messagebox.showerror(
                "Error al guardar jugador",
                str(error),
                parent=self,
            )
            return

        messagebox.showinfo(
            "Jugador guardado",
            mensaje,
            parent=self,
        )

        self.al_guardar()
        self.destroy()