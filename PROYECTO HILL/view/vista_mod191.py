import tkinter as tk
from tkinter import ttk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_TEXTO, COLOR_TEXTO_SECUNDARIO,
    COLOR_EXITO, COLOR_ERROR, COLOR_ADVERTENCIA, COLOR_SEPARADOR,
    FUENTE_SUBTITULO, FUENTE_NORMAL,
    BotonEstilizado, EntradaEstilizada, EtiquetaTitulo, EtiquetaSubtitulo, CajaTexto, RadioEstilizado,
    configurar_estilo_notebook
)


class VistaMod191(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLOR_FONDO)
        self.controller = None
        configurar_estilo_notebook()
        self._crear_interfaz()

    def _crear_interfaz(self):
        titulo = EtiquetaTitulo(self, "Cifrado Módulo 191 (CP437)")
        titulo.pack(pady=(10, 5), padx=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        tab_cifrar = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.notebook.add(tab_cifrar, text="  Cifrar / Descifrar  ")

        tab_alfabeto = tk.Frame(self.notebook, bg=COLOR_FONDO)
        self.notebook.add(tab_alfabeto, text="  Alfabeto  ")

        self._crear_tab_cifrar(tab_cifrar)
        self._crear_tab_alfabeto(tab_alfabeto)

    def _crear_tab_cifrar(self, padre):
        contenedor = tk.Frame(padre, bg=COLOR_FONDO)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        panel_izquierdo = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3), pady=5)

        panel_derecho = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(3, 0), pady=5)

        etiqueta_entrada = EtiquetaSubtitulo(panel_izquierdo, "Texto de entrada:", bg=COLOR_PANEL)
        etiqueta_entrada.pack(pady=(10, 3), padx=10, anchor="w")

        self.caja_entrada = CajaTexto(panel_izquierdo, alto=6)
        self.caja_entrada.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.caja_entrada.config(state="normal")

        marco_modo = tk.Frame(panel_izquierdo, bg=COLOR_PANEL)
        marco_modo.pack(padx=10, pady=5, fill=tk.X)

        etiqueta_modo = tk.Label(marco_modo, text="Modo:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        etiqueta_modo.pack(side=tk.LEFT, padx=(0, 10))

        self.variable_modo = tk.StringVar(value="cesar")
        radio_cesar = RadioEstilizado(marco_modo, "César", self.variable_modo, "cesar")
        radio_cesar.pack(side=tk.LEFT, padx=(0, 10))
        radio_vigenere = RadioEstilizado(marco_modo, "Vigenère", self.variable_modo, "vigenere")
        radio_vigenere.pack(side=tk.LEFT)

        marco_clave = tk.Frame(panel_izquierdo, bg=COLOR_PANEL)
        marco_clave.pack(padx=10, pady=5, fill=tk.X)

        self.etiqueta_clave = tk.Label(marco_clave, text="Clave (numérica):", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        self.etiqueta_clave.pack(side=tk.LEFT, padx=(0, 5))
        self.entrada_clave = EntradaEstilizada(marco_clave, width=20)
        self.entrada_clave.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.variable_modo.trace_add("write", self._modo_cambiado)

        marco_botones = tk.Frame(panel_izquierdo, bg=COLOR_PANEL)
        marco_botones.pack(padx=10, pady=10, fill=tk.X)

        boton_cifrar = BotonEstilizado(marco_botones, "Cifrar", self._cifrar, color=COLOR_ACENTO)
        boton_cifrar.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        boton_descifrar = BotonEstilizado(marco_botones, "Descifrar", self._descifrar, color="#e94560")
        boton_descifrar.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        boton_limpiar = BotonEstilizado(marco_botones, "Limpiar", self._limpiar, color=COLOR_SEPARADOR)
        boton_limpiar.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        etiqueta_resultado = EtiquetaSubtitulo(panel_izquierdo, "Resultado:", bg=COLOR_PANEL)
        etiqueta_resultado.pack(pady=(5, 3), padx=10, anchor="w")

        self.caja_resultado = CajaTexto(panel_izquierdo, alto=5)
        self.caja_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        etiqueta_sim = EtiquetaSubtitulo(panel_derecho, "Simulación paso a paso:", bg=COLOR_PANEL)
        etiqueta_sim.pack(pady=(10, 3), padx=10, anchor="w")

        self.caja_simulacion = CajaTexto(panel_derecho, alto=20)
        self.caja_simulacion.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def _crear_tab_alfabeto(self, padre):
        etiqueta_alf = EtiquetaSubtitulo(padre, "Alfabeto Módulo 191 (CP437):", bg=COLOR_FONDO)
        etiqueta_alf.pack(pady=(10, 5), padx=10, anchor="w")

        self.caja_alfabeto = CajaTexto(padre, alto=25)
        self.caja_alfabeto.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def _modo_cambiado(self, *args):
        if self.variable_modo.get() == "cesar":
            self.etiqueta_clave.config(text="Clave (numérica):")
        else:
            self.etiqueta_clave.config(text="Clave (texto):")

    def establecer_controlador(self, controller):
        self.controller = controller

    def obtener_texto_entrada(self):
        return self.caja_entrada.get("1.0", tk.END).strip()

    def obtener_clave(self):
        return self.entrada_clave.get()

    def es_vigenere(self):
        return self.variable_modo.get() == "vigenere"

    def mostrar_resultado(self, texto):
        self.caja_resultado.actualizar(texto)

    def mostrar_simulacion(self, pasos, es_vigenere):
        contenido = ""
        for paso in pasos:
            contenido += paso + "\n"
        self.caja_simulacion.actualizar(contenido)

    def mostrar_alfabeto(self, texto):
        self.caja_alfabeto.actualizar(texto)

    def mostrar_error(self, mensaje):
        self.caja_resultado.actualizar(f"Error: {mensaje}", COLOR_ERROR)

    def _cifrar(self):
        if self.controller:
            self.controller.cifrar()

    def _descifrar(self):
        if self.controller:
            self.controller.descifrar()

    def _limpiar(self):
        self.caja_entrada.delete("1.0", tk.END)
        self.entrada_clave.delete(0, tk.END)
        self.caja_resultado.actualizar("")
        self.caja_simulacion.actualizar("")