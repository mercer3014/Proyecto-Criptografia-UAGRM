import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable

COLOR_FONDO = "#1e1e2e"
COLOR_PANEL = "#2a2a3e"
COLOR_PANEL_CLARO = "#313145"
COLOR_ACENTO = "#7c6af7"
COLOR_ACENTO_HOVER = "#9a8bff"
COLOR_TEXTO = "#cdd6f4"
COLOR_TEXTO_SECUNDARIO = "#a6adc8"
COLOR_EXITO = "#a6e3a1"
COLOR_ERROR = "#f38ba8"
COLOR_ADVERTENCIA = "#fab387"
COLOR_INFO = "#89dceb"
COLOR_SEPARADOR = "#45475a"
COLOR_RESALTADO = "#f9e2af"
COLOR_PIVOTE = "#f38ba8"

FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 11, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
FUENTE_MONO = ("Consolas", 11)
FUENTE_MONO_GRANDE = ("Consolas", 12, "bold")
FUENTE_PEQUENA = ("Segoe UI", 9)
FUENTE_PASO = ("Segoe UI", 10, "bold")


class BotonEstilizado(tk.Button):
    def __init__(self, padre, texto: str, comando: Callable, color: str = COLOR_ACENTO, ancho: int = 0, **kwargs):
        super().__init__(padre, text=texto, command=comando, bg=color, fg=COLOR_TEXTO,
                         font=FUENTE_NORMAL, relief="flat", padx=14, pady=6, cursor="hand2",
                         activebackground=COLOR_ACENTO_HOVER, activeforeground=COLOR_TEXTO, bd=0, **kwargs)
        self._color_original = color
        if ancho:
            self.config(width=ancho)
        self.bind("<Enter>", lambda e: self.config(bg=COLOR_ACENTO_HOVER))
        self.bind("<Leave>", lambda e: self.config(bg=self._color_original))


class EntradaEstilizada(tk.Entry):
    def __init__(self, padre, **kwargs):
        super().__init__(padre, bg="#3b3b54", fg=COLOR_TEXTO, insertbackground="white",
                         font=FUENTE_MONO, relief="solid", bd=2, highlightthickness=2,
                         highlightcolor=COLOR_ACENTO, highlightbackground="#555570",
                         selectbackground=COLOR_ACENTO, selectforeground=COLOR_TEXTO, **kwargs)


class EtiquetaTitulo(tk.Label):
    def __init__(self, padre, texto: str, **kwargs):
        super().__init__(padre, text=texto, bg=COLOR_FONDO, fg=COLOR_ACENTO, font=FUENTE_TITULO, **kwargs)


class EtiquetaSubtitulo(tk.Label):
    def __init__(self, padre, texto: str, **kwargs):
        bg = kwargs.pop("bg", COLOR_FONDO)
        super().__init__(padre, text=texto, bg=bg, fg=COLOR_TEXTO, font=FUENTE_SUBTITULO, **kwargs)


class CajaTexto(scrolledtext.ScrolledText):
    def __init__(self, padre, alto: int = 8, **kwargs):
        super().__init__(padre, bg="#3b3b54", fg=COLOR_TEXTO, font=FUENTE_MONO, relief="solid",
                         bd=2, height=alto, wrap=tk.WORD, state="disabled", highlightthickness=1,
                         highlightcolor=COLOR_ACENTO, highlightbackground="#555570",
                         insertbackground=COLOR_TEXTO, selectbackground=COLOR_ACENTO,
                         selectforeground=COLOR_TEXTO, **kwargs)
        self._alto = alto

    def actualizar(self, texto: str, color: str = COLOR_TEXTO):
        self.config(state="normal")
        self.delete("1.0", tk.END)
        self.insert(tk.END, texto)
        self.config(state="disabled", fg=color)


class RadioEstilizado(tk.Radiobutton):
    def __init__(self, padre, texto: str, variable, valor, **kwargs):
        super().__init__(padre, text=f"  {texto}", variable=variable, value=valor,
                         bg=COLOR_FONDO, fg=COLOR_TEXTO, selectcolor=COLOR_PANEL,
                         activebackground=COLOR_FONDO, activeforeground=COLOR_TEXTO,
                         font=FUENTE_NORMAL, **kwargs)


class SpinboxEstilizado(tk.Spinbox):
    def __init__(self, padre, **kwargs):
        super().__init__(padre, bg="#3b3b54", fg=COLOR_TEXTO, font=FUENTE_MONO,
                         relief="solid", bd=2, highlightthickness=2,
                         highlightcolor=COLOR_ACENTO, highlightbackground="#555570",
                         buttonbackground=COLOR_PANEL, **kwargs)


def configurar_estilo_notebook():
    estilo = ttk.Style()
    estilo.theme_use("default")
    estilo.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
    estilo.configure("TNotebook.Tab", background=COLOR_PANEL, foreground=COLOR_TEXTO_SECUNDARIO,
                      padding=[18, 8], font=FUENTE_NORMAL)
    estilo.map("TNotebook.Tab", background=[("selected", COLOR_ACENTO)], foreground=[("selected", COLOR_TEXTO)])