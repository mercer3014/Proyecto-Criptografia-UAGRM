import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk

from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO, FUENTE_TITULO, FUENTE_SUBTITULO,
    FUENTE_NORMAL, FUENTE_PEQUENA, BotonEstilizado,
    configurar_estilo_notebook
)

EJERCICIOS = [
    ("1", "Vectores Unitarios",
     "Demuestra cómo el cifrado de vectores unitarios\n"
     "(BAA, ABA, AAB) revela las columnas de K.\n\n"
     "VINCENTY MAMANI DAVID LEONEL"),
    ("2", "Matriz Inversa",
     "Calcula la adjunta y determinante para hallar\n"
     "K⁻¹ en módulo 27.\n\n"
     "ORELLANA GUTIERREZ DIEGO "),
    ("3", "Ataque Gauss-Jordan",
     "Simula paso a paso el ataque Gauss-Jordan sobre\n"
     "[(Texto Claro) | (Texto Cifrado)] para recuperar K.\n\n"
     "CEREZO CHOQUE ALEX BRAYAN"),
    ("4", "Módulo 191",
     "Cifrado César y Vigenère en módulo 191\n"
     "para el alfabeto CP437 extendido.\n\n"
     "CONDORI HURTADO GABRIEL"),
    ("5", "Cifrado Hill 2×2",
     "Cifrado de digramas con álgebra lineal.\n"
     "Clave simbólica, módulo 27 y 191.\n\n"
     "CONDORI VILLANUEVA PITHER DANIEL"),
]


class AplicacionPrincipal:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Cifrado de Hill — Proyecto Unificado")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.geometry("1280x800")
        self.raiz.minsize(1100, 700)

        configurar_estilo_notebook()

        self._frame_actual = None
        self._controlador_actual = None

        self._construir_interfaz()

    def _construir_interfaz(self):
        panel_superior = tk.Frame(self.raiz, bg=COLOR_PANEL, pady=10)
        panel_superior.pack(fill=tk.X)

        tk.Label(
            panel_superior,
            text="Cifrado de Hill — Proyecto Unificado",
            bg=COLOR_PANEL, fg=COLOR_ACENTO,
            font=("Segoe UI", 20, "bold")
        ).pack()

        tk.Label(
            panel_superior,
            text="Módulo 27 (ABCDEFGHIJKLMNÑOPQRSTUVWXYZ) — Módulo 191 (CP437)",
            bg=COLOR_PANEL, fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        ).pack(pady=(2, 0))

        panel_principal = tk.Frame(self.raiz, bg=COLOR_FONDO)
        panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self._panel_lateral = tk.Frame(panel_principal, bg=COLOR_PANEL, width=300)
        self._panel_lateral.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        self._panel_lateral.pack_propagate(False)

        tk.Label(
            self._panel_lateral,
            text="Menú de Ejercicios",
            bg=COLOR_PANEL, fg=COLOR_ACENTO,
            font=FUENTE_TITULO
        ).pack(pady=(15, 12))

        for numero, titulo, _ in EJERCICIOS:
            btn = BotonEstilizado(
                self._panel_lateral,
                texto=f"Ej. {numero}: {titulo}",
                comando=lambda n=int(numero): self._cargar_ejercicio(n),
                ancho=30
            )
            btn.pack(pady=4, padx=10)

        panel_derecho = tk.Frame(panel_principal, bg=COLOR_FONDO)
        panel_derecho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._descripcion_label = tk.Label(
            panel_derecho,
            text="",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA,
            wraplength=800,
            justify="left"
        )
        self._descripcion_label.pack(anchor="w", pady=(0, 5))

        self._contenedor_ejercicio = tk.Frame(panel_derecho, bg=COLOR_FONDO)
        self._contenedor_ejercicio.pack(fill=tk.BOTH, expand=True)

    def _limpiar_panel(self):
        if self._frame_actual is not None:
            self._frame_actual.destroy()
            self._frame_actual = None
        self._controlador_actual = None

    def _cargar_ejercicio(self, numero):
        self._limpiar_panel()

        idx = numero - 1
        if idx < 0 or idx >= len(EJERCICIOS):
            return

        _, _, descripcion = EJERCICIOS[idx]
        self._descripcion_label.config(text=descripcion)

        if numero == 1:
            self._cargar_ej1()
        elif numero == 2:
            self._cargar_ej2()
        elif numero == 3:
            self._cargar_ej3()
        elif numero == 4:
            self._cargar_ej4()
        elif numero == 5:
            self._cargar_ej5()

    def _cargar_ej1(self):
        from view.vista_vectores import VistaVectoresUnitarios
        from controllers.controlador_vectores import ControladorVectoresUnitarios
        vista = VistaVectoresUnitarios(self._contenedor_ejercicio)
        vista.pack(fill=tk.BOTH, expand=True)
        controlador = ControladorVectoresUnitarios(vista)
        self._frame_actual = vista
        self._controlador_actual = controlador

    def _cargar_ej2(self):
        from view.vista_inversa import VistaMatrizInversa
        from controllers.controlador_inversa import ControladorMatrizInversa
        vista = VistaMatrizInversa(self._contenedor_ejercicio)
        vista.pack(fill=tk.BOTH, expand=True)
        controlador = ControladorMatrizInversa(vista)
        self._frame_actual = vista
        self._controlador_actual = controlador

    def _cargar_ej3(self):
        from view.vista_gauss import VistaGaussJordan
        from controllers.controlador_gauss import ControladorGaussJordan
        vista = VistaGaussJordan(self._contenedor_ejercicio)
        vista.pack(fill=tk.BOTH, expand=True)
        controlador = ControladorGaussJordan(vista)
        self._frame_actual = vista
        self._controlador_actual = controlador

    def _cargar_ej4(self):
        from view.vista_mod191 import VistaMod191
        from controllers.controlador_mod191 import ControladorMod191
        vista = VistaMod191(self._contenedor_ejercicio)
        vista.pack(fill=tk.BOTH, expand=True)
        controlador = ControladorMod191(vista)
        self._frame_actual = vista
        self._controlador_actual = controlador

    def _cargar_ej5(self):
        from view.vista_hill import VistaCifraHill
        from controllers.controlador_hill import ControladorCifraHill
        vista = VistaCifraHill(self._contenedor_ejercicio)
        vista.pack(fill=tk.BOTH, expand=True)
        controlador = ControladorCifraHill(vista)
        self._frame_actual = vista
        self._controlador_actual = controlador

    def iniciar(self):
        self._cargar_ejercicio(1)
        self.raiz.mainloop()


if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.iniciar()