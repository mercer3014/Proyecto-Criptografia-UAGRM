"""
Modelo del simulador de ataque Gauss-Jordan.

Gestiona el estado de la aplicación y coordina las operaciones
criptográficas y matemáticas. No tiene dependencia de la interfaz.

Patrón: Modelo en MVC.
"""

from librerias.matematica import texto_a_numeros, reducir_mod
from librerias.matrices import (
    construir_matriz_aumentada,
    gauss_jordan_modular,
    OperacionFila,
    Matriz,
    multiplicar_matrices
)
from librerias.hill_cipher import CifradoHill


class EstadoSimulador:
    """
    Contiene el estado completo de una sesión del simulador.

    Atributos:
        texto_claro: Texto claro ingresado.
        texto_cifrado: Texto cifrado ingresado.
        n: Tamaño del bloque.
        modulo: Módulo del sistema.
        matriz_aumentada: La matriz [P | C] construida.
        pasos: Lista de OperacionFila del proceso Gauss-Jordan.
        clave_recuperada: Clave extraída al final del proceso.
        paso_actual: Índice del paso que se está visualizando.
        error: Mensaje de error si algo falló.
    """

    def __init__(self) -> None:
        self.texto_claro: str = ""
        self.texto_cifrado: str = ""
        self.n: int = 2
        self.modulo: int = 26
        self.matriz_aumentada: list[list[int]] = []
        self.pasos: list[OperacionFila] = []
        self.clave_recuperada: list[list[int]] = []
        self.paso_actual: int = 0
        self.error: str = ""
        self.listo: bool = False


