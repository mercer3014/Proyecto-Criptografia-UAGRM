from models.gauss_jordan import ModeloSimulador
from librerias.matematica import ALFABETO_27


class ControladorGaussJordan:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloSimulador()
        self.vista.establecer_controlador(self)

    def construir_matriz(self):
        texto_claro = self.vista.obtener_texto_claro()
        texto_cifrado = self.vista.obtener_texto_cifrado()
        n = self.vista.obtener_n()
        if not texto_claro or not texto_cifrado:
            self.vista.mostrar_error("Ingrese texto claro y texto cifrado.")
            return
        exito = self.modelo.configurar(texto_claro, texto_cifrado, n)
        if not exito:
            self.vista.mostrar_error(self.modelo.estado.error)
            return
        datos = self.modelo.estado.matriz_aumentada
        texto = self.modelo.formatear_matriz_aumentada_columnas(datos, n)
        self.vista.mostrar_matriz_inicial(texto)

    def ejecutar_ataque(self):
        if self.modelo.estado.matriz_aumentada is None:
            self.construir_matriz()
            if self.modelo.estado.matriz_aumentada is None:
                return
        exito = self.modelo.ejecutar_ataque()
        if not exito:
            self.vista.mostrar_error(self.modelo.estado.error)
            return
        clave = self.modelo.estado.clave_recuperada
        if clave:
            clave_str = "Clave K recuperada:\n"
            for fila in clave:
                clave_str += "  ".join(f"{v:>3}" for v in fila) + "\n"
            self.vista.mostrar_clave(clave_str)
        self._actualizar_vista()

    def siguiente_paso(self):
        paso = self.modelo.siguiente_paso()
        if paso is None:
            self.vista.mostrar_info("No hay mas pasos.")
            return
        self._actualizar_vista()

    def paso_anterior(self):
        self.modelo.paso_anterior()
        self._actualizar_vista()

    def ir_a_paso(self, indice):
        paso = self.modelo.ir_a_paso(indice)
        if paso is None:
            return
        self._actualizar_vista()

    def ir_al_ultimo(self):
        if self.modelo.estado.pasos:
            self.modelo.ir_a_paso(len(self.modelo.estado.pasos) - 1)
            self._actualizar_vista()

    def ir_al_primero(self):
        if self.modelo.estado.pasos:
            self.modelo.ir_a_paso(0)
            self._actualizar_vista()

    def _actualizar_vista(self):
        paso = self.modelo.obtener_paso_actual()
        if paso is None:
            return
        n = self.modelo.estado.n
        total = len(self.modelo.estado.pasos)
        actual = self.modelo.estado.paso_actual + 1
        antes = self.modelo.formatear_matriz_aumentada_columnas(paso.estado_antes, n)
        despues = self.modelo.formatear_matriz_aumentada_columnas(paso.estado_despues, n)
        self.vista.mostrar_paso(paso.descripcion, antes, despues, actual, total, n)

    def cargar_ejemplo(self):
        self.vista.entrada_claro.delete(0, "end")
        self.vista.entrada_claro.insert(0, "HILL")
        self.vista.entrada_cifrado.delete(0, "end")
        self.vista.entrada_cifrado.insert(0, "MFQI")

    def reiniciar(self):
        self.modelo.reiniciar()
        self.vista.entrada_claro.delete(0, "end")
        self.vista.entrada_cifrado.delete(0, "end")
        self.vista.caja_simulacion.actualizar("")
        self.vista.etiqueta_clave.config(text="")


import tkinter as tk