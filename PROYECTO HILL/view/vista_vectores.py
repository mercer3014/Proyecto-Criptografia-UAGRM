import tkinter as tk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_TEXTO, COLOR_TEXTO_SECUNDARIO,
    COLOR_EXITO, COLOR_ERROR, COLOR_SEPARADOR,
    FUENTE_SUBTITULO, FUENTE_NORMAL,
    BotonEstilizado, EntradaEstilizada, EtiquetaTitulo, CajaTexto
)


class VistaVectoresUnitarios(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLOR_FONDO)
        self.controller = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        panel_izquierdo = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5), pady=5)

        panel_derecho = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        titulo = EtiquetaTitulo(panel_izquierdo, "Analizador de Vectores Unitarios (Mod 27)")
        titulo.pack(pady=(10, 15), padx=10)

        marco_clave = tk.Frame(panel_izquierdo, bg=COLOR_PANEL)
        marco_clave.pack(padx=15, pady=5, fill=tk.X)

        etiqueta_clave = tk.Label(marco_clave, text="Matriz Clave 3×3:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_SUBTITULO)
        etiqueta_clave.pack(anchor="w", pady=(5, 5))

        cuadricula = tk.Frame(marco_clave, bg=COLOR_PANEL)
        cuadricula.pack(padx=5, pady=5)
        self.entradas_clave = []
        for i in range(3):
            fila_entradas = []
            for j in range(3):
                entrada = EntradaEstilizada(cuadricula, width=5, justify="center")
                entrada.grid(row=i, column=j, padx=3, pady=3)
                fila_entradas.append(entrada)
            self.entradas_clave.append(fila_entradas)

        self.etiqueta_estado = tk.Label(marco_clave, text="", bg=COLOR_PANEL, fg=COLOR_EXITO, font=FUENTE_NORMAL)
        self.etiqueta_estado.pack(pady=(5, 5))

        boton_establecer = BotonEstilizado(marco_clave, "Establecer Clave", self._establecer_clave, color=COLOR_ACENTO)
        boton_establecer.pack(pady=(5, 15), fill=tk.X, padx=5)

        separador = tk.Frame(panel_izquierdo, bg=COLOR_SEPARADOR, height=2)
        separador.pack(fill=tk.X, padx=15, pady=10)

        marco_vectores = tk.Frame(panel_izquierdo, bg=COLOR_PANEL)
        marco_vectores.pack(padx=15, pady=5, fill=tk.X)

        etiqueta_vectores = tk.Label(marco_vectores, text="Vectores Unitarios:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_SUBTITULO)
        etiqueta_vectores.pack(anchor="w", pady=(5, 10))

        boton_v0 = BotonEstilizado(marco_vectores, "Cifrar [1,0,0]=BAA", lambda: self._cifrar_vector(0), color=COLOR_ACENTO, ancho=24)
        boton_v0.pack(pady=3, padx=5, fill=tk.X)

        boton_v1 = BotonEstilizado(marco_vectores, "Cifrar [0,1,0]=ABA", lambda: self._cifrar_vector(1), color=COLOR_ACENTO, ancho=24)
        boton_v1.pack(pady=3, padx=5, fill=tk.X)

        boton_v2 = BotonEstilizado(marco_vectores, "Cifrar [0,0,1]=AAB", lambda: self._cifrar_vector(2), color=COLOR_ACENTO, ancho=24)
        boton_v2.pack(pady=3, padx=5, fill=tk.X)

        separador2 = tk.Frame(marco_vectores, bg=COLOR_SEPARADOR, height=1)
        separador2.pack(fill=tk.X, padx=5, pady=8)

        boton_todos = BotonEstilizado(marco_vectores, "Cifrar Todos", self._cifrar_todos, color="#e94560")
        boton_todos.pack(pady=3, padx=5, fill=tk.X)

        titulo_resultado = tk.Label(panel_derecho, text="Resultado paso a paso:", bg=COLOR_PANEL, fg=COLOR_TEXTO_SECUNDARIO, font=FUENTE_SUBTITULO)
        titulo_resultado.pack(pady=(10, 5), padx=10, anchor="w")

        self.caja_resultado = CajaTexto(panel_derecho, alto=25)
        self.caja_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def establecer_controlador(self, controller):
        self.controller = controller

    def obtener_clave(self):
        resultado = []
        for i in range(3):
            fila = []
            for j in range(3):
                fila.append(self.entradas_clave[i][j].get())
            resultado.append(fila)
        return resultado

    def mostrar_resultado(self, texto):
        self.caja_resultado.actualizar(texto)

    def mostrar_error(self, mensaje):
        self.etiqueta_estado.config(text=mensaje, fg=COLOR_ERROR)

    def limpiar(self):
        for i in range(3):
            for j in range(3):
                self.entradas_clave[i][j].delete(0, tk.END)
        self.etiqueta_estado.config(text="")
        self.caja_resultado.actualizar("")

    def _establecer_clave(self):
        if self.controller:
            self.controller.establecer_clave()

    def _cifrar_vector(self, indice):
        if self.controller:
            self.controller.cifrar_vector(indice)

    def _cifrar_todos(self):
        if self.controller:
            self.controller.cifrar_todos()