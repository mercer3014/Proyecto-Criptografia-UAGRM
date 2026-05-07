"""
Librería de aritmética modular implementada desde cero.

Provee las operaciones matemáticas fundamentales necesarias para
criptografía modular: algoritmo extendido de Euclides, inverso
multiplicativo modular y reducción modular.

No se utiliza ninguna librería externa. Toda la lógica es propia.
"""


def mcd_extendido(a: int, b: int) -> tuple[int, int, int]:
    """
    Calcula el máximo común divisor mediante el algoritmo extendido
    de Euclides.

    Retorna (mcd, x, y) tales que: a*x + b*y = mcd(a, b).
    Esta identidad de Bezout es la base para encontrar inversos modulares.

    Parametros:
        a: Primer entero.
        b: Segundo entero.

    Retorna:
        Tupla (mcd, x, y).
    """
    if b == 0:
        return a, 1, 0

    mcd, x1, y1 = mcd_extendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return mcd, x, y


def inverso_modular(a: int, modulo: int) -> int:
    """
    Calcula el inverso multiplicativo de 'a' módulo 'modulo'.

    El inverso existe si y solo si mcd(a, modulo) == 1.
    Se basa en el algoritmo extendido de Euclides.

    Parametros:
        a: El número del que se busca el inverso.
        modulo: El módulo del sistema.

    Retorna:
        El inverso modular, un entero en [0, modulo).

    Lanza:
        ValueError si el inverso no existe.
    """
    mcd, x, _ = mcd_extendido(a % modulo, modulo)

    if mcd != 1:
        raise ValueError(
            f"El inverso de {a} mod {modulo} no existe "
            f"porque mcd({a}, {modulo}) = {mcd} ≠ 1."
        )

    return x % modulo


def reducir_mod(valor: int, modulo: int) -> int:
    """
    Reduce un valor al rango [0, modulo) de forma correcta
    incluso para valores negativos.

    Python ya maneja esto bien con %, pero se define explícitamente
    para documentar la intención y cumplir el requerimiento de
    lógica propia.

    Parametros:
        valor: Entero a reducir.
        modulo: El módulo.

    Retorna:
        Entero en [0, modulo).
    """
    return ((valor % modulo) + modulo) % modulo


def es_coprimo(a: int, b: int) -> bool:
    """
    Verifica si dos enteros son coprimos (mcd = 1).

    Parametros:
        a: Primer entero.
        b: Segundo entero.

    Retorna:
        True si mcd(a, b) == 1, False en caso contrario.
    """
    mcd, _, _ = mcd_extendido(a, b)
    return mcd == 1


def texto_a_numeros(texto: str) -> list[int]:
    """
    Convierte una cadena de texto a una lista de enteros.

    Cada letra del alfabeto inglés (A-Z, sin distinguir mayúsculas)
    se convierte a su índice numérico: A=0, B=1, ..., Z=25.
    Los espacios y caracteres no alfabéticos se ignoran.

    Parametros:
        texto: Cadena de texto a convertir.

    Retorna:
        Lista de enteros en [0, 25].
    """
    resultado = []
    for caracter in texto.upper():
        if caracter.isalpha():
            resultado.append(ord(caracter) - ord('A'))
    return resultado


def numeros_a_texto(numeros: list[int]) -> str:
    """
    Convierte una lista de enteros al texto correspondiente.

    Cada entero en [0, 25] se mapea a la letra A-Z correspondiente.

    Parametros:
        numeros: Lista de enteros.

    Retorna:
        Cadena de texto en mayúsculas.
    """
    resultado = []
    for numero in numeros:
        letra = chr((numero % 26) + ord('A'))
        resultado.append(letra)
    return ''.join(resultado)
