import tkinter as tk
from estilos import (
    COLOR_FONDO, COLOR_PANEL, COLOR_ACENTO, COLOR_TEXTO, COLOR_TEXTO_SECUNDARIO,
    COLOR_EXITO, COLOR_ERROR, COLOR_INFO, COLOR_SEPARADOR,
    FUENTE_SUBTITULO, FUENTE_NORMAL,
    BotonEstilizado, EntradaEstilizada, EtiquetaTitulo, EtiquetaSubtitulo, CajaTexto, RadioEstilizado
)


class VistaCifraHill(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre, bg=COLOR_FONDO)
        self.controller = None
        self._crear_interfaz()

    def _crear_interfaz(self):
        titulo = EtiquetaTitulo(self, "Cifrado Hill 2×2")
        titulo.pack(pady=(10, 5), padx=10)

        marco_modulo = tk.Frame(self, bg=COLOR_FONDO)
        marco_modulo.pack(pady=(0, 5), padx=10, anchor="w")

        etiqueta_modulo = tk.Label(marco_modulo, text="Módulo:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        etiqueta_modulo.pack(side=tk.LEFT, padx=(10, 5))

        self.variable_modulo = tk.IntVar(value=27)
        radio27 = RadioEstilizado(marco_modulo, "Mod 27 (con Ñ)", self.variable_modulo, 27)
        radio27.pack(side=tk.LEFT, padx=5)
        radio191 = RadioEstilizado(marco_modulo, "Mod 191 (CP437)", self.variable_modulo, 191)
        radio191.pack(side=tk.LEFT, padx=5)

        self.variable_modulo.trace_add("write", self._modulo_cambiado)

        contenedor = tk.Frame(self, bg=COLOR_FONDO)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        panel_izquierdo = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)

        panel_derecho = tk.Frame(contenedor, bg=COLOR_PANEL, relief="flat", bd=0)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        self._crear_panel_izquierdo(panel_izquierdo)
        self._crear_panel_derecho(panel_derecho)

    def _crear_panel_izquierdo(self, padre):
        etiqueta_modo_clave = EtiquetaSubtitulo(padre, "Modo de clave:", bg=COLOR_PANEL)
        etiqueta_modo_clave.pack(pady=(10, 5), padx=10, anchor="w")

        marco_modo = tk.Frame(padre, bg=COLOR_PANEL)
        marco_modo.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.variable_modo_clave = tk.StringVar(value="simbolica")
        radio_sim = RadioEstilizado(marco_modo, "Simbólica", self.variable_modo_clave, "simbolica")
        radio_sim.pack(side=tk.LEFT, padx=(0, 15))
        radio_num = RadioEstilizado(marco_modo, "Numérica", self.variable_modo_clave, "numerica")
        radio_num.pack(side=tk.LEFT)

        self.variable_modo_clave.trace_add("write", self._modo_clave_cambiado)

        self.marco_clave_sim = tk.Frame(padre, bg=COLOR_PANEL)
        self.marco_clave_sim.pack(padx=10, pady=5, fill=tk.X)

        etiqueta_sim = tk.Label(self.marco_clave_sim, text="Clave (4 letras, ej: GATO):", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        etiqueta_sim.pack(anchor="w", pady=(0, 3))
        self.entrada_clave_sim = EntradaEstilizada(self.marco_clave_sim, width=10, justify="center")
        self.entrada_clave_sim.pack(anchor="w")

        self.marco_clave_num = tk.Frame(padre, bg=COLOR_PANEL)
        self.marco_clave_num.pack(padx=10, pady=5, fill=tk.X)

        etiqueta_num = tk.Label(self.marco_clave_num, text="Matriz 2×2:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        etiqueta_num.pack(anchor="w", pady=(0, 3))
        cuadricula = tk.Frame(self.marco_clave_num, bg=COLOR_PANEL)
        cuadricula.pack(anchor="w")
        self.entradas_numericas = []
        for i in range(2):
            fila = []
            for j in range(2):
                entrada = EntradaEstilizada(cuadricula, width=5, justify="center")
                entrada.grid(row=i, column=j, padx=3, pady=3)
                fila.append(entrada)
            self.entradas_numericas.append(fila)
        self.marco_clave_num.pack_forget()

        boton_establecer = BotonEstilizado(padre, "Establecer Clave", self._establecer_clave, color=COLOR_ACENTO)
        boton_establecer.pack(padx=10, pady=5, fill=tk.X)

        self.etiqueta_estado = tk.Label(padre, text="", bg=COLOR_PANEL, fg=COLOR_EXITO, font=FUENTE_NORMAL)
        self.etiqueta_estado.pack(padx=10, pady=(0, 5))

        separador1 = tk.Frame(padre, bg=COLOR_SEPARADOR, height=1)
        separador1.pack(fill=tk.X, padx=10, pady=8)

        etiqueta_texto = EtiquetaSubtitulo(padre, "Texto de entrada:", bg=COLOR_PANEL)
        etiqueta_texto.pack(pady=(0, 3), padx=10, anchor="w")

        self.caja_texto = CajaTexto(padre, alto=5)
        self.caja_texto.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.caja_texto.config(state="normal")

        marco_botones = tk.Frame(padre, bg=COLOR_PANEL)
        marco_botones.pack(padx=10, pady=5, fill=tk.X)

        boton_cifrar = BotonEstilizado(marco_botones, "Cifrar", self._cifrar, color=COLOR_ACENTO)
        boton_cifrar.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        boton_descifrar = BotonEstilizado(marco_botones, "Descifrar", self._descifrar, color="#e94560")
        boton_descifrar.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        boton_limpiar = BotonEstilizado(marco_botones, "Limpiar", self._limpiar, color=COLOR_SEPARADOR)
        boton_limpiar.pack(side=tk.LEFT, padx=3, expand=True, fill=tk.X)

        separador2 = tk.Frame(padre, bg=COLOR_SEPARADOR, height=1)
        separador2.pack(fill=tk.X, padx=10, pady=8)

        etiqueta_resultado = EtiquetaSubtitulo(padre, "Resultado:", bg=COLOR_PANEL)
        etiqueta_resultado.pack(pady=(0, 3), padx=10, anchor="w")

        self.caja_resultado = CajaTexto(padre, alto=5)
        self.caja_resultado.pack(fill=tk.X, padx=10, pady=(0, 10))

    def _crear_panel_derecho(self, padre):
        etiqueta_sim = EtiquetaSubtitulo(padre, "Simulación paso a paso:", bg=COLOR_PANEL)
        etiqueta_sim.pack(pady=(10, 3), padx=10, anchor="w")

        self.caja_simulacion = CajaTexto(padre, alto=25)
        self.caja_simulacion.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def _modulo_cambiado(self, *args):
        if self.controller:
            self.controller.cambiar_modulo(self.variable_modulo.get())

    def _modo_clave_cambiado(self, *args):
        if self.variable_modo_clave.get() == "simbolica":
            self.marco_clave_num.pack_forget()
            self.marco_clave_sim.pack(padx=10, pady=5, fill=tk.X)
        else:
            self.marco_clave_sim.pack_forget()
            self.marco_clave_num.pack(padx=10, pady=5, fill=tk.X)

    def establecer_controlador(self, controller):
        self.controller = controller

    def obtener_modulo(self):
        return self.variable_modulo.get()

    def obtener_modo_clave(self):
        return self.variable_modo_clave.get()

    def obtener_clave_simbolica(self):
        return self.entrada_clave_sim.get()

    def obtener_valores_numericos(self):
        resultado = []
        for i in range(2):
            fila = []
            for j in range(2):
                fila.append(self.entradas_numericas[i][j].get())
            resultado.append(fila)
        return resultado

    def obtener_texto(self):
        return self.caja_texto.get("1.0", tk.END).strip()

    def mostrar_resultado(self, texto, color=COLOR_TEXTO):
        self.caja_resultado.actualizar(texto, color)

    def mostrar_estado_clave(self, mensaje, color=COLOR_EXITO):
        self.etiqueta_estado.config(text=mensaje, fg=color)

    def mostrar_pasos_cifrado(self, pasos):
        contenido = ""
        for paso in pasos:
            contenido += paso + "\n"
        self.caja_simulacion.actualizar(contenido)

    def mostrar_pasos_descifrado(self, pasos):
        contenido = ""
        for paso in pasos:
            contenido += paso + "\n"
        self.caja_simulacion.actualizar(contenido)

    def mostrar_info_clave(self, info):
        self.etiqueta_estado.config(text=info, fg=COLOR_INFO)

    def limpiar_campos(self):
        self.entrada_clave_sim.delete(0, tk.END)
        for i in range(2):
            for j in range(2):
                self.entradas_numericas[i][j].delete(0, tk.END)
        self.caja_texto.delete("1.0", tk.END)
        self.caja_resultado.actualizar("")
        self.caja_simulacion.actualizar("")
        self.etiqueta_estado.config(text="")

    def _establecer_clave(self):
        if self.controller:
            self.controller.establecer_clave()

    def _cifrar(self):
        if self.controller:
            self.controller.cifrar()

    def _descifrar(self):
        if self.controller:
            self.controller.descifrar()

    def _limpiar(self):
        if self.controller:
            self.controller.limpiar()