from typing import Optional
from librerias.matematica import reducir_mod, inverso_modular, es_coprimo


class Matriz:
    def __init__(self, datos: list, modulo: int = 27):
        if not datos or not datos[0]:
            raise ValueError("La matriz no puede estar vacía.")
        self.filas = len(datos)
        self.columnas = len(datos[0])
        self.modulo = modulo
        for fila in datos:
            if len(fila) != self.columnas:
                raise ValueError("Todas las filas deben tener el mismo número de columnas.")
        self.datos = [
            [reducir_mod(valor, modulo) for valor in fila]
            for fila in datos
        ]

    def obtener(self, fila: int, columna: int) -> int:
        return self.datos[fila][columna]

    def establecer(self, fila: int, columna: int, valor: int):
        self.datos[fila][columna] = reducir_mod(valor, self.modulo)

    def copia(self) -> "Matriz":
        datos_copia = [fila[:] for fila in self.datos]
        return Matriz(datos_copia, self.modulo)

    def como_lista(self) -> list:
        return [fila[:] for fila in self.datos]

    def __str__(self) -> str:
        lineas = []
        for fila in self.datos:
            contenido = "  ".join(str(valor).rjust(3) for valor in fila)
            lineas.append(f"[ {contenido} ]")
        return "\n".join(lineas)

    def __getitem__(self, indice):
        return self.datos[indice]

    def intercambiar_filas(self, i: int, j: int):
        self.datos[i], self.datos[j] = self.datos[j], self.datos[i]

    def multiplicar_fila(self, fila: int, escalar: int, modulo: int = None):
        if modulo is None:
            modulo = self.modulo
        self.datos[fila] = [reducir_mod(elem * escalar, modulo) for elem in self.datos[fila]]

    def sumar_fila_multiplo(self, fila_destino: int, fila_fuente: int, escalar: int, modulo: int = None):
        if modulo is None:
            modulo = self.modulo
        self.datos[fila_destino] = [
            reducir_mod(self.datos[fila_destino][k] + escalar * self.datos[fila_fuente][k], modulo)
            for k in range(len(self.datos[fila_destino]))
        ]


class OperacionFila:
    def __init__(self, tipo: str, descripcion: str, estado_antes: list, estado_despues: list):
        self.tipo = tipo
        self.descripcion = descripcion
        self.estado_antes = [fila[:] for fila in estado_antes]
        self.estado_despues = [fila[:] for fila in estado_despues]


def _intercambiar_filas(datos: list, i: int, j: int, modulo: int) -> OperacionFila:
    antes = [fila[:] for fila in datos]
    datos[i], datos[j] = datos[j], datos[i]
    despues = [fila[:] for fila in datos]
    return OperacionFila("Intercambio de filas", f"F{i+1} ↔ F{j+1}", antes, despues)


def _escalar_fila(datos: list, i: int, escalar: int, modulo: int) -> OperacionFila:
    antes = [fila[:] for fila in datos]
    datos[i] = [reducir_mod(elemento * escalar, modulo) for elemento in datos[i]]
    despues = [fila[:] for fila in datos]
    return OperacionFila("Multiplicación de fila", f"F{i+1} ← {escalar} · F{i+1} (mod {modulo})", antes, despues)


def _combinar_filas(datos: list, i: int, j: int, escalar: int, modulo: int) -> OperacionFila:
    antes = [fila[:] for fila in datos]
    datos[i] = [reducir_mod(datos[i][k] + escalar * datos[j][k], modulo) for k in range(len(datos[i]))]
    despues = [fila[:] for fila in datos]
    signo = "+" if escalar >= 0 else "-"
    return OperacionFila(
        "Combinación de filas",
        f"F{i+1} ← F{i+1} {signo} {abs(escalar)} · F{j+1} (mod {modulo})",
        antes, despues
    )


def multiplicar_matrices(a: Matriz, b: Matriz, modulo: int = 27) -> Matriz:
    if a.columnas != b.filas:
        raise ValueError(f"Dimensiones incompatibles: ({a.filas}x{a.columnas}) × ({b.filas}x{b.columnas}).")
    resultado = [[0] * b.columnas for _ in range(a.filas)]
    for i in range(a.filas):
        for j in range(b.columnas):
            suma = 0
            for k in range(a.columnas):
                suma += a.obtener(i, k) * b.obtener(k, j)
            resultado[i][j] = reducir_mod(suma, modulo)
    return Matriz(resultado, modulo)


