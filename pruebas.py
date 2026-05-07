"""
Pruebas y validación del sistema.

Verifica el correcto funcionamiento de todas las librerías:
aritmética modular, operaciones matriciales, Gauss-Jordan
y cifrado/descifrado Hill.

Ejecutar con:
    python pruebas.py
"""

from librerias.matematica import (
    mcd_extendido,
    inverso_modular,
    reducir_mod,
    es_coprimo,
    texto_a_numeros,
    numeros_a_texto
)
from librerias.matrices import (
    Matriz,
    multiplicar_matrices,
    gauss_jordan_modular,
    construir_matriz_aumentada
)
from librerias.hill_cipher import CifradoHill


# ---------------------------------------------------------------------------
# Utilidad de reporte
# ---------------------------------------------------------------------------

_total = 0
_aprobadas = 0
_fallidas = 0


def prueba(nombre: str, condicion: bool, detalle: str = "") -> None:
    """Registra y reporta el resultado de una prueba."""
    global _total, _aprobadas, _fallidas
    _total += 1
    if condicion:
        _aprobadas += 1
        print(f"  [OK]  {nombre}")
    else:
        _fallidas += 1
        print(f"  [FALLO] {nombre}")
        if detalle:
            print(f"         Detalle: {detalle}")


def seccion(titulo: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print(f"{'='*55}")


# ---------------------------------------------------------------------------
# Pruebas de aritmética modular
# ---------------------------------------------------------------------------

def pruebas_matematica() -> None:
    seccion("1. Aritmética modular (matematica.py)")

    # mcd_extendido
    mcd, x, y = mcd_extendido(35, 15)
    prueba(
        "mcd_extendido(35, 15) = 5",
        mcd == 5,
        f"Obtenido: mcd={mcd}"
    )

    mcd2, x2, y2 = mcd_extendido(26, 6)
    prueba(
        "mcd_extendido(26, 6) = 2",
        mcd2 == 2
    )

    # Verificar identidad de Bezout: a*x + b*y == mcd
    prueba(
        "Identidad de Bezout: 35*x + 15*y = 5",
        35 * x + 15 * y == 5,
        f"35*{x} + 15*{y} = {35*x + 15*y}"
    )

    # inverso_modular
    inv = inverso_modular(3, 26)
    prueba(
        "inverso_modular(3, 26) = 9  [porque 3*9=27≡1 mod26]",
        inv == 9,
        f"Obtenido: {inv}"
    )

    inv2 = inverso_modular(5, 26)
    prueba(
        "inverso_modular(5, 26) = 21 [porque 5*21=105≡1 mod26]",
        inv2 == 21,
        f"Obtenido: {inv2}"
    )

    # Verificar que inv * a ≡ 1 mod 26
    prueba(
        "Verificación: 3 * inv(3) ≡ 1 mod 26",
        (3 * inv) % 26 == 1
    )

    # Inverso inexistente (mcd != 1)
    error_capturado = False
    try:
        inverso_modular(2, 26)
    except ValueError:
        error_capturado = True
    prueba(
        "inverso_modular(2, 26) lanza ValueError [mcd(2,26)=2]",
        error_capturado
    )

    # reducir_mod con negativos
    prueba("reducir_mod(-3, 26) = 23", reducir_mod(-3, 26) == 23)
    prueba("reducir_mod(29, 26) = 3", reducir_mod(29, 26) == 3)
    prueba("reducir_mod(0, 26) = 0",  reducir_mod(0, 26) == 0)

    # es_coprimo
    prueba("es_coprimo(3, 26) = True",  es_coprimo(3, 26) is True)
    prueba("es_coprimo(2, 26) = False", es_coprimo(2, 26) is False)

    # texto_a_numeros / numeros_a_texto
    nums = texto_a_numeros("HOLA")
    prueba(
        "texto_a_numeros('HOLA') = [7,14,11,0]",
        nums == [7, 14, 11, 0],
        f"Obtenido: {nums}"
    )

    texto = numeros_a_texto([7, 14, 11, 0])
    prueba(
        "numeros_a_texto([7,14,11,0]) = 'HOLA'",
        texto == "HOLA",
        f"Obtenido: {texto}"
    )

    prueba(
        "texto_a_numeros ignora espacios: 'HO LA' = [7,14,11,0]",
        texto_a_numeros("HO LA") == [7, 14, 11, 0]
    )


# ---------------------------------------------------------------------------
# Pruebas de operaciones matriciales
# ---------------------------------------------------------------------------

def pruebas_matrices() -> None:
    seccion("2. Operaciones matriciales (matrices.py)")

    # Construcción de Matriz
    m = Matriz([[1, 2], [3, 4]], modulo=26)
    prueba("Matriz 2x2 construida correctamente", m.filas == 2 and m.columnas == 2)
    prueba("Elemento m[0][0] = 1", m.obtener(0, 0) == 1)
    prueba("Elemento m[1][1] = 4", m.obtener(1, 1) == 4)

    # Reducción modular automática
    m2 = Matriz([[27, 53], [0, 26]], modulo=26)
    prueba("27 mod 26 = 1 al construir", m2.obtener(0, 0) == 1)
    prueba("26 mod 26 = 0 al construir", m2.obtener(1, 1) == 0)

    # Multiplicación matricial mod 26
    # K = [[3,3],[2,5]], P = [[7],[4]] → C = [[33],[34]] mod 26 = [[7],[8]]
    k = Matriz([[3, 3], [2, 5]], modulo=26)
    p = Matriz([[7], [4]], modulo=26)
    c = multiplicar_matrices(k, p, modulo=26)
    prueba(
        "K*P mod 26: [[3,3],[2,5]] * [7,4] = [7,8]",
        c.obtener(0, 0) == 7 and c.obtener(1, 0) == 8,
        f"Obtenido: [{c.obtener(0,0)}, {c.obtener(1,0)}]"
    )

    # Multiplicación incompatible
    error_dims = False
    try:
        multiplicar_matrices(
            Matriz([[1, 2, 3]]),
            Matriz([[1, 2]]),
        )
    except ValueError:
        error_dims = True
    prueba("Multiplicación con dims incompatibles lanza ValueError", error_dims)

    # Gauss-Jordan modular: caso conocido
    # Clave K = [[3,3],[2,5]]
    # P (texto claro) = [[7,11],[4,15]]
    # C (texto cifrado) = K*P mod 26
    # C[0] = [3*7+3*4, 3*11+3*15] mod 26 = [33, 78] mod 26 = [7, 0]
    # C[1] = [2*7+5*4, 2*11+5*15] mod 26 = [34, 97] mod 26 = [8, 19]
    # Aumentada: [[7,11, 7, 0],[4,15, 8,19]]
    # Gauss-Jordan debe recuperar K = [[3,3],[2,5]]

    # Gauss-Jordan: la clave K=[[3,3],[2,5]] cifra BIEN→BQZV
    # P (texto claro por filas): fila1=[1,8], fila2=[4,13]
    # C (texto cifrado por filas): fila1=[1,16], fila2=[25,21]
    # Matriz aumentada [P|C]: [[1,8,1,16],[4,13,25,21]]
    # GJ sobre [P|C] da K^T = [[3,2],[3,5]]
    # Al transponer: K = [[3,3],[2,5]]  ← la clave original

    aumentada = construir_matriz_aumentada(
        texto_claro_nums=[1, 8, 4, 13],
        texto_cifrado_nums=[1, 16, 25, 21],
        n=2,
        modulo=26
    )

    kt_rec, pasos = gauss_jordan_modular(aumentada, 2, modulo=26)

    prueba(
        "Gauss-Jordan retorna una solución (no None)",
        kt_rec is not None,
        "El sistema es singular o sin solución"
    )

    if kt_rec is not None:
        # Transponer para obtener K real
        clave_rec = [[kt_rec[j][i] for j in range(2)] for i in range(2)]
        prueba(
            "Clave recuperada K[0][0] = 3  (tras transponer K^T)",
            clave_rec[0][0] == 3,
            f"Obtenido: {clave_rec[0][0]}"
        )
        prueba(
            "Clave recuperada K[0][1] = 3",
            clave_rec[0][1] == 3,
            f"Obtenido: {clave_rec[0][1]}"
        )
        prueba(
            "Clave recuperada K[1][0] = 2",
            clave_rec[1][0] == 2,
            f"Obtenido: {clave_rec[1][0]}"
        )
        prueba(
            "Clave recuperada K[1][1] = 5",
            clave_rec[1][1] == 5,
            f"Obtenido: {clave_rec[1][1]}"
        )

    prueba(
        "Gauss-Jordan registra al menos 1 operación de fila",
        len(pasos) >= 1,
        f"Pasos registrados: {len(pasos)}"
    )

    # Construir matriz aumentada: validación de longitud insuficiente
    error_longitud = False
    try:
        construir_matriz_aumentada([7], [7], n=2)
    except ValueError:
        error_longitud = True
    prueba(
        "construir_matriz_aumentada lanza ValueError si faltan datos",
        error_longitud
    )


# ---------------------------------------------------------------------------
# Pruebas del cifrado Hill
# ---------------------------------------------------------------------------

def pruebas_hill() -> None:
    seccion("3. Cifrado Hill (hill_cipher.py)")

    clave_datos = [[3, 3], [2, 5]]
    cifrador = CifradoHill(clave_datos, modulo=26)

    # Cifrado de un bloque
    cifrado, pasos_cifrado = cifrador.cifrar("BIEN")
    prueba(
        "CifradoHill.cifrar('BIEN') retorna cadena no vacía",
        len(cifrado) > 0,
        f"Obtenido: '{cifrado}'"
    )
    prueba(
        "CifradoHill.cifrar produce pasos detallados",
        len(pasos_cifrado) > 0
    )

    # Descifrado: descifrar lo cifrado debe dar el original
    descifrado, pasos_descifrado = cifrador.descifrar(cifrado)
    prueba(
        "CifradoHill.descifrar(cifrar('BIEN')) = 'BIEN'",
        descifrado.startswith("BIEN"),
        f"Obtenido: '{descifrado}'"
    )

    # Consistencia: cifrar "MATH" y descifrar
    cifrado2, _ = cifrador.cifrar("MATH")
    descifrado2, _ = cifrador.descifrar(cifrado2)
    prueba(
        "Cifrar→Descifrar 'MATH' es consistente",
        descifrado2.startswith("MATH"),
        f"Obtenido: '{descifrado2}'"
    )

    # Clave no invertible debe lanzar error
    error_clave = False
    try:
        CifradoHill([[2, 4], [6, 8]], modulo=26)
    except ValueError:
        error_clave = True
    prueba(
        "CifradoHill rechaza clave con det no coprimo con 26",
        error_clave
    )

    # Clave 3x3 válida: det debe ser coprimo con 26
    # K = [[1,2,3],[0,1,4],[5,6,0]] — verificar det
    clave_3x3 = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    try:
        cifrador3 = CifradoHill(clave_3x3, modulo=26)
        cifrado3, _ = cifrador3.cifrar("ACT")
        descifrado3, _ = cifrador3.descifrar(cifrado3)
        prueba(
            "Cifrado Hill 3x3: cifrar→descifrar 'ACT' consistente",
            descifrado3.startswith("ACT"),
            f"Obtenido: '{descifrado3}'"
        )
    except ValueError as e:
        # Intentar con otra clave válida
        clave_3x3b = [[17, 17, 5], [21, 18, 21], [2, 2, 19]]
        try:
            cifrador3b = CifradoHill(clave_3x3b, modulo=26)
            cifrado3b, _ = cifrador3b.cifrar("ACT")
            descifrado3b, _ = cifrador3b.descifrar(cifrado3b)
            prueba(
                "Cifrado Hill 3x3 (clave alternativa): cifrar→descifrar 'ACT'",
                descifrado3b.startswith("ACT"),
                f"Obtenido: '{descifrado3b}'"
            )
        except ValueError as e2:
            prueba("Cifrado Hill 3x3", False, str(e2))

    # Relleno con X cuando texto no es múltiplo del bloque
    cifrado_impar, _ = cifrador.cifrar("ABC")
    prueba(
        "cifrar texto impar rellena con X y no lanza error",
        len(cifrado_impar) == 4,  # 3 letras → rellena a 4 (2 bloques de 2)
        f"Longitud obtenida: {len(cifrado_impar)}"
    )


# ---------------------------------------------------------------------------
# Pruebas de integración: ataque completo
# ---------------------------------------------------------------------------

def pruebas_integracion() -> None:
    seccion("4. Integración: ataque Gauss-Jordan completo")

    from mvc.modelo import ModeloSimulador

    modelo = ModeloSimulador()

    # Usar clave conocida para generar par plano/cifrado y luego atacar
    clave_original = [[3, 3], [2, 5]]
    cifrador = CifradoHill(clave_original, modulo=26)

    texto_plano = "BIEN"
    texto_cifrado, _ = cifrador.cifrar(texto_plano)

    prueba(
        f"Texto cifrado generado: '{texto_cifrado}'",
        len(texto_cifrado) == len(texto_plano),
        f"Esperado: misma longitud, obtenido: '{texto_cifrado}'"
    )

    # Configurar el modelo con el par conocido
    exito_config = modelo.configurar(
        texto_claro=texto_plano,
        texto_cifrado=texto_cifrado,
        n=2,
        modulo=26
    )
    prueba("Modelo.configurar() con datos válidos retorna True", exito_config)

    # Ejecutar el ataque
    exito_ataque = modelo.ejecutar_ataque()
    prueba("Modelo.ejecutar_ataque() retorna True", exito_ataque)

    clave_rec = modelo.estado.clave_recuperada
    prueba(
        "Clave recuperada es una matriz 2x2",
        len(clave_rec) == 2 and len(clave_rec[0]) == 2
    )
    prueba(
        "Clave recuperada [0][0] == 3",
        clave_rec[0][0] == 3,
        f"Obtenido: {clave_rec[0][0]}"
    )
    prueba(
        "Clave recuperada [1][1] == 5",
        clave_rec[1][1] == 5,
        f"Obtenido: {clave_rec[1][1]}"
    )

    # Verificar que con la clave recuperada se puede descifrar
    desc, err = modelo.descifrar_con_clave_recuperada(texto_cifrado)
    prueba(
        "Descifrar con clave recuperada reproduce el texto original",
        desc.startswith("BIEN") and not err,
        f"Obtenido: '{desc}', error: '{err}'"
    )

    # Navegación de pasos
    total_pasos = len(modelo.estado.pasos)
    prueba(
        f"Hay al menos 1 paso registrado ({total_pasos} pasos)",
        total_pasos >= 1
    )

    modelo.ir_a_paso(0)
    prueba("ir_a_paso(0) deja paso_actual en 0", modelo.estado.paso_actual == 0)

    modelo.siguiente_paso()
    if total_pasos > 1:
        prueba(
            "siguiente_paso() avanza a paso 1",
            modelo.estado.paso_actual == 1
        )

    modelo.ir_a_paso(0)
    modelo.paso_anterior()
    prueba(
        "paso_anterior() en paso 0 no retrocede (permanece en 0)",
        modelo.estado.paso_actual == 0
    )

    # Configuración inválida (texto demasiado corto)
    modelo2 = ModeloSimulador()
    exito_invalido = modelo2.configurar("A", "B", n=2)
    prueba(
        "configurar() con texto corto retorna False",
        not exito_invalido
    )
    prueba(
        "configurar() con texto corto registra mensaje de error",
        len(modelo2.estado.error) > 0
    )


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n" + "=" * 55)
    print("  SUITE DE PRUEBAS — Simulador Gauss-Jordan")
    print("  Criptografía — Ingeniería Informática")
    print("=" * 55)

    pruebas_matematica()
    pruebas_matrices()
    pruebas_hill()
    pruebas_integracion()

    print(f"\n{'='*55}")
    print(f"  RESUMEN FINAL")
    print(f"  Total:     {_total} pruebas")
    print(f"  Aprobadas: {_aprobadas}")
    print(f"  Fallidas:  {_fallidas}")
    estado = "TODAS LAS PRUEBAS APROBADAS" if _fallidas == 0 else f"{_fallidas} PRUEBA(S) FALLIDA(S)"
    print(f"  Estado:    {estado}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
