import tkinter as tk
from tkinter import messagebox, ttk

class Vista(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Ataque Gauss‑Jordan – Cifrado Hill")
        self.geometry("900x700")
        self.controlador = None   # se enlazará luego

        # Variables de control
        self.tamano = tk.IntVar(value=2)
        self.modo_entrada = tk.StringVar(value="letras")
        self.datos_plano = []
        self.datos_cifrado = []

        self.crear_widgets()

    def set_controlador(self, controlador):
        self.controlador = controlador

    def crear_widgets(self):
        # Frame superior: configuración
        frame_config = tk.LabelFrame(self, text="Configuración", padx=10, pady=10)
        frame_config.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_config, text="Tamaño de matriz (n):").grid(row=0, column=0, sticky="w")
        self.spin_n = tk.Spinbox(frame_config, from_=2, to=5, textvariable=self.tamano, width=5)
        self.spin_n.grid(row=0, column=1, sticky="w")

        tk.Label(frame_config, text="Modo de entrada:").grid(row=1, column=0, sticky="w")
        self.rb_letras = tk.Radiobutton(frame_config, text="Letras (A-Z)", variable=self.modo_entrada, value="letras")
        self.rb_letras.grid(row=1, column=1, sticky="w")
        self.rb_numeros = tk.Radiobutton(frame_config, text="Números (0-25)", variable=self.modo_entrada, value="numeros")
        self.rb_numeros.grid(row=1, column=2, sticky="w")

        self.btn_config = tk.Button(frame_config, text="Cargar matrices", command=self.on_cargar_matrices)
        self.btn_config.grid(row=2, column=0, columnspan=3, pady=5)

        # Frame medio: entrada de matrices
        self.frame_entrada = tk.LabelFrame(self, text="Matrices de entrada", padx=10, pady=10)
        self.frame_entrada.pack(fill="both", expand=False, padx=10, pady=5)

        self.entradas_plano = []
        self.entradas_cifrado = []

        # Frame de pasos y navegación
        frame_pasos = tk.LabelFrame(self, text="Proceso paso a paso", padx=10, pady=10)
        frame_pasos.pack(fill="both", expand=True, padx=10, pady=5)

        self.lbl_descripcion = tk.Label(frame_pasos, text="", wraplength=800, justify="left")
        self.lbl_descripcion.pack(anchor="w")

        self.frame_matriz = tk.Frame(frame_pasos)
        self.frame_matriz.pack(pady=10)

        # Botones de navegación
        frame_nav = tk.Frame(frame_pasos)
        frame_nav.pack()

        self.btn_anterior = tk.Button(frame_nav, text="◀ Paso anterior", command=self.paso_anterior, state="disabled")
        self.btn_anterior.grid(row=0, column=0, padx=5)

        self.btn_siguiente = tk.Button(frame_nav, text="Paso siguiente ▶", command=self.paso_siguiente, state="disabled")
        self.btn_siguiente.grid(row=0, column=1, padx=5)

        self.btn_reiniciar = tk.Button(frame_nav, text="Reiniciar", command=self.reiniciar, state="disabled")
        self.btn_reiniciar.grid(row=0, column=2, padx=5)

        self.lbl_estado = tk.Label(frame_pasos, text="")
        self.lbl_estado.pack(pady=5)

    def on_cargar_matrices(self):
        """Recolecta los valores ingresados según el modo y los pasa al controlador."""
        n = self.tamano.get()
        try:
            if self.modo_entrada.get() == "letras":
                # Leer bloques como letras separadas por espacios
                plano_filas = []
                cifrado_filas = []
                for i in range(n):
                    fila_plano = self.entradas_plano[i].get().strip().upper().split()
                    fila_cifrado = self.entradas_cifrado[i].get().strip().upper().split()
                    if len(fila_plano) != n or len(fila_cifrado) != n:
                        raise ValueError(f"La fila {i+1} debe tener exactamente {n} elementos.")
                    # Validar que sean letras
                    plano_filas.append(fila_plano)
                    cifrado_filas.append(fila_cifrado)
                self.controlador.cargar_matrices_desde_letras(plano_filas, cifrado_filas)
            else:
                # Modo números
                plano_filas = []
                cifrado_filas = []
                for i in range(n):
                    fila_plano = [int(x) for x in self.entradas_plano[i].get().strip().split()]
                    fila_cifrado = [int(x) for x in self.entradas_cifrado[i].get().strip().split()]
                    if len(fila_plano) != n or len(fila_cifrado) != n:
                        raise ValueError(f"La fila {i+1} debe tener exactamente {n} números.")
                    plano_filas.append(fila_plano)
                    cifrado_filas.append(fila_cifrado)
                self.controlador.cargar_matrices_desde_numeros(plano_filas, cifrado_filas)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Éxito", "Matrices cargadas. Pulse 'Iniciar simulación'.")

    def habilitar_controles(self, estado):
        self.btn_anterior.config(state="normal" if estado else "disabled")
        self.btn_siguiente.config(state="normal" if estado else "disabled")
        self.btn_reiniciar.config(state="normal" if estado else "disabled")

    def mostrar_paso(self, paso):
        """Muestra un paso: descripción y matriz."""
        self.lbl_descripcion.config(text=paso['descripcion'])
        matriz = paso['matriz']
        self.dibujar_matriz(matriz)

    def dibujar_matriz(self, matriz):
        """Dibuja la matriz aumentada en el frame_matriz."""
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()
        n = matriz.filas
        m = matriz.columnas
        # Dividir visualmente la parte izquierda (P) y derecha (C)
        mitad = self.controlador.modelo.n if self.controlador else n // 2
        for i in range(n):
            for j in range(m):
                valor = matriz[i][j]
                # Color de fondo: izquierda (P) gris claro, derecha (C) gris oscuro
                bg = "#d9ead3" if j < mitad else "#cfe2f3"
                etiq = tk.Label(self.frame_matriz, text=str(valor), width=5, relief="ridge", bg=bg)
                etiq.grid(row=i, column=j, padx=1, pady=1)

    def paso_siguiente(self):
        if self.controlador:
            self.controlador.avanzar_paso()

    def paso_anterior(self):
        if self.controlador:
            self.controlador.retroceder_paso()

    def reiniciar(self):
        if self.controlador:
            self.controlador.reiniciar_simulacion()

    def crear_cuadricula_entrada(self, n):
        """Recrea los campos de entrada para las matrices de tamaño n x n."""
        for widget in self.frame_entrada.winfo_children():
            widget.destroy()
        self.entradas_plano.clear()
        self.entradas_cifrado.clear()

        tk.Label(self.frame_entrada, text="Texto claro (P)", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10)
        tk.Label(self.frame_entrada, text="Texto cifrado (C)", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10)

        for i in range(n):
            # Una sola caja de texto por fila para el texto claro
            e_p = tk.Entry(self.frame_entrada, width=20)
            e_p.grid(row=i+1, column=0, padx=5, pady=2)
            self.entradas_plano.append(e_p)
            
            # Una sola caja de texto por fila para el texto cifrado
            e_c = tk.Entry(self.frame_entrada, width=20)
            e_c.grid(row=i+1, column=1, padx=5, pady=2)
            self.entradas_cifrado.append(e_c)

        # Botón para iniciar simulación
        self.btn_iniciar = tk.Button(self.frame_entrada, text="Iniciar simulación", command=self.iniciar_simulacion)
        self.btn_iniciar.grid(row=n+1, column=0, columnspan=2, pady=10)

    def iniciar_simulacion(self):
        """Ya se cargaron las matrices, ejecuta Gauss‑Jordan."""
        if self.controlador:
            self.controlador.iniciar_simulacion()
