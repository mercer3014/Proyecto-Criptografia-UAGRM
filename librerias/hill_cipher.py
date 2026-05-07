"""
Librería del cifrado Hill implementada desde cero.

El cifrado Hill es un cifrado poligráfico que utiliza álgebra lineal.
Opera sobre bloques de texto de tamaño n usando una matriz clave n x n.

Ecuación de cifrado:  C = K * P  (mod 26)
Ecuación de descifrado: P = K^(-1) * C  (mod 26)

No se utiliza ninguna librería criptográfica externa.
"""

from librerias.matematica import (
    texto_a_numeros,
    numeros_a_texto,
    reducir_mod,
    inverso_modular
)
from librerias.matrices import (
    Matriz,
    multiplicar_matrices,
    gauss_jordan_modular
)


class CifradoHill:
    """
    Implementa el cifrado y descifrado Hill.

    El cifrado Hill transforma bloques de n letras usando una
    multiplicación matricial: C = K * P mod 26.

    Atributos:
        n: Tamaño del bloque (2 para 2x2, 3 para 3x3, etc.).
        modulo: Módulo del sistema (26 para el alfabeto inglés).
        clave: Matriz clave n x n.
    """

    def __init__(self, clave_datos: list[list[int]], modulo: int = 26) -> None:
        """
        Inicializa el cifrador con una clave.

        Parametros:
            clave_datos: Matriz n x n como lista de listas.
            modulo: Módulo del sistema.

        Lanza:
            ValueError si la clave no es cuadrada o no es invertible.
        """
        n = len(clave_datos)
        for fila in clave_datos:
            if len(fila) != n:
                raise ValueError("La clave debe ser una matriz cuadrada.")

        self.n = n
        self.modulo = modulo
        self.clave = Matriz(clave_datos, modulo)

        # Verificar que la clave sea invertible
        det = self._determinante_mod(clave_datos, n, modulo)
        try:
            inverso_modular(det, modulo)
        except ValueError:
            raise ValueError(
                f"La clave no es invertible mod {modulo}. "
                f"Su determinante es {det}, "
                f"que no es coprimo con {modulo}."
            )

    def _determinante_mod(
        self,
        datos: list[list[int]],
        n: int,
        modulo: int
    ) -> int:
        """
        Calcula el determinante de una matriz cuadrada módulo 'modulo'.

        Usa expansión por cofactores de forma recursiva.
        Solo se usa para validación; no para operaciones principales.

        Parametros:
            datos: Matriz como lista de listas.
            n: Tamaño de la matriz.
            modulo: Módulo.

        Retorna:
            Determinante mod modulo.
        """
        if n == 1:
            return reducir_mod(datos[0][0], modulo)

        if n == 2:
            det = datos[0][0] * datos[1][1] - datos[0][1] * datos[1][0]
            return reducir_mod(det, modulo)

        det = 0
        for j in range(n):
            menor = [
                [datos[i][k] for k in range(n) if k != j]
                for i in range(1, n)
            ]
            cofactor = ((-1) ** j) * datos[0][j] * self._determinante_mod(
                menor, n - 1, modulo
            )
            det += cofactor

        return reducir_mod(det, modulo)

    def _preparar_bloques(self, texto: str) -> list[list[int]]:
        """
        Convierte texto a bloques de tamaño n, rellenando con 'X' (23)
        si el texto no es múltiplo de n.

        Parametros:
            texto: Cadena de texto.

        Retorna:
            Lista de bloques, donde cada bloque es una lista de n enteros.
        """
        numeros = texto_a_numeros(texto)

        # Rellenar si es necesario
        while len(numeros) % self.n != 0:
            numeros.append(ord('X') - ord('A'))

        bloques = []
        for i in range(0, len(numeros), self.n):
            bloques.append(numeros[i:i + self.n])

        return bloques

    def cifrar(self, texto_claro: str) -> tuple[str, list[dict]]:
        """
        Cifra el texto usando el cifrado Hill.

        Cada bloque de n letras se multiplica por la clave:
        C_bloque = K * P_bloque (mod 26)

        Parametros:
            texto_claro: Texto a cifrar.

        Retorna:
            Tupla (texto_cifrado, pasos), donde pasos es una lista
            de diccionarios con el detalle de cada bloque procesado.
        """
        bloques = self._preparar_bloques(texto_claro)
        resultado_numeros = []
        pasos = []

        for idx, bloque in enumerate(bloques):
            # Representar el bloque como matriz columna (n x 1)
            bloque_matriz = Matriz(
                [[num] for num in bloque],
                self.modulo
            )

            # C = K * P mod 26
            cifrado_matriz = multiplicar_matrices(
                self.clave,
                bloque_matriz,
                self.modulo
            )

            cifrado_bloque = [
                cifrado_matriz.obtener(i, 0)
                for i in range(self.n)
            ]

            pasos.append({
                "bloque_numero": idx + 1,
                "texto_claro": numeros_a_texto(bloque),
                "valores_claro": bloque,
                "valores_cifrado": cifrado_bloque,
                "texto_cifrado": numeros_a_texto(cifrado_bloque),
                "descripcion": (
                    f"Bloque {idx+1}: K × {bloque} = {cifrado_bloque} "
                    f"(mod {self.modulo})"
                )
            })

            resultado_numeros.extend(cifrado_bloque)

        return numeros_a_texto(resultado_numeros), pasos

    def descifrar(self, texto_cifrado: str) -> tuple[str, list[dict]]:
        """
        Descifra el texto usando la inversa de la clave Hill.

        P = K^(-1) * C (mod 26)

        La inversa de la clave se calcula usando Gauss-Jordan modular.

        Parametros:
            texto_cifrado: Texto cifrado.

        Retorna:
            Tupla (texto_claro, pasos).
        """
        # Construir la matriz identidad para obtener K^(-1) via Gauss-Jordan
        identidad = [
            [1 if i == j else 0 for j in range(self.n)]
            for i in range(self.n)
        ]

        clave_datos = self.clave.como_lista()
        aumentada = [
            clave_datos[i] + identidad[i]
            for i in range(self.n)
        ]

        inversa_datos, _ = gauss_jordan_modular(aumentada, self.n, self.modulo)

        if inversa_datos is None:
            raise ValueError("La clave no tiene inversa modular.")

        clave_inversa = Matriz(inversa_datos, self.modulo)

        bloques = self._preparar_bloques(texto_cifrado)
        resultado_numeros = []
        pasos = []

        for idx, bloque in enumerate(bloques):
            bloque_matriz = Matriz(
                [[num] for num in bloque],
                self.modulo
            )

            descifrado_matriz = multiplicar_matrices(
                clave_inversa,
                bloque_matriz,
                self.modulo
            )

            descifrado_bloque = [
                descifrado_matriz.obtener(i, 0)
                for i in range(self.n)
            ]

            pasos.append({
                "bloque_numero": idx + 1,
                "texto_cifrado": numeros_a_texto(bloque),
                "valores_cifrado": bloque,
                "valores_descifrado": descifrado_bloque,
                "texto_descifrado": numeros_a_texto(descifrado_bloque),
                "descripcion": (
                    f"Bloque {idx+1}: K⁻¹ × {bloque} = "
                    f"{descifrado_bloque} (mod {self.modulo})"
                )
            })

            resultado_numeros.extend(descifrado_bloque)

        return numeros_a_texto(resultado_numeros), pasos
