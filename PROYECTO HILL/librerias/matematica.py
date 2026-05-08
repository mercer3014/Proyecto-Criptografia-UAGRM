ALFABETO_27 = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


def mcd_extendido(a: int, b: int) -> tuple:
    if b == 0:
        return a, 1, 0
    mcd, x1, y1 = mcd_extendido(b, a % b)
    return mcd, y1, x1 - (a // b) * y1


def inverso_modular(a: int, modulo: int) -> int:
    mcd, x, _ = mcd_extendido(a % modulo, modulo)
    if mcd != 1:
        raise ValueError(
            f"El inverso de {a} mod {modulo} no existe "
            f"porque mcd({a}, {modulo}) = {mcd} ≠ 1."
        )
    return x % modulo


def reducir_mod(valor: int, modulo: int) -> int:
    return ((valor % modulo) + modulo) % modulo


def es_coprimo(a: int, b: int) -> bool:
    mcd, _, _ = mcd_extendido(a, b)
    return mcd == 1


def texto_a_numeros(texto: str, modulo: int = 27) -> list:
    if modulo == 27:
        resultado = []
        for caracter in texto.upper():
            idx = ALFABETO_27.find(caracter)
            if idx != -1:
                resultado.append(idx)
        return resultado
    resultado = []
    for caracter in texto:
        codigo = ord(caracter)
        if 0 <= codigo < modulo:
            resultado.append(codigo)
    return resultado


def numeros_a_texto(numeros: list, modulo: int = 27) -> str:
    if modulo == 27:
        resultado = []
        for numero in numeros:
            resultado.append(ALFABETO_27[numero % 27])
        return ''.join(resultado)
    resultado = []
    for numero in numeros:
        resultado.append(chr(numero % modulo))
    return ''.join(resultado)


def char_to_int(caracter: str, modulo: int = 27) -> int:
    if modulo == 27:
        idx = ALFABETO_27.find(caracter.upper())
        if idx == -1:
            raise ValueError(f"Carácter inválido para módulo 27: '{caracter}'")
        return idx
    codigo = ord(caracter)
    if 0 <= codigo < modulo:
        return codigo
    raise ValueError(f"Carácter fuera de rango para módulo {modulo}: '{caracter}'")


def int_to_char(numero: int, modulo: int = 27) -> str:
    if modulo == 27:
        return ALFABETO_27[numero % 27]
    return chr(numero % modulo)