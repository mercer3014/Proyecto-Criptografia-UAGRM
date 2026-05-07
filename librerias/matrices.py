"""
Librería de operaciones matriciales implementada desde cero.

Incluye representación de matrices, operaciones elementales de fila,
y el método de Gauss-Jordan en aritmética modular para recuperar
la clave del cifrado Hill.

No se utiliza numpy ni ninguna librería matemática externa.
"""

from typing import Optional
from librerias.matematica import reducir_mod, inverso_modular


class Matriz:
    """
    Representa una matriz de enteros con soporte para aritmética modular.

    Atributos:
        filas: Número de filas.
        columnas: Número de columnas.
        datos: Lista de listas que contiene los valores.
        modulo: Módulo del sistema (26 para Hill estándar).
    """

    def __init__(
        self,
        datos: list[list[int]],
        modulo: int = 26
    ) -> None:
        """
        Inicializa la matriz con los datos dados.

        Parametros:
            datos: Lista de listas de enteros.
            modulo: Módulo para la aritmética (default 26).
        """
        if not datos or not datos[0]:
            raise ValueError("La matriz no puede estar vacía.")

        self.filas = len(datos)
        self.columnas = len(datos[0])
        self.modulo = modulo

        for fila in datos:
            if len(fila) != self.columnas:
                raise ValueError(
                    "Todas las filas deben tener el mismo número de columnas."
                )

        # Se copia para evitar mutaciones externas no deseadas
        self.datos = [
            [reducir_mod(valor, modulo) for valor in fila]
            for fila in datos
        ]

    def obtener(self, fila: int, columna: int) -> int:
        """Retorna el elemento en la posición (fila, columna)."""
        return self.datos[fila][columna]

    def establecer(self, fila: int, columna: int, valor: int) -> None:
        """Establece el valor en la posición (fila, columna)."""
        self.datos[fila][columna] = reducir_mod(valor, self.modulo)

    def copia(self) -> "Matriz":
        """Retorna una copia independiente de la matriz."""
        datos_copia = [fila[:] for fila in self.datos]
        return Matriz(datos_copia, self.modulo)

    def __str__(self) -> str:
        """Representación legible de la matriz."""
        lineas = []
        for fila in self.datos:
            contenido = "  ".join(str(valor).rjust(3) for valor in fila)
            lineas.append(f"[ {contenido} ]")
        return "\n".join(lineas)

    def como_lista(self) -> list[list[int]]:
        """Retorna una copia de los datos como lista de listas."""
        return [fila[:] for fila in self.datos]


def multiplicar_matrices(
    a: Matriz,
    b: Matriz,
    modulo: int = 26
) -> Matriz:
    """
    Multiplica dos matrices en aritmética modular.

    La multiplicación estándar C[i][j] = sum(A[i][k] * B[k][j])
    se realiza mod 'modulo'.

    Parametros:
        a: Primera matriz.
        b: Segunda matriz.
        modulo: Módulo del sistema.

    Retorna:
        Matriz resultante de la multiplicación.

    Lanza:
        ValueError si las dimensiones son incompatibles.
    """
    if a.columnas != b.filas:
        raise ValueError(
            f"Dimensiones incompatibles: ({a.filas}x{a.columnas}) "
            f"× ({b.filas}x{b.columnas})."
        )

    resultado = [
        [0] * b.columnas
        for _ in range(a.filas)
    ]

    for i in range(a.filas):
        for j in range(b.columnas):
            suma = 0
            for k in range(a.columnas):
                suma += a.obtener(i, k) * b.obtener(k, j)
            resultado[i][j] = reducir_mod(suma, modulo)

    return Matriz(resultado, modulo)


# ---------------------------------------------------------------------------
# Operaciones elementales de fila (Gauss-Jordan)
# ---------------------------------------------------------------------------

class OperacionFila:
    """
    Representa una operación elemental de fila aplicada sobre una matriz.

    Se usa para registrar el historial paso a paso del algoritmo
    Gauss-Jordan y mostrarlo en la interfaz.

    Atributos:
        tipo: Descripción del tipo de operación.
        descripcion: Texto legible explicando la operación concreta.
        estado_antes: Copia de la matriz antes de aplicar la operación.
        estado_despues: Copia de la matriz después de aplicar la operación.
    """

    def __init__(
        self,
        tipo: str,
        descripcion: str,
        estado_antes: list[list[int]],
        estado_despues: list[list[int]]
    ) -> None:
        self.tipo = tipo
        self.descripcion = descripcion
        self.estado_antes = [fila[:] for fila in estado_antes]
        self.estado_despues = [fila[:] for fila in estado_despues]


def _intercambiar_filas(
    datos: list[list[int]],
    i: int,
    j: int,
    modulo: int
) -> OperacionFila:
    """Intercambia las filas i y j. Operación elemental tipo I."""
    antes = [fila[:] for fila in datos]
    datos[i], datos[j] = datos[j], datos[i]
    despues = [fila[:] for fila in datos]
    return OperacionFila(
        tipo="Intercambio de filas",
        descripcion=f"F{i+1} ↔ F{j+1}",
        estado_antes=antes,
        estado_despues=despues
    )


def _escalar_fila(
    datos: list[list[int]],
    i: int,
    escalar: int,
    modulo: int
) -> OperacionFila:
    """Multiplica la fila i por el escalar modular. Operación elemental tipo II."""
    antes = [fila[:] for fila in datos]
    datos[i] = [
        reducir_mod(elemento * escalar, modulo)
        for elemento in datos[i]
    ]
    despues = [fila[:] for fila in datos]
    return OperacionFila(
        tipo="Multiplicación de fila",
        descripcion=f"F{i+1} ← {escalar} · F{i+1} (mod {modulo})",
        estado_antes=antes,
        estado_despues=despues
    )


