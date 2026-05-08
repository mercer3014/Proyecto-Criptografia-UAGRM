from models.matriz_inversa import ModeloMatrizInversa
from librerias.matematica import ALFABETO_27


class ControladorMatrizInversa:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloMatrizInversa()
        self.vista.establecer_controlador(self)

    def crear_matriz(self):
        try:
            n = self.vista.obtener_tamano()
            if n < 2 or n > 3:
                self.vista.mostrar_error("El tamano debe ser 2 o 3.")
                return
            self.modelo.crear_matriz(n)
            self.vista._crear_cuadricula_entrada(n)
            self.vista.mostrar_resultado(f"Matriz {n}x{n} creada. Ingrese valores y presione un boton de calculo.")
        except Exception as e:
            self.vista.mostrar_error(f"Error: {e}")

    def calcular_determinante(self):
        if self.modelo.datos is None:
            self.vista.mostrar_error("Primero cree una matriz.")
            return
        self._guardar_valores()
        resultado = self.modelo.calcular_determinante()
        if resultado is None:
            self.vista.mostrar_error("No hay datos en la matriz.")
            return
        lineas = []
        lineas.append(f"Determinante: {resultado['determinante']}")
        lineas.append(f"Determinante mod 27: {resultado['determinante_mod']}")
        if resultado["inverso_det"] is not None:
            lineas.append(f"Inverso del determinante mod 27: {resultado['inverso_det']}")
        else:
            lineas.append("El determinante no tiene inverso modular (mcd(det,27)!=1).")
        self.vista.mostrar_resultado("\n".join(lineas))

    def calcular_adjunta(self):
        if self.modelo.datos is None:
            self.vista.mostrar_error("Primero cree una matriz.")
            return
        self._guardar_valores()
        resultado = self.modelo.calcular_adjunta()
        if resultado is None:
            self.vista.mostrar_error("No hay datos en la matriz.")
            return
        lineas = ["Matriz adjunta (mod 27):", ""]
        for fila in resultado["adjunta"]:
            partes = []
            for val in fila:
                letra = ALFABETO_27[val] if 0 <= val < 27 else "?"
                partes.append(f"{val:>3}({letra})")
            lineas.append("  ".join(partes))
        self.vista.mostrar_resultado("\n".join(lineas))

    def calcular_inversa(self):
        if self.modelo.datos is None:
            self.vista.mostrar_error("Primero cree una matriz.")
            return
        self._guardar_valores()
        resultado = self.modelo.calcular_inversa()
        if resultado is None:
            self.vista.mostrar_error("La matriz no es invertible modulo 27.\ndet(K) mod 27 = 0 o no es coprimo con 27.")
            return
        lineas = []
        lineas.append(f"det(K) = {resultado['determinante']}")
        lineas.append(f"det(K) mod 27 = {resultado['determinante_mod']}")
        lineas.append(f"det(K)^(-1) mod 27 = {resultado['inverso_det']}")
        lineas.append("")
        lineas.append("Matriz adjunta (mod 27):")
        for fila in resultado["adjunta"]:
            partes = []
            for val in fila:
                letra = ALFABETO_27[val] if 0 <= val < 27 else "?"
                partes.append(f"{val:>3}({letra})")
            lineas.append("  ".join(partes))
        lineas.append("")
        lineas.append("Matriz inversa K^(-1) (mod 27):")
        for fila in resultado["inversa"]:
            partes = []
            for val in fila:
                letra = ALFABETO_27[val] if 0 <= val < 27 else "?"
                partes.append(f"{val:>3}({letra})")
            lineas.append("  ".join(partes))
        self.vista.mostrar_resultado("\n".join(lineas))

    def _guardar_valores(self):
        valores = self.vista.obtener_valores()
        n = self.modelo.tamano
        for i in range(n):
            for j in range(n):
                self.modelo.guardar_dato(i, j, valores[i][j])