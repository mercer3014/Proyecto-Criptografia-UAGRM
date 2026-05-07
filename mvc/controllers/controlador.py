from librerias.matrices import Matriz
from mvc.models.modelo import SimuladorGaussJordan

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = SimuladorGaussJordan(modulo=26)
        self._pasos = []
        self._indice_actual = 0

    def cargar_matrices_desde_letras(self, plano_filas, cifrado_filas):
        P, C = Matriz.desde_letras(plano_filas, cifrado_filas)
        self.modelo.establecer_matrices(P, C)
        self._pasos = self.modelo.pasos  # solo el paso inicial
        self._indice_actual = 0

    def cargar_matrices_desde_numeros(self, plano_filas, cifrado_filas):
        P = Matriz(plano_filas)
        C = Matriz(cifrado_filas)
        self.modelo.establecer_matrices(P, C)
        self._pasos = self.modelo.pasos
        self._indice_actual = 0

    def iniciar_simulacion(self):
        """Ejecuta el algoritmo completo guardando todos los pasos."""
        try:
            self.modelo.ejecutar_gauss_jordan()
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error en la simulación", str(e))
            return
        self._pasos = self.modelo.pasos
        self._indice_actual = 0
        self.vista.habilitar_controles(True)
        self.mostrar_paso_actual()

    def mostrar_paso_actual(self):
        if 0 <= self._indice_actual < len(self._pasos):
            paso = self._pasos[self._indice_actual]
            self.vista.mostrar_paso(paso)
            # Actualizar etiquetas de estado
            self.vista.lbl_estado.config(
                text=f"Paso {self._indice_actual+1}/{len(self._pasos)}"
            )
            # Control de botones
            self.vista.btn_anterior.config(state="normal" if self._indice_actual > 0 else "disabled")
            self.vista.btn_siguiente.config(state="normal" if self._indice_actual < len(self._pasos)-1 else "disabled")

    def avanzar_paso(self):
        if self._indice_actual < len(self._pasos) - 1:
            self._indice_actual += 1
            self.mostrar_paso_actual()

    def retroceder_paso(self):
        if self._indice_actual > 0:
            self._indice_actual -= 1
            self.mostrar_paso_actual()

    def reiniciar_simulacion(self):
        self._indice_actual = 0
        self.mostrar_paso_actual()
