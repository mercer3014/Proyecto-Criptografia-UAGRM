from librerias.matematica import (
    texto_a_numeros, numeros_a_texto, reducir_mod, inverso_modular,
    char_to_int, int_to_char, ALFABETO_27
)
from librerias.matrices import Matriz, multiplicar_matrices, gauss_jordan_modular


class CifradoHill:
    def __init__(self, clave_datos: list, modulo: int = 27):
        n = len(clave_datos)
        for fila in clave_datos:
            if len(fila) != n:
                raise ValueError("La clave debe ser una matriz cuadrada.")
        self.n = n
        self.modulo = modulo
        self.clave = Matriz(clave_datos, modulo)
        det = self._determinante_mod(clave_datos, n, modulo)
        try:
            inverso_modular(det, modulo)
        except ValueError:
            raise ValueError(
                f"La clave no es invertible mod {modulo}. "
                f"Su determinante es {det}, que no es coprimo con {modulo}."
            )

    def _determinante_mod(self, datos: list, n: int, modulo: int) -> int:
        if n == 1:
            return reducir_mod(datos[0][0], modulo)
        if n == 2:
            det = datos[0][0] * datos[1][1] - datos[0][1] * datos[1][0]
            return reducir_mod(det, modulo)
        det = 0
        for j in range(n):
            menor = [[datos[i][k] for k in range(n) if k != j] for i in range(1, n)]
            cofactor = ((-1) ** j) * datos[0][j] * self._determinante_mod(menor, n - 1, modulo)
            det += cofactor
        return reducir_mod(det, modulo)

    def _preparar_bloques(self, texto: str) -> list:
        numeros = texto_a_numeros(texto, self.modulo)
        relleno = ord('X') - ord('A') if self.modulo == 27 else 23
        while len(numeros) % self.n != 0:
            numeros.append(relleno % self.modulo)
        bloques = []
        for i in range(0, len(numeros), self.n):
            bloques.append(numeros[i:i + self.n])
        return bloques

    def cifrar(self, texto_claro: str) -> tuple:
        bloques = self._preparar_bloques(texto_claro)
        resultado_numeros = []
        pasos = []
        for idx, bloque in enumerate(bloques):
            bloque_matriz = Matriz([[num] for num in bloque], self.modulo)
            cifrado_matriz = multiplicar_matrices(self.clave, bloque_matriz, self.modulo)
            cifrado_bloque = [cifrado_matriz.obtener(i, 0) for i in range(self.n)]
            pasos.append({
                "bloque_numero": idx + 1,
                "texto_claro": numeros_a_texto(bloque, self.modulo),
                "valores_claro": bloque,
                "valores_cifrado": cifrado_bloque,
                "texto_cifrado": numeros_a_texto(cifrado_bloque, self.modulo),
            })
            resultado_numeros.extend(cifrado_bloque)
        return numeros_a_texto(resultado_numeros, self.modulo), pasos

    def descifrar(self, texto_cifrado: str) -> tuple:
        identidad = [[1 if i == j else 0 for j in range(self.n)] for i in range(self.n)]
        clave_datos = self.clave.como_lista()
        aumentada = [clave_datos[i] + identidad[i] for i in range(self.n)]
        inversa_datos, _ = gauss_jordan_modular(aumentada, self.n, self.modulo)
        if inversa_datos is None:
            raise ValueError("La clave no tiene inversa modular.")
        clave_inversa = Matriz(inversa_datos, self.modulo)
        bloques = self._preparar_bloques(texto_cifrado)
        resultado_numeros = []
        pasos = []
        for idx, bloque in enumerate(bloques):
            bloque_matriz = Matriz([[num] for num in bloque], self.modulo)
            descifrado_matriz = multiplicar_matrices(clave_inversa, bloque_matriz, self.modulo)
            descifrado_bloque = [descifrado_matriz.obtener(i, 0) for i in range(self.n)]
            pasos.append({
                "bloque_numero": idx + 1,
                "texto_cifrado": numeros_a_texto(bloque, self.modulo),
                "valores_cifrado": bloque,
                "valores_descifrado": descifrado_bloque,
                "texto_descifrado": numeros_a_texto(descifrado_bloque, self.modulo),
            })
            resultado_numeros.extend(descifrado_bloque)
        return numeros_a_texto(resultado_numeros, self.modulo), pasos

    @staticmethod
    def construir_matriz_clave(clave_texto: str, modulo: int = 27) -> list:
        if modulo == 27:
            clave = clave_texto.upper()
            nums = []
            for c in clave:
                idx = ALFABETO_27.find(c)
                if idx == -1:
                    raise ValueError(f"Carácter inválido en la clave: '{c}'")
                nums.append(idx)
            n = int(len(nums) ** 0.5)
            if n * n != len(nums):
                raise ValueError(f"La clave debe tener un número cuadrado de letras (4 para 2x2, 9 para 3x3). Tiene {len(nums)}.")
            return [nums[i * n:(i + 1) * n] for i in range(n)]
        else:
            nums = []
            for c in clave_texto:
                codigo = ord(c)
                if 0 <= codigo < modulo:
                    nums.append(codigo)
                else:
                    raise ValueError(f"Carácter fuera de rango para módulo {modulo}: '{c}'")
            n = int(len(nums) ** 0.5)
            if n * n != len(nums):
                raise ValueError(f"La clave debe tener un número cuadrado de caracteres. Tiene {len(nums)}.")
            return [nums[i * n:(i + 1) * n] for i in range(n)]