def gauss_jordan_modular(matriz_aumentada: list, n: int, modulo: int = 27) -> tuple:
    datos = [fila[:] for fila in matriz_aumentada]
    pasos = []
    for columna_pivote in range(n):
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
        if pivote_fila != columna_pivote:
            pasos.append(_intercambiar_filas(datos, columna_pivote, pivote_fila, modulo))
        pivote = datos[columna_pivote][columna_pivote]
        try:
            inv_pivote = inverso_modular(pivote, modulo)
        except ValueError:
            return None, pasos
        if inv_pivote != 1:
            pasos.append(_escalar_fila(datos, columna_pivote, inv_pivote, modulo))
        for fila in range(n):
            if fila == columna_pivote:
                continue
            elemento = datos[fila][columna_pivote]
            if elemento == 0:
                continue
            escalar = reducir_mod(-elemento, modulo)
            pasos.append(_combinar_filas(datos, fila, columna_pivote, escalar, modulo))
    resultado = [datos[i][n:] for i in range(n)]
    return resultado, pasos


def construir_matriz_aumentada(texto_claro_nums: list, texto_cifrado_nums: list, n: int, modulo: int = 27) -> list:
    if len(texto_claro_nums) < n * n:
        raise ValueError(f"Se necesitan al menos {n * n} caracteres de texto claro para recuperar una clave {n}x{n}.")
    if len(texto_claro_nums) != len(texto_cifrado_nums):
        raise ValueError("El texto claro y el texto cifrado deben tener la misma longitud.")
    claro_matriz = []
    cifrado_matriz = []
    for i in range(n):
        fila_claro = [reducir_mod(texto_claro_nums[i * n + j], modulo) for j in range(n)]
        fila_cifrado = [reducir_mod(texto_cifrado_nums[i * n + j], modulo) for j in range(n)]
        claro_matriz.append(fila_claro)
        cifrado_matriz.append(fila_cifrado)
    return [claro_matriz[i] + cifrado_matriz[i] for i in range(n)]


def calcular_determinante(matriz: list, modulo: int = 27) -> int:
    n = len(matriz)
    if n == 1:
        return reducir_mod(matriz[0][0], modulo)
    if n == 2:
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        return reducir_mod(det, modulo)
    A = [fila[:] for fila in matriz]
    det = 1
    signo = 1
    for i in range(n):
        if A[i][i] == 0:
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    signo = -signo
                    break
            else:
                return 0
        pivote = A[i][i]
        inv_pivote_val = None
        try:
            inv_pivote_val = inverso_modular(pivote, modulo)
        except ValueError:
            return 0
        det = (det * pivote) % modulo
        for f in range(i + 1, n):
            if A[f][i] != 0:
                factor = (A[f][i] * inv_pivote_val) % modulo
                for c in range(i, n):
                    A[f][c] = (A[f][c] - factor * A[i][c]) % modulo
    return reducir_mod(det * signo, modulo)


def calcular_adjunta(matriz: list, modulo: int = 27) -> list:
    n = len(matriz)
    if n == 1:
        return [[1]]
    adjunta = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatriz = [fila[:j] + fila[j+1:] for fila_idx, fila in enumerate(matriz) if fila_idx != i]
            cofactor = ((-1) ** (i + j)) * calcular_determinante(submatriz, modulo)
            adjunta[j][i] = reducir_mod(cofactor, modulo)
    return adjunta


def calcular_inversa(matriz: list, modulo: int = 27) -> Optional[list]:
    det = calcular_determinante(matriz, modulo)
    try:
        inv_det = inverso_modular(det, modulo)
    except ValueError:
        return None
    adjunta = calcular_adjunta(matriz, modulo)
    n = len(matriz)
    inversa = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            inversa[i][j] = reducir_mod(inv_det * adjunta[i][j], modulo)
    return inversa


def es_invertible(matriz: list, modulo: int = 27) -> bool:
    det = calcular_determinante(matriz, modulo)
    det_mod = det % modulo
    if det_mod == 0:
        return False
    return es_coprimo(det_mod, modulo)