class ModeloSimulador:
    """
    Modelo principal del simulador de ataque Gauss-Jordan.

    Responsabilidades:
        - Validar las entradas del usuario.
        - Construir la matriz aumentada [Texto Claro | Texto Cifrado].
        - Ejecutar el algoritmo Gauss-Jordan modular.
        - Mantener el estado de la simulación.
        - Proveer cifrado y descifrado Hill para demostración.
    """

    def __init__(self) -> None:
        self._estado = EstadoSimulador()

    @property
    def estado(self) -> EstadoSimulador:
        """Acceso de solo lectura al estado."""
        return self._estado

    def reiniciar(self) -> None:
        """Reinicia el estado a valores por defecto."""
        self._estado = EstadoSimulador()

    def configurar(
        self,
        texto_claro: str,
        texto_cifrado: str,
        n: int,
        modulo: int = 26
    ) -> bool:
        """
        Valida e inicializa la simulación con los datos dados.

        Parametros:
            texto_claro: Texto claro conocido.
            texto_cifrado: Texto cifrado correspondiente.
            n: Tamaño del bloque de la clave.
            modulo: Módulo del sistema.

        Retorna:
            True si la configuración es válida, False si hay error.
        """
        self.reiniciar()
        e = self._estado

        e.texto_claro = texto_claro.upper().strip()
        e.texto_cifrado = texto_cifrado.upper().strip()
        e.n = n
        e.modulo = modulo

        # Validaciones
        claro_nums = texto_a_numeros(e.texto_claro)
        cifrado_nums = texto_a_numeros(e.texto_cifrado)

        chars_necesarios = n * n

        if len(claro_nums) < chars_necesarios:
            e.error = (
                f"El texto claro necesita al menos {chars_necesarios} "
                f"letras para una clave {n}x{n}. "
                f"Solo tiene {len(claro_nums)}."
            )
            return False

        if len(cifrado_nums) < chars_necesarios:
            e.error = (
                f"El texto cifrado necesita al menos {chars_necesarios} "
                f"letras para una clave {n}x{n}. "
                f"Solo tiene {len(cifrado_nums)}."
            )
            return False

        # Usar solo los primeros n*n caracteres
        claro_nums = claro_nums[:chars_necesarios]
        cifrado_nums = cifrado_nums[:chars_necesarios]

        try:
            e.matriz_aumentada = construir_matriz_aumentada(
                claro_nums, cifrado_nums, n, modulo
            )
        except ValueError as exc:
            e.error = str(exc)
            return False

        e.listo = True
        return True

    def ejecutar_ataque(self) -> bool:
        """
        Ejecuta el algoritmo Gauss-Jordan sobre la matriz aumentada.

        El resultado son los pasos detallados y la clave recuperada.

        Retorna:
            True si el ataque tuvo éxito, False si el sistema no tiene
            solución única (texto claro linealmente dependiente).
        """
        e = self._estado

        if not e.listo:
            e.error = "Debe configurar el simulador antes de ejecutar."
            return False

        clave_transpuesta, pasos = gauss_jordan_modular(
            e.matriz_aumentada, e.n, e.modulo
        )

        e.pasos = pasos

        if clave_transpuesta is None:
            e.error = (
                "No se pudo recuperar la clave. "
                "Los bloques de texto claro son linealmente dependientes "
                f"o el sistema no tiene solución única mod {e.modulo}. "
                "Intente con un texto claro diferente."
            )
            return False

        # Gauss-Jordan sobre [P | C] resuelve P * X = C, donde X = K^T.
        # Para obtener K hay que transponer el resultado.
        n = e.n
        clave = [
            [clave_transpuesta[j][i] for j in range(n)]
            for i in range(n)
        ]
        e.clave_recuperada = clave
        e.paso_actual = 0
        return True

    def ir_a_paso(self, indice: int) -> None:
        """
        Navega a un paso específico de la simulación.

        Parametros:
            indice: Índice del paso (0-based).
        """
        total = len(self._estado.pasos)
        if 0 <= indice < total:
            self._estado.paso_actual = indice

    def siguiente_paso(self) -> bool:
        """
        Avanza al siguiente paso.

        Retorna:
            True si hay más pasos, False si ya está en el último.
        """
        e = self._estado
        if e.paso_actual < len(e.pasos) - 1:
            e.paso_actual += 1
            return True
        return False

    def paso_anterior(self) -> bool:
        """
        Retrocede al paso anterior.

        Retorna:
            True si retrocedió, False si ya está en el primero.
        """
        e = self._estado
        if e.paso_actual > 0:
            e.paso_actual -= 1
            return True
        return False

    def obtener_paso_actual(self) -> OperacionFila | None:
        """
        Retorna la operación del paso actual.

        Retorna:
            OperacionFila del paso actual, o None si no hay pasos.
        """
        e = self._estado
        if not e.pasos:
            return None
        return e.pasos[e.paso_actual]

    def cifrar_con_clave_recuperada(self, texto: str) -> tuple[str, str]:
        """
        Cifra un texto usando la clave recuperada para verificar.

        Parametros:
            texto: Texto a cifrar.

        Retorna:
            Tupla (texto_cifrado, mensaje_error).
        """
        e = self._estado
        if not e.clave_recuperada:
            return "", "No hay clave recuperada aún."

        try:
            cifrador = CifradoHill(e.clave_recuperada, e.modulo)
            cifrado, _ = cifrador.cifrar(texto)
            return cifrado, ""
        except ValueError as exc:
            return "", str(exc)

    def descifrar_con_clave_recuperada(self, texto: str) -> tuple[str, str]:
        """
        Descifra un texto usando la clave recuperada para verificar.

        Parametros:
            texto: Texto a descifrar.

        Retorna:
            Tupla (texto_descifrado, mensaje_error).
        """
        e = self._estado
        if not e.clave_recuperada:
            return "", "No hay clave recuperada aún."

        try:
            cifrador = CifradoHill(e.clave_recuperada, e.modulo)
            descifrado, _ = cifrador.descifrar(texto)
            return descifrado, ""
        except ValueError as exc:
            return "", str(exc)

    def formatear_matriz(self, datos: list[list[int]]) -> str:
        """
        Formatea una matriz para mostrarla en la interfaz.

        Parametros:
            datos: Matriz como lista de listas.

        Retorna:
            Cadena de texto formateada.
        """
        lineas = []
        for fila in datos:
            contenido = "  ".join(str(v).rjust(3) for v in fila)
            lineas.append(f"│ {contenido} │")
        return "\n".join(lineas)

    def formatear_matriz_aumentada(
        self,
        datos: list[list[int]],
        n: int
    ) -> str:
        """
        Formatea la matriz aumentada mostrando el separador entre
        la parte izquierda y derecha.

        Parametros:
            datos: Matriz aumentada como lista de listas.
            n: Tamaño del bloque izquierdo.

        Retorna:
            Cadena de texto con separador visual.
        """
        lineas = []
        for fila in datos:
            izquierda = "  ".join(str(v).rjust(3) for v in fila[:n])
            derecha = "  ".join(str(v).rjust(3) for v in fila[n:])
            lineas.append(f"│ {izquierda} ║ {derecha} │")
        return "\n".join(lineas)