def _combinar_filas(
    datos: list[list[int]],
    i: int,
    j: int,
    escalar: int,
    modulo: int
) -> OperacionFila:
    """
    Reemplaza F_i por F_i + escalar * F_j (mod modulo).
    Operación elemental tipo III.
    """
    antes = [fila[:] for fila in datos]
    datos[i] = [
        reducir_mod(datos[i][k] + escalar * datos[j][k], modulo)
        for k in range(len(datos[i]))
    ]
    despues = [fila[:] for fila in datos]

    signo = "+" if escalar >= 0 else "-"
    return OperacionFila(
        tipo="Combinación de filas",
        descripcion=(
            f"F{i+1} ← F{i+1} {signo} {abs(escalar)} · F{j+1} "
            f"(mod {modulo})"
        ),
        estado_antes=antes,
        estado_despues=despues
    )


def gauss_jordan_modular(
    matriz_aumentada: list[list[int]],
    n: int,
    modulo: int = 26
) -> tuple[Optional[list[list[int]]], list[OperacionFila]]:
    """
    Aplica el método de Gauss-Jordan en aritmética modular sobre
    una matriz aumentada [A | B] de dimensión n x 2n.

    El objetivo es transformar la parte izquierda en la identidad,
    de modo que la parte derecha sea A^(-1) * B, es decir, la clave.

    Parametros:
        matriz_aumentada: Lista de listas representando [A | B].
        n: Tamaño del bloque cuadrado (n x n).
        modulo: Módulo del sistema (26).

    Retorna:
        Tupla (resultado, pasos):
            - resultado: La mitad derecha de la matriz reducida, o None
              si el sistema no tiene solución única.
            - pasos: Lista de OperacionFila con el historial completo.
    """
    datos = [fila[:] for fila in matriz_aumentada]
    pasos: list[OperacionFila] = []

    for columna_pivote in range(n):
        # Buscar un pivote coprimo con el módulo en la columna actual.
        # Se priorizan filas cuyo elemento pivote tenga inverso modular,
        # ya que si el pivote no es coprimo con el módulo no se puede
        # normalizar la fila.
        pivote_fila = None
        for fila in range(columna_pivote, n):
            if datos[fila][columna_pivote] != 0:
                try:
                    inverso_modular(datos[fila][columna_pivote], modulo)
                    pivote_fila = fila
                    break
                except ValueError:
                    if pivote_fila is None:
                        pivote_fila = fila

        if pivote_fila is None:
            return None, pasos

        # Mover el pivote a la posición diagonal si es necesario
        if pivote_fila != columna_pivote:
            op = _intercambiar_filas(datos, columna_pivote, pivote_fila, modulo)
            pasos.append(op)

        # Calcular el inverso del elemento pivote
        pivote = datos[columna_pivote][columna_pivote]
        try:
            inv_pivote = inverso_modular(pivote, modulo)
        except ValueError:
            return None, pasos

        # Escalar la fila pivote para que el elemento diagonal sea 1
        if inv_pivote != 1:
            op = _escalar_fila(datos, columna_pivote, inv_pivote, modulo)
            pasos.append(op)

        # Eliminar todos los demás elementos de la columna pivote
        for fila in range(n):
            if fila == columna_pivote:
                continue
            elemento = datos[fila][columna_pivote]
            if elemento == 0:
                continue
            escalar = reducir_mod(-elemento, modulo)
            op = _combinar_filas(datos, fila, columna_pivote, escalar, modulo)
            pasos.append(op)

    # Extraer la mitad derecha como resultado (la clave recuperada)
    resultado = [datos[i][n:] for i in range(n)]
    return resultado, pasos


def construir_matriz_aumentada(
    texto_claro_nums: list[int],
    texto_cifrado_nums: list[int],
    n: int,
    modulo: int = 26
) -> list[list[int]]:
    """
    Construye la matriz aumentada [Texto Claro | Texto Cifrado].

    Para un cifrado Hill con bloques de tamaño n, se necesitan al menos
    n bloques de texto claro/cifrado para determinar la clave n x n.

    Parametros:
        texto_claro_nums: Lista de enteros del texto claro.
        texto_cifrado_nums: Lista de enteros del texto cifrado.
        n: Tamaño del bloque.
        modulo: Módulo del sistema.

    Retorna:
        Matriz aumentada como lista de listas.

    Lanza:
        ValueError si no hay suficientes datos.
    """
    if len(texto_claro_nums) < n * n:
        raise ValueError(
            f"Se necesitan al menos {n * n} caracteres de texto claro "
            f"para recuperar una clave {n}x{n}."
        )

    if len(texto_claro_nums) != len(texto_cifrado_nums):
        raise ValueError(
            "El texto claro y el texto cifrado deben tener la misma longitud."
        )

    # Tomar solo los primeros n*n caracteres para formar las matrices n x n
    claro_matriz = []
    cifrado_matriz = []

    for i in range(n):
        fila_claro = [
            reducir_mod(texto_claro_nums[i * n + j], modulo)
            for j in range(n)
        ]
        fila_cifrado = [
            reducir_mod(texto_cifrado_nums[i * n + j], modulo)
            for j in range(n)
        ]
        claro_matriz.append(fila_claro)
        cifrado_matriz.append(fila_cifrado)

    # Concatenar horizontalmente: [P | C]
    matriz_aumentada = [
        claro_matriz[i] + cifrado_matriz[i]
        for i in range(n)
    ]

    return matriz_aumentada
