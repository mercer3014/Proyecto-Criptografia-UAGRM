"""
Vista del simulador de ataque Gauss-Jordan.

Construye y gestiona toda la interfaz gráfica usando Tkinter.
No contiene lógica criptográfica; se comunica con el controlador.

Patrón: Vista en MVC.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Callable


# ---------------------------------------------------------------------------
# Constantes de diseño
# ---------------------------------------------------------------------------

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
COLOR_RESULTADO = "#a6e3a1"

FUENTE_TITULO = ("Segoe UI", 14, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 11, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
FUENTE_MONO = ("Consolas", 11)
FUENTE_MONO_GRANDE = ("Consolas", 12, "bold")
FUENTE_PEQUENA = ("Segoe UI", 9)
FUENTE_PASO = ("Segoe UI", 10, "bold")


# ---------------------------------------------------------------------------
# Widgets personalizados reutilizables
# ---------------------------------------------------------------------------

class BotonEstilizado(tk.Button):
    """Botón con estilo coherente al tema de la aplicación."""

    def __init__(
        self,
        padre,
        texto: str,
        comando: Callable,
        color: str = COLOR_ACENTO,
        ancho: int = 0,
        **kwargs
    ) -> None:
        super().__init__(
            padre,
            text=texto,
            command=comando,
            bg=color,
            fg=COLOR_TEXTO,
            font=FUENTE_NORMAL,
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            activebackground=COLOR_ACENTO_HOVER,
            activeforeground=COLOR_TEXTO,
            bd=0,
            **kwargs
        )
        self._color_original = color
        if ancho:
            self.config(width=ancho)
        self.bind("<Enter>", lambda e: self.config(bg=COLOR_ACENTO_HOVER))
        self.bind("<Leave>", lambda e: self.config(bg=self._color_original))


class EntradaEstilizada(tk.Entry):
    """Campo de entrada con estilo coherente al tema."""

    def __init__(self, padre, **kwargs) -> None:
        super().__init__(
            padre,
            bg=COLOR_PANEL_CLARO,
            fg=COLOR_TEXTO,
            insertbackground=COLOR_TEXTO,
            font=FUENTE_MONO,
            relief="flat",
            bd=6,
            highlightthickness=1,
            highlightcolor=COLOR_ACENTO,
            highlightbackground=COLOR_SEPARADOR,
            **kwargs
        )


class EtiquetaTitulo(tk.Label):
    """Etiqueta para títulos de sección."""

    def __init__(self, padre, texto: str, **kwargs) -> None:
        super().__init__(
            padre,
            text=texto,
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO,
            font=FUENTE_TITULO,
            **kwargs
        )


class EtiquetaSubtitulo(tk.Label):
    """Etiqueta para subtítulos."""

    def __init__(self, padre, texto: str, **kwargs) -> None:
        bg = kwargs.pop("bg", COLOR_FONDO)
        super().__init__(
            padre,
            text=texto,
            bg=bg,
            fg=COLOR_TEXTO,
            font=FUENTE_SUBTITULO,
            **kwargs
        )


class CajaTexto(scrolledtext.ScrolledText):
    """Área de texto multilínea con scroll y estilo."""

    def __init__(self, padre, alto: int = 8, **kwargs) -> None:
        super().__init__(
            padre,
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            font=FUENTE_MONO,
            relief="flat",
            bd=4,
            height=alto,
            wrap=tk.WORD,
            state="disabled",
            highlightthickness=1,
            highlightcolor=COLOR_SEPARADOR,
            highlightbackground=COLOR_PANEL,
            insertbackground=COLOR_TEXTO,
            selectbackground=COLOR_ACENTO,
            selectforeground=COLOR_TEXTO,
            **kwargs
        )
        self._alto = alto

    def actualizar(self, texto: str, color: str = COLOR_TEXTO) -> None:
        """Reemplaza el contenido con el texto dado."""
        self.config(state="normal")
        self.delete("1.0", tk.END)
        self.insert(tk.END, texto)
        self.config(state="disabled", fg=color)


# ---------------------------------------------------------------------------
# Vista principal
# ---------------------------------------------------------------------------

class VistaPrincipal:
    """
    Vista completa del simulador de ataque Gauss-Jordan.

    Organizada en tres pestañas:
        1. Configuración: ingreso de datos y construcción de la matriz.
        2. Simulación: navegación paso a paso de Gauss-Jordan.
        3. Verificación: cifrar/descifrar con la clave recuperada.

    Atributos:
        raiz: Ventana principal de Tkinter.
        controlador: Referencia al controlador (se asigna externamente).
    """

    def __init__(self) -> None:
        self.raiz = tk.Tk()
        self.raiz.title("Simulador de Ataque Gauss-Jordan — Cifrado Hill")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.geometry("980x720")
        self.raiz.minsize(850, 650)

        self.controlador = None

        # Variables Tkinter
        self._var_texto_claro = tk.StringVar()
        self._var_texto_cifrado = tk.StringVar()
        self._var_n = tk.IntVar(value=2)
        self._var_verificar_entrada = tk.StringVar()
        self._var_modo_verificar = tk.StringVar(value="cifrar")

        self._construir_interfaz()

        # Bindings de teclado para navegación
        self.raiz.bind("<Left>", lambda e: self._on_anterior())
        self.raiz.bind("<Right>", lambda e: self._on_siguiente())
        self.raiz.bind("<Home>", lambda e: self._on_primer_paso())
        self.raiz.bind("<End>", lambda e: self._on_ultimo_paso())

    # -----------------------------------------------------------------------
    # Construcción de la interfaz
    # -----------------------------------------------------------------------

    def _construir_interfaz(self) -> None:
        """Construye todos los elementos de la interfaz."""
        self._construir_encabezado()
        self._construir_pestanas()

    def _construir_encabezado(self) -> None:
        """Panel de encabezado con título y descripción."""
        frame = tk.Frame(self.raiz, bg=COLOR_PANEL, pady=10)
        frame.pack(fill="x")

        tk.Label(
            frame,
            text="Simulador de Ataque Gauss-Jordan",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            font=("Segoe UI", 17, "bold")
        ).pack()

        tk.Label(
            frame,
            text="Recuperación de clave en el cifrado Hill mediante "
                 "operaciones elementales de fila (mod 26)",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        ).pack(pady=(2, 0))

    def _construir_pestanas(self) -> None:
        """Crea el contenedor de pestañas."""
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure(
            "TNotebook",
            background=COLOR_FONDO,
            borderwidth=0
        )
        estilo.configure(
            "TNotebook.Tab",
            background=COLOR_PANEL,
            foreground=COLOR_TEXTO_SECUNDARIO,
            padding=[18, 8],
            font=FUENTE_NORMAL
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", COLOR_ACENTO)],
            foreground=[("selected", COLOR_TEXTO)]
        )

        self._notebook = ttk.Notebook(self.raiz)
        self._notebook.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self._pestana_configuracion = tk.Frame(
            self._notebook, bg=COLOR_FONDO
        )
        self._pestana_simulacion = tk.Frame(
            self._notebook, bg=COLOR_FONDO
        )
        self._pestana_verificacion = tk.Frame(
            self._notebook, bg=COLOR_FONDO
        )

        self._notebook.add(self._pestana_configuracion, text="  Configuración  ")
        self._notebook.add(self._pestana_simulacion, text="  Simulación paso a paso  ")
        self._notebook.add(self._pestana_verificacion, text="  Verificación  ")

        self._construirpestana_configuracion()
        self._construir_pestanasimulacion()
        self._construir_pestanaverificacion()

    def _construirpestana_configuracion(self) -> None:
        """Pestaña 1: Entrada de datos y vista de la matriz aumentada."""
        padre = self._pestana_configuracion

        # Panel izquierdo: formulario
        panel_form = tk.Frame(padre, bg=COLOR_FONDO, padx=16, pady=12)
        panel_form.pack(side="left", fill="y")

        EtiquetaTitulo(panel_form, "Datos de entrada").pack(anchor="w")

        tk.Label(
            panel_form,
            text=(
                "Para recuperar la clave K de un cifrado Hill n×n,\n"
                "se necesitan al menos n² letras de texto claro y\n"
                "su correspondiente texto cifrado."
            ),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA,
            justify="left"
        ).pack(anchor="w", pady=(4, 12))

        # Tamaño del bloque
        tk.Label(
            panel_form,
            text="Tamaño del bloque (n):",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=FUENTE_NORMAL
        ).pack(anchor="w")

        frame_n = tk.Frame(panel_form, bg=COLOR_FONDO)
        frame_n.pack(anchor="w", pady=(2, 10))

        for valor, texto in [(2, "2×2"), (3, "3×3")]:
            tk.Radiobutton(
                frame_n,
                text=f"  n = {valor}  ({texto})",
                variable=self._var_n,
                value=valor,
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
                selectcolor=COLOR_PANEL,
                activebackground=COLOR_FONDO,
                activeforeground=COLOR_TEXTO,
                font=FUENTE_NORMAL
            ).pack(side="left", padx=4)

        # Texto claro
        tk.Label(
            panel_form,
            text="Texto claro (conocido):",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=FUENTE_NORMAL
        ).pack(anchor="w", pady=(8, 2))

        frame_claro = tk.Frame(panel_form, bg=COLOR_FONDO)
        frame_claro.pack(anchor="w", fill="x")

        EntradaEstilizada(
            frame_claro,
            textvariable=self._var_texto_claro,
            width=28
        ).pack(side="left", padx=(0, 4))

        tk.Label(
            frame_claro,
            text="Solo A-Z",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        ).pack(side="left")

        # Texto cifrado
        tk.Label(
            panel_form,
            text="Texto cifrado (resultado Hill):",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=FUENTE_NORMAL
        ).pack(anchor="w", pady=(10, 2))

        frame_cifrado = tk.Frame(panel_form, bg=COLOR_FONDO)
        frame_cifrado.pack(anchor="w", fill="x")

        EntradaEstilizada(
            frame_cifrado,
            textvariable=self._var_texto_cifrado,
            width=28
        ).pack(side="left", padx=(0, 4))

        tk.Label(
            frame_cifrado,
            text="Mismo largo",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        ).pack(side="left")

        # Separador
        tk.Frame(panel_form, bg=COLOR_SEPARADOR, height=1).pack(fill="x", pady=10)

        # Botones de acción
        EtiquetaSubtitulo(panel_form, "Acciones").pack(anchor="w", pady=(0, 6))

        BotonEstilizado(
            panel_form,
            texto="Cargar ejemplo",
            comando=self._cargar_ejemplo,
            color=COLOR_PANEL_CLARO,
            ancho=22
        ).pack(anchor="w", pady=3)

        BotonEstilizado(
            panel_form,
            texto="Construir matriz [P | C]",
            comando=self._on_construir,
            ancho=22
        ).pack(anchor="w", pady=3)

        BotonEstilizado(
            panel_form,
            texto="Ejecutar ataque completo",
            comando=self._on_ejecutar,
            color="#5a4fcf",
            ancho=22
        ).pack(anchor="w", pady=3)

        BotonEstilizado(
            panel_form,
            texto="Reiniciar",
            comando=self._on_reiniciar,
            color="#6e3535",
            ancho=22
        ).pack(anchor="w", pady=3)

        # Panel derecho: visualización de la matriz
        panel_matriz = tk.Frame(
            padre, bg=COLOR_PANEL, padx=16, pady=12
        )
        panel_matriz.pack(side="right", fill="both", expand=True, padx=(8, 0))

        EtiquetaSubtitulo(
            panel_matriz,
            "Matriz aumentada  [Texto Claro | Texto Cifrado]",
            bg=COLOR_PANEL
        ).pack(anchor="w", pady=(0, 6))

        tk.Label(
            panel_matriz,
            text=(
                "Cada fila corresponde a un bloque de texto.\n"
                "La parte izquierda (║) es el texto claro P,\n"
                "la derecha es el texto cifrado C.\n"
                "Gauss-Jordan transforma P → I para obtener K."
            ),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA,
            justify="left"
        ).pack(anchor="w", pady=(0, 8))

        self._caja_matriz_inicial = CajaTexto(panel_matriz, alto=10)
        self._caja_matriz_inicial.pack(fill="both", expand=True)

        self._etiqueta_estado_config = tk.Label(
            panel_matriz,
            text="",
            bg=COLOR_PANEL,
            font=FUENTE_PEQUENA,
            wraplength=380,
            justify="left"
        )
        self._etiqueta_estado_config.pack(anchor="w", pady=(8, 0))

    def _construir_pestanasimulacion(self) -> None:
        """Pestaña 2: Navegación paso a paso del algoritmo."""
        padre = self._pestana_simulacion

        # Encabezado informativo
        frame_info = tk.Frame(padre, bg=COLOR_PANEL, padx=16, pady=8)
        frame_info.pack(fill="x")

        tk.Label(
            frame_info,
            text="Simulación de Gauss-Jordan modular",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            font=FUENTE_TITULO
        ).pack(side="left")

        self._etiqueta_progreso = tk.Label(
            frame_info,
            text="Paso 0 / 0",
            bg=COLOR_PANEL,
            fg=COLOR_RESALTADO,
            font=FUENTE_MONO_GRANDE
        )
        self._etiqueta_progreso.pack(side="right")

        # Descripción del paso actual
        frame_desc = tk.Frame(padre, bg=COLOR_PANEL, padx=16, pady=6)
        frame_desc.pack(fill="x")

        tk.Label(
            frame_desc,
            text="Operación actual:",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        ).pack(anchor="w")

        self._etiqueta_operacion = tk.Label(
            frame_desc,
            text="Presione 'Ejecutar ataque completo' en la pestaña anterior.",
            bg=COLOR_PANEL,
            fg=COLOR_RESALTADO,
            font=FUENTE_PASO,
            wraplength=900,
            justify="left"
        )
        self._etiqueta_operacion.pack(anchor="w", pady=(2, 0))

        self._etiqueta_tipo_operacion = tk.Label(
            frame_desc,
            text="",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        )
        self._etiqueta_tipo_operacion.pack(anchor="w")

        # Separador
        tk.Frame(padre, bg=COLOR_SEPARADOR, height=1).pack(fill="x")

        # Paneles: antes y después
        frame_matrices = tk.Frame(padre, bg=COLOR_FONDO, padx=12, pady=8)
        frame_matrices.pack(fill="both", expand=True)

        frame_antes = tk.Frame(frame_matrices, bg=COLOR_FONDO)
        frame_antes.pack(side="left", fill="both", expand=True, padx=(0, 6))

        tk.Label(
            frame_antes,
            text="Antes de la operación",
            bg=COLOR_FONDO,
            fg=COLOR_ADVERTENCIA,
            font=FUENTE_SUBTITULO
        ).pack(anchor="w")

        self._caja_antes = CajaTexto(frame_antes, alto=10)
        self._caja_antes.pack(fill="both", expand=True, pady=(4, 0))

        frame_despues = tk.Frame(frame_matrices, bg=COLOR_FONDO)
        frame_despues.pack(side="right", fill="both", expand=True, padx=(6, 0))

        tk.Label(
            frame_despues,
            text="Después de la operación",
            bg=COLOR_FONDO,
            fg=COLOR_EXITO,
            font=FUENTE_SUBTITULO
        ).pack(anchor="w")

        self._caja_despues = CajaTexto(frame_despues, alto=10)
        self._caja_despues.pack(fill="both", expand=True, pady=(4, 0))

        # Clave recuperada
        frame_clave = tk.Frame(padre, bg=COLOR_PANEL, padx=16, pady=6)
        frame_clave.pack(fill="x")

        tk.Label(
            frame_clave,
            text="Clave recuperada K:",
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO,
            font=FUENTE_SUBTITULO
        ).pack(side="left", padx=(0, 10))

        self._etiqueta_clave = tk.Label(
            frame_clave,
            text="(pendiente de calcular)",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_MONO_GRANDE
        )
        self._etiqueta_clave.pack(side="left")

        # Controles de navegación
        frame_nav = tk.Frame(padre, bg=COLOR_FONDO, pady=6)
        frame_nav.pack(fill="x")

        nav_container = tk.Frame(frame_nav, bg=COLOR_FONDO)
        nav_container.pack(anchor="center")

        self._btn_anterior = BotonEstilizado(
            nav_container,
            texto="\u2190 Anterior",
            comando=self._on_anterior,
            color=COLOR_PANEL_CLARO,
            ancho=12
        )
        self._btn_anterior.pack(side="left", padx=4)

        self._btn_siguiente = BotonEstilizado(
            nav_container,
            texto="Siguiente \u2192",
            comando=self._on_siguiente,
            ancho=12
        )
        self._btn_siguiente.pack(side="left", padx=4)

        tk.Frame(nav_container, bg=COLOR_FONDO, width=20).pack(side="left")

        BotonEstilizado(
            nav_container,
            texto="Primero",
            comando=self._on_primer_paso,
            color=COLOR_PANEL_CLARO,
            ancho=10
        ).pack(side="left", padx=4)

        BotonEstilizado(
            nav_container,
            texto="Último",
            comando=self._on_ultimo_paso,
            color=COLOR_PANEL_CLARO,
            ancho=10
        ).pack(side="left", padx=4)

        tk.Label(
            frame_nav,
            text="Teclas: ← → para navegar pasos | Inicio/Fin para ir al primero/último",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        ).pack(pady=(2, 0))

    def _construir_pestanaverificacion(self) -> None:
        """Pestaña 3: Cifrar/descifrar con la clave recuperada."""
        padre = self._pestana_verificacion

        tk.Label(
            padre,
            text=(
                "Una vez recuperada la clave, puede verificar su "
                "corrección cifrando o descifrando texto."
            ),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO_SECUNDARIO,
            font=FUENTE_PEQUENA
        ).pack(anchor="w", padx=16, pady=(10, 4))

        frame_entrada = tk.Frame(padre, bg=COLOR_FONDO, padx=16, pady=8)
        frame_entrada.pack(fill="x")

        tk.Label(
            frame_entrada,
            text="Texto de entrada:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=FUENTE_NORMAL
        ).pack(anchor="w")

        EntradaEstilizada(
            frame_entrada,
            textvariable=self._var_verificar_entrada,
            width=40
        ).pack(anchor="w", pady=4)

        frame_modo = tk.Frame(frame_entrada, bg=COLOR_FONDO)
        frame_modo.pack(anchor="w", pady=6)

        for valor, texto in [("cifrar", "Cifrar"), ("descifrar", "Descifrar")]:
            tk.Radiobutton(
                frame_modo,
                text=f"  {texto}",
                variable=self._var_modo_verificar,
                value=valor,
                bg=COLOR_FONDO,
                fg=COLOR_TEXTO,
                selectcolor=COLOR_PANEL,
                activebackground=COLOR_FONDO,
                activeforeground=COLOR_TEXTO,
                font=FUENTE_NORMAL
            ).pack(side="left", padx=8)

        BotonEstilizado(
            frame_entrada,
            texto="Procesar con clave recuperada",
            comando=self._on_verificar,
            ancho=28
        ).pack(anchor="w", pady=6)

        # Resultado
        tk.Label(
            padre,
            text="Resultado:",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=FUENTE_NORMAL
        ).pack(anchor="w", padx=16)

        self._caja_verificacion = CajaTexto(padre, alto=5)
        self._caja_verificacion.pack(fill="x", padx=16, pady=4)

        # Información de la clave
        frame_info_clave = tk.Frame(padre, bg=COLOR_PANEL, padx=16, pady=10)
        frame_info_clave.pack(fill="both", expand=True, padx=16, pady=8)

        tk.Label(
            frame_info_clave,
            text="Información de la clave recuperada",
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO,
            font=FUENTE_SUBTITULO
        ).pack(anchor="w")

        self._caja_info_clave = CajaTexto(frame_info_clave, alto=8)
        self._caja_info_clave.pack(fill="both", expand=True, pady=6)

    # -----------------------------------------------------------------------
    # Métodos de actualización de la interfaz
    # -----------------------------------------------------------------------

    def mostrar_matriz_inicial(
        self,
        texto: str,
        mensaje: str = "",
        es_error: bool = False
    ) -> None:
        """Muestra la matriz aumentada en la pestaña de configuración."""
        self._caja_matriz_inicial.actualizar(texto)
        color = COLOR_ERROR if es_error else COLOR_EXITO
        self._etiqueta_estado_config.config(
            text=mensaje,
            fg=color
        )

    def actualizar_paso(
        self,
        descripcion_operacion: str,
        tipo_operacion: str,
        texto_antes: str,
        texto_despues: str,
        numero_paso: int,
        total_pasos: int,
        n: int
    ) -> None:
        """Actualiza todos los elementos de la pestaña de simulación."""
        self._etiqueta_operacion.config(text=descripcion_operacion)
        self._etiqueta_tipo_operacion.config(
            text=f"Tipo: {tipo_operacion}"
        )
        self._etiqueta_progreso.config(
            text=f"Paso {numero_paso} / {total_pasos}"
        )
        self._caja_antes.actualizar(texto_antes, COLOR_ADVERTENCIA)
        self._caja_despues.actualizar(texto_despues, COLOR_EXITO)

    def mostrar_clave_recuperada(self, texto_clave: str) -> None:
        """Muestra la clave recuperada en la barra inferior."""
        self._etiqueta_clave.config(
            text=texto_clave,
            fg=COLOR_EXITO
        )

    def mostrar_resultado_verificacion(
        self,
        texto: str,
        es_error: bool = False
    ) -> None:
        """Muestra el resultado en la pestaña de verificación."""
        color = COLOR_ERROR if es_error else COLOR_EXITO
        self._caja_verificacion.actualizar(texto, color)

    def mostrar_info_clave(self, texto: str) -> None:
        """Muestra la información detallada de la clave."""
        self._caja_info_clave.actualizar(texto)

    def ir_a_pestana(self, indice: int) -> None:
        """Navega programáticamente a una pestaña."""
        self._notebook.select(indice)

    def mostrar_error(self, mensaje: str) -> None:
        """Muestra un cuadro de diálogo de error."""
        messagebox.showerror("Error", mensaje)

    def mostrar_info(self, mensaje: str) -> None:
        """Muestra un cuadro de diálogo informativo."""
        messagebox.showinfo("Información", mensaje)

    # -----------------------------------------------------------------------
    # Getters de los campos del formulario
    # -----------------------------------------------------------------------

    def obtener_texto_claro(self) -> str:
        return self._var_texto_claro.get()

    def obtener_texto_cifrado(self) -> str:
        return self._var_texto_cifrado.get()

    def obtener_n(self) -> int:
        return self._var_n.get()

    def obtener_entrada_verificacion(self) -> str:
        return self._var_verificar_entrada.get()

    def obtener_modo_verificar(self) -> str:
        return self._var_modo_verificar.get()

    # -----------------------------------------------------------------------
    # Callbacks internos que delegan al controlador
    # -----------------------------------------------------------------------

    def _on_construir(self) -> None:
        if self.controlador:
            self.controlador.on_construir_matriz()

    def _on_ejecutar(self) -> None:
        if self.controlador:
            self.controlador.on_ejecutar_ataque()

    def _on_siguiente(self) -> None:
        if self.controlador:
            self.controlador.on_siguiente_paso()

    def _on_anterior(self) -> None:
        if self.controlador:
            self.controlador.on_paso_anterior()

    def _on_primer_paso(self) -> None:
        if self.controlador:
            self.controlador.on_ir_a_paso(0)

    def _on_ultimo_paso(self) -> None:
        if self.controlador:
            self.controlador.on_ir_al_ultimo_paso()

    def _on_verificar(self) -> None:
        if self.controlador:
            self.controlador.on_verificar()

    def _on_reiniciar(self) -> None:
        if self.controlador:
            self.controlador.on_reiniciar()

    def _cargar_ejemplo(self) -> None:
        """Carga datos de ejemplo para demostración rápida."""
        # Clave conocida: [[3,3],[2,5]]
        # Texto claro: BIEN → B=1, I=8, E=4, N=13
        # Bloque 1: K*[1,8] = [3*1+3*8, 2*1+5*8] = [27,42] mod 26 = [1,16] = BQ
        # Bloque 2: K*[4,13] = [3*4+3*13, 2*4+5*13] = [51,73] mod 26 = [25,21] = ZV
        # Texto cifrado: BQZV
        self._var_texto_claro.set("BIEN")
        self._var_texto_cifrado.set("BQZV")
        self._var_n.set(2)

    def iniciar(self) -> None:
        """Inicia el bucle principal de Tkinter."""
        self.raiz.mainloop()