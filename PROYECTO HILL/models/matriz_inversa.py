from librerias.matematica import ALFABETO_27, reducir_mod, inverso_modular, es_coprimo
from librerias.matrices import (
    calcular_determinante, calcular_adjunta, calcular_inversa, es_invertible
)


class ModeloMatrizInversa:
    MODULO = 27
    ALFABETO_27 = ALFABETO_27

    def __init__(self):
        self.datos = None
        self.tamano = 0

    def _mod(self, value):
        return int(value) % self.MODULO

    def crear_matriz(self, tamano):
        self.tamano = tamano
        self.datos = [[0] * tamano for _ in range(tamano)]
        return self.datos

    def guardar_dato(self, fila, columna, valor):
        if self.datos is None:
            return False
        if fila < 0 or fila >= self.tamano or columna < 0 or columna >= self.tamano:
            return False
        valor = valor.strip()
        if valor == "":
            return False
        try:
            numero = int(valor)
            self.datos[fila][columna] = self._mod(numero)
            return True
        except ValueError:
            if len(valor) == 1 and valor.upper() in self.ALFABETO_27:
                self.datos[fila][columna] = self.ALFABETO_27.index(valor.upper())
                return True
            return False

    def calcular_determinante(self):
        if self.datos is None:
            return None
        det = calcular_determinante(self.datos, self.MODULO)
        det_mod = det % self.MODULO
        inv_det = None
        try:
            inv_det = inverso_modular(det_mod, self.MODULO)
        except ValueError:
            pass
        return {
            "determinante": det,
            "determinante_mod": det_mod,
            "inverso_det": inv_det,
        }

    def calcular_adjunta(self):
        if self.datos is None:
            return None
        adjunta = calcular_adjunta(self.datos, self.MODULO)
        return {
            "adjunta": adjunta,
        }

    def calcular_inversa(self):
        if self.datos is None:
            return None
        if not es_invertible(self.datos, self.MODULO):
            return None
        det = calcular_determinante(self.datos, self.MODULO)
        det_mod = det % self.MODULO
        inv_det = inverso_modular(det_mod, self.MODULO)
        adjunta = calcular_adjunta(self.datos, self.MODULO)
        inversa = calcular_inversa(self.datos, self.MODULO)
        return {
            "determinante": det,
            "determinante_mod": det_mod,
            "inverso_det": inv_det,
            "adjunta": adjunta,
            "inversa": inversa,
        }

    def _formatear_matriz(self, datos):
        lineas = []
        for fila in datos:
            partes = []
            for val in fila:
                letra = ""
                if 0 <= val < len(self.ALFABETO_27):
                    letra = self.ALFABETO_27[val]
                partes.append(f"{val:>3}({letra})")
            lineas.append("  ".join(partes))
        return "\n".join(lineas)