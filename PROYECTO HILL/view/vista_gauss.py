import tkinter as tk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_TEXTO, COLOR_TEXTO_SECUNDARIO,
    COLOR_EXITO, COLOR_ERROR, COLOR_SEPARADOR, COLOR_INFO,
    FUENTE_SUBTITULO, FUENTE_NORMAL,
    BotonEstilizado, EntradaEstilizada, EtiquetaTitulo, EtiquetaSubtitulo, CajaTexto, RadioEstilizado
)


class VistaGaussJordan(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLOR_FONDO)
        self.controller = None
        self.paso_actual = 0
        self.total_pasos = 0
        self._crear_interfaz()

    def _crear_interfaz(self):
        titulo = EtiquetaTitulo(self, "Simulador de Ataque Gauss-Jordan")
        titulo.pack(pady=(10, 5), padx=10)

        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        panel_izquierdo = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5), pady=5)

        panel_derecho = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        self._crear_panel_configuracion(panel_izquierdo)
        self._crear_panel_simulacion(panel_derecho)

    def _crear_panel_configuracion(self, padre):
        etiqueta_config = EtiquetaSubtitulo(padre, "Configuración", bg=COLOR_PANEL)
        etiqueta_config.pack(pady=(10, 10), padx=10, anchor="w")

        marco_entrada = tk.Frame(padre, bg=COLOR_PANEL)
        marco_entrada.pack(padx=10, pady=5, fill=tk.X)

        etiqueta_claro = tk.Label(marco_entrada, text="Texto claro:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        etiqueta_claro.pack(anchor="w", pady=(5, 2))
        self.entrada_claro = EntradaEstilizada(marco_entrada, width=30)
        self.entrada_claro.pack(fill=tk.X, pady=(0, 5))

        etiqueta_cifrado = tk.Label(marco_entrada, text="Texto cifrado:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        etiqueta_cifrado.pack(anchor="w", pady=(5, 2))
        self.entrada_cifrado = EntradaEstilizada(marco_entrada, width=30)
        self.entrada_cifrado.pack(fill=tk.X, pady=(0, 10))

        separador1 = tk.Frame(marco_entrada, bg=COLOR_SEPARADOR, height=1)
        separador1.pack(fill=tk.X, pady=5)

        etiqueta_n = tk.Label(marco_entrada, text="Tamaño de bloque:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        etiqueta_n.pack(anchor="w", pady=(5, 5))

        self.variable_n = tk.IntVar(value=2)
        marco_radio = tk.Frame(marco_entrada, bg=COLOR_PANEL)
        marco_radio.pack(anchor="w", pady=(0, 10))

        radio2 = RadioEstilizado(marco_radio, "n = 2", self.variable_n, 2)
        radio2.pack(side=tk.LEFT, padx=(0, 15))
        radio3 = RadioEstilizado(marco_radio, "n = 3", self.variable_n, 3)
        radio3.pack(side=tk.LEFT)

        separador2 = tk.Frame(marco_entrada, bg=COLOR_SEPARADOR, height=1)
        separador2.pack(fill=tk.X, pady=5)

        boton_ejemplo = BotonEstilizado(marco_entrada, "Cargar ejemplo", self._cargar_ejemplo, color=COLOR_ACENTO)
        boton_ejemplo.pack(fill=tk.X, pady=5)

        boton_construir = BotonEstilizado(marco_entrada, "Construir matriz", self._construir_matriz, color=COLOR_ACENTO)
        boton_construir.pack(fill=tk.X, pady=3)

        boton_ataque = BotonEstilizado(marco_entrada, "Ejecutar ataque", self._ejecutar_ataque, color="#e94560")
        boton_ataque.pack(fill=tk.X, pady=3)

        boton_reiniciar = BotonEstilizado(marco_entrada, "Reiniciar", self._reiniciar, color=COLOR_SEPARADOR)
        boton_reiniciar.pack(fill=tk.X, pady=3)

    def _crear_panel_simulacion(self, padre):
        etiqueta_sim = EtiquetaSubtitulo(padre, "Simulación paso a paso", bg=COLOR_PANEL)
        etiqueta_sim.pack(pady=(10, 5), padx=10, anchor="w")

        self.caja_simulacion = CajaTexto(padre, alto=18)
        self.caja_simulacion.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        marco_navegacion = tk.Frame(padre, bg=COLOR_PANEL)
        marco_navegacion.pack(pady=(5, 5), padx=10, fill=tk.X)

        boton_primero = BotonEstilizado(marco_navegacion, "Primero", self._ir_primero, color=COLOR_SEPARADOR, ancho=10)
        boton_primero.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        boton_anterior = BotonEstilizado(marco_navegacion, "Anterior", self._ir_anterior, color=COLOR_SEPARADOR, ancho=10)
        boton_anterior.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        boton_siguiente = BotonEstilizado(marco_navegacion, "Siguiente", self._ir_siguiente, color=COLOR_ACENTO, ancho=10)
        boton_siguiente.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        boton_ultimo = BotonEstilizado(marco_navegacion, "Último", self._ir_ultimo, color=COLOR_ACENTO, ancho=10)
        boton_ultimo.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        separador = tk.Frame(padre, bg=COLOR_SEPARADOR, height=1)
        separador.pack(fill=tk.X, padx=10, pady=5)

        self.etiqueta_clave = tk.Label(padre, text="", bg=COLOR_PANEL, fg=COLOR_EXITO, font=FUENTE_NORMAL)
        self.etiqueta_clave.pack(pady=(5, 10), padx=10, anchor="w")

    def establecer_controlador(self, controller):
        self.controller = controller

    def obtener_texto_claro(self):
        return self.entrada_claro.get()

    def obtener_texto_cifrado(self):
        return self.entrada_cifrado.get()

    def obtener_n(self):
        return self.variable_n.get()

    def mostrar_matriz_inicial(self, texto):
        self.caja_simulacion.actualizar(texto)

    def mostrar_paso(self, descripcion, texto_antes, texto_despues, paso_num, total_pasos, n):
        self.paso_actual = paso_num
        self.total_pasos = total_pasos
        contenido = f"Paso {paso_num}/{total_pasos}: {descripcion}\n\n"
        contenido += "Matriz antes:\n"
        contenido += texto_antes + "\n\n"
        contenido += "Matriz después:\n"
        contenido += texto_despues
        self.caja_simulacion.actualizar(contenido)

    def mostrar_clave(self, texto):
        self.etiqueta_clave.config(text=texto, fg=COLOR_EXITO)

    def mostrar_error(self, mensaje):
        self.caja_simulacion.actualizar(f"Error: {mensaje}", COLOR_ERROR)

    def mostrar_info(self, mensaje):
        self.caja_simulacion.actualizar(mensaje, COLOR_INFO)

    def _cargar_ejemplo(self):
        if self.controller:
            self.controller.cargar_ejemplo()

    def _construir_matriz(self):
        if self.controller:
            self.controller.construir_matriz()

    def _ejecutar_ataque(self):
        if self.controller:
            self.controller.ejecutar_ataque()

    def _reiniciar(self):
        if self.controller:
            self.controller.reiniciar()

    def _ir_primero(self):
        if self.controller:
            self.controller.ir_al_primero()

    def _ir_anterior(self):
        if self.controller:
            self.controller.paso_anterior()

    def _ir_siguiente(self):
        if self.controller:
            self.controller.siguiente_paso()

    def _ir_ultimo(self):
        if self.controller:
            self.controller.ir_al_ultimo()