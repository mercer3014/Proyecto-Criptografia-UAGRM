from dataclasses import dataclass, field
from typing import Optional
from librerias.matematica import texto_a_numeros, numeros_a_texto, reducir_mod
from librerias.matrices import construir_matriz_aumentada, gauss_jordan_modular
from librerias.hill_cipher import CifradoHill


@dataclass
class EstadoSimulador:
    texto_claro: str = ""
    texto_cifrado: str = ""
    n: int = 0
    modulo: int = 27
    matriz_aumentada: Optional[list] = None
    pasos: list = field(default_factory=list)
    clave_recuperada: Optional[list] = None
    paso_actual: int = 0
    error: str = ""
    listo: bool = False


class ModeloSimulador:

    def __init__(self):
        self._estado = EstadoSimulador()

    @property
    def estado(self):
        return self._estado

    def reiniciar(self):
        self._estado = EstadoSimulador()

    def configurar(self, texto_claro, texto_cifrado, n, modulo=27):
        try:
            texto_claro = texto_claro.upper().replace(" ", "")
            texto_cifrado = texto_cifrado.upper().replace(" ", "")
            if len(texto_claro) < n * n:
                self._estado.error = f"Se necesitan al menos {n * n} caracteres de texto claro."
                return False
            if len(texto_cifrado) < n * n:
                self._estado.error = f"Se necesitan al menos {n * n} caracteres de texto cifrado."
                return False
            min_len = min(len(texto_claro), len(texto_cifrado))
            texto_claro = texto_claro[:min_len]
            texto_cifrado = texto_cifrado[:min_len]
            claro_nums = texto_a_numeros(texto_claro, modulo)
            cifrado_nums = texto_a_numeros(texto_cifrado, modulo)
            aumentada = construir_matriz_aumentada(claro_nums, cifrado_nums, n, modulo)
            self._estado.texto_claro = texto_claro
            self._estado.texto_cifrado = texto_cifrado
            self._estado.n = n
            self._estado.modulo = modulo
            self._estado.matriz_aumentada = aumentada
            self._estado.pasos = []
            self._estado.clave_recuperada = None
            self._estado.paso_actual = 0
            self._estado.error = ""
            self._estado.listo = False
            return True
        except Exception as e:
            self._estado.error = str(e)
            return False

    def ejecutar_ataque(self):
        if self._estado.matriz_aumentada is None:
            self._estado.error = "No se ha configurado el ataque."
            return False
        try:
            resultado, pasos = gauss_jordan_modular(
                self._estado.matriz_aumentada,
                self._estado.n,
                self._estado.modulo
            )
            if resultado is None:
                self._estado.error = "No se pudo recuperar la clave. La matriz no es invertible."
                self._estado.pasos = pasos
                return False
            resultado_transpuesta = [
                [resultado[j][i] for j in range(self._estado.n)]
                for i in range(self._estado.n)
            ]
            self._estado.clave_recuperada = resultado_transpuesta
            self._estado.pasos = pasos
            self._estado.listo = True
            return True
        except Exception as e:
            self._estado.error = str(e)
            return False

    def ir_a_paso(self, indice):
        if 0 <= indice < len(self._estado.pasos):
            self._estado.paso_actual = indice
            return self._estado.pasos[indice]
        return None

    def siguiente_paso(self):
        if self._estado.paso_actual < len(self._estado.pasos) - 1:
            self._estado.paso_actual += 1
        return self.obtener_paso_actual()

    def paso_anterior(self):
        if self._estado.paso_actual > 0:
            self._estado.paso_actual -= 1
        return self.obtener_paso_actual()

    def obtener_paso_actual(self):
        if not self._estado.pasos:
            return None
        if self._estado.paso_actual < len(self._estado.pasos):
            return self._estado.pasos[self._estado.paso_actual]
        return None

    def cifrar_con_clave_recuperada(self, texto):
        if self._estado.clave_recuperada is None:
            raise ValueError("No se ha recuperado ninguna clave.")
        cifrador = CifradoHill(self._estado.clave_recuperada, self._estado.modulo)
        return cifrador.cifrar(texto)

    def descifrar_con_clave_recuperada(self, texto):
        if self._estado.clave_recuperada is None:
            raise ValueError("No se ha recuperado ninguna clave.")
        cifrador = CifradoHill(self._estado.clave_recuperada, self._estado.modulo)
        return cifrador.descifrar(texto)

    def formatear_matriz(self, datos):
        lineas = []
        for fila in datos:
            partes = [str(val).rjust(3) for val in fila]
            lineas.append("[ " + "  ".join(partes) + " ]")
        return "\n".join(lineas)

    def formatear_matriz_aumentada(self, datos, n):
        lineas = []
        for fila in datos:
            izquierda = [str(val).rjust(3) for val in fila[:n]]
            derecha = [str(val).rjust(3) for val in fila[n:]]
            lineas.append("[ " + "  ".join(izquierda) + " | " + "  ".join(derecha) + " ]")
        return "\n".join(lineas)

    def formatear_matriz_aumentada_columnas(self, datos, n):
        datos_t = []
        for i in range(n):
            fila = [datos[j][i] for j in range(n)] + [datos[j][i + n] for j in range(n)]
            datos_t.append(fila)
        return self.formatear_matriz_aumentada(datos_t, n)