import tkinter as tk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_PANEL_CLARO, COLOR_ACENTO, COLOR_TEXTO, COLOR_TEXTO_SECUNDARIO,
    COLOR_EXITO, COLOR_ERROR, COLOR_SEPARADOR,
    FUENTE_SUBTITULO, FUENTE_NORMAL,
    BotonEstilizado, EntradaEstilizada, EtiquetaTitulo, CajaTexto
)


class VistaMatrizInversa(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLOR_FONDO)
        self.controller = None
        self.tamano_actual = 2
        self.entradas_matriz = []
        self._crear_interfaz()

    def _crear_interfaz(self):
        titulo = EtiquetaTitulo(self, "Calculador de Matriz Inversa (Mod 27)")
        titulo.pack(pady=(10, 5), padx=10)

        panel_superior = tk.Frame(self, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_superior.pack(fill=tk.X, padx=10, pady=(0, 5))

        marco_tamano = tk.Frame(panel_superior, bg=COLOR_PANEL)
        marco_tamano.pack(pady=10, padx=15, fill=tk.X)

        etiqueta_tamano = tk.Label(marco_tamano, text="Tamano de matriz (n):", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_SUBTITULO)
        etiqueta_tamano.pack(side=tk.LEFT, padx=(0, 10))

        self.spin_tamano = tk.Spinbox(marco_tamano, from_=2, to=3, width=5, font=FUENTE_NORMAL,
                                       bg="#3b3b54", fg=COLOR_TEXTO, insertbackground="white",
                                       relief="solid", bd=2, highlightthickness=2,
                                       highlightcolor=COLOR_ACENTO, highlightbackground="#555570",
                                       buttonbackground=COLOR_PANEL)
        self.spin_tamano.delete(0, tk.END)
        self.spin_tamano.insert(0, "2")

        boton_crear = BotonEstilizado(marco_tamano, "Crear Matriz", self._crear_matriz_btn, color=COLOR_ACENTO)
        boton_crear.pack(side=tk.LEFT, padx=15)

        self.marco_cuadricula = tk.Frame(panel_superior, bg=COLOR_PANEL)
        self.marco_cuadricula.pack(padx=15, pady=5)

        self._crear_cuadricula_entrada(2)

        boton_guardar = BotonEstilizado(panel_superior, "Guardar Datos", self._guardar_datos, color=COLOR_PANEL_CLARO)
        boton_guardar.pack(pady=(5, 10), padx=15)

        marco_botones = tk.Frame(panel_superior, bg=COLOR_PANEL)
        marco_botones.pack(pady=(0, 10), padx=15, fill=tk.X)

        boton_det = BotonEstilizado(marco_botones, "Determinante", self._calcular_det, color=COLOR_ACENTO)
        boton_det.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        boton_adj = BotonEstilizado(marco_botones, "Adjunta", self._calcular_adj, color=COLOR_ACENTO)
        boton_adj.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        boton_inv = BotonEstilizado(marco_botones, "Inversa", self._calcular_inv, color="#e94560")
        boton_inv.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        separador = tk.Frame(self, bg=COLOR_SEPARADOR, height=2)
        separador.pack(fill=tk.X, padx=10, pady=10)

        titulo_resultado = tk.Label(self, text="Resultado:", bg=COLOR_FONDO, fg=COLOR_TEXTO_SECUNDARIO, font=FUENTE_SUBTITULO)
        titulo_resultado.pack(anchor="w", padx=15, pady=(0, 5))

        self.caja_resultado = CajaTexto(self, alto=15)
        self.caja_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def establecer_controlador(self, controller):
        self.controller = controller

    def _crear_matriz_btn(self):
        try:
            n = int(self.spin_tamano.get())
        except ValueError:
            n = 2
        if n < 2:
            n = 2
        if n > 3:
            n = 3
        self.tamano_actual = n
        if self.controller:
            self.controller.crear_matriz()
        else:
            self._crear_cuadricula_entrada(n)

    def _crear_cuadricula_entrada(self, n):
        self.tamano_actual = n
        for widget in self.marco_cuadricula.winfo_children():
            widget.destroy()
        self.entradas_matriz = []
        for i in range(n):
            fila = []
            for j in range(n):
                entrada = EntradaEstilizada(self.marco_cuadricula, width=5, justify="center")
                entrada.grid(row=i, column=j, padx=3, pady=3)
                fila.append(entrada)
            self.entradas_matriz.append(fila)

    def _guardar_datos(self):
        if self.controller:
            self.controller.guardar_datos()

    def _calcular_det(self):
        if self.controller:
            self.controller.calcular_determinante()

    def _calcular_adj(self):
        if self.controller:
            self.controller.calcular_adjunta()

    def _calcular_inv(self):
        if self.controller:
            self.controller.calcular_inversa()

    def obtener_tamano(self):
        return self.tamano_actual

    def obtener_valores(self):
        resultado = []
        for i in range(self.tamano_actual):
            fila = []
            for j in range(self.tamano_actual):
                fila.append(self.entradas_matriz[i][j].get())
            resultado.append(fila)
        return resultado

    def mostrar_resultado(self, texto):
        self.caja_resultado.actualizar(texto)

    def mostrar_error(self, mensaje):
        self.caja_resultado.actualizar(mensaje, COLOR_ERROR)