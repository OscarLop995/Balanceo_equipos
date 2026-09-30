import tkinter as tk

from balanceador_equipos.interfaz.ventana_principal import (
    VentanaPrincipal,
)
from balanceador_equipos.persistencia import inicializar_base_datos


class Aplicacion:
    """
    Punto de entrada de la interfaz gráfica de la aplicación.
    """

    def __init__(self) -> None:
        inicializar_base_datos()

        self.ventana = tk.Tk()
        self.ventana.title("Balanceador de equipos")
        self.ventana.geometry("900x600")

        VentanaPrincipal(self.ventana)

    def ejecutar(self) -> None:
        """
        Inicia el ciclo principal de la aplicación.
        """

        self.ventana.mainloop()