"""
Controlador del simulador de ataque Gauss-Jordan.

Actúa como intermediario entre la Vista y el Modelo.
Recibe eventos de la interfaz, invoca la lógica del modelo
y actualiza la vista con los resultados.

Patrón: Controlador en MVC.
"""

from mvc.modelo import ModeloSimulador
from mvc.vista import VistaPrincipal, COLOR_RESALTADO, COLOR_TEXTO_SECUNDARIO


class Controlador:
    """
    Controlador principal de la aplicación.

    Coordina todas las interacciones entre la vista y el modelo,
    asegurando que la lógica de negocio esté separada de la interfaz.

    Atributos:
        modelo: Instancia del modelo del simulador.
        vista: Instancia de la vista principal.
    """

    def __init__(self, modelo: ModeloSimulador, vista: VistaPrincipal) -> None:
        self.modelo = modelo
        self.vista = vista
        self.vista.controlador = self

    def iniciar(self) -> None:
        """Inicia la aplicación."""
        self.vista.iniciar()

    # -----------------------------------------------------------------------
    # Handlers de eventos de la vista
    # -----------------------------------------------------------------------

    def on_construir_matriz(self) -> None:
        """
        Responde al botón 'Construir matriz'.

        Valida las entradas, construye la matriz aumentada
        y la muestra en la interfaz.
        """
        texto_claro = self.vista.obtener_texto_claro()
        texto_cifrado = self.vista.obtener_texto_cifrado()
        n = self.vista.obtener_n()

        if not texto_claro:
            self.vista.mostrar_error("Ingrese el texto claro.")
            return

        if not texto_cifrado:
            self.vista.mostrar_error("Ingrese el texto cifrado.")
            return

        exito = self.modelo.configurar(texto_claro, texto_cifrado, n)

        if not exito:
            self.vista.mostrar_matriz_inicial(
                texto=self.modelo.estado.error,
                mensaje=self.modelo.estado.error,
                es_error=True
            )
            return

        # Formatear la matriz aumentada para mostrarla
        datos = self.modelo.estado.matriz_aumentada
        texto_mat = self._formatear_matriz_con_encabezado(datos, n)

        self.vista.mostrar_matriz_inicial(
            texto=texto_mat,
            mensaje=(
                f"Matriz construida: {n}×{2*n} "
                f"(n={n}, mod {self.modelo.estado.modulo})"
            )
        )

    def on_ejecutar_ataque(self) -> None:
        """
        Responde al botón 'Ejecutar ataque completo'.

        Configura si aún no lo está, ejecuta Gauss-Jordan,
        muestra los pasos y navega a la pestaña de simulación.
        """
        # Si no está configurado, intentar configurar primero
        if not self.modelo.estado.listo:
            self.on_construir_matriz()
            if not self.modelo.estado.listo:
                return

        exito = self.modelo.ejecutar_ataque()

        if not exito:
            self.vista.mostrar_error(self.modelo.estado.error)
            return

        total = len(self.modelo.estado.pasos)

        if total == 0:
            self.vista.mostrar_info(
                "No fueron necesarias operaciones de fila.\n"
                "La matriz ya estaba en forma identidad."
            )
        else:
            # Mostrar el primer paso
            self._actualizar_vista_paso()

        # Mostrar la clave recuperada
        self._mostrar_clave_recuperada()

        # Ir a la pestaña de simulación
        self.vista.ir_a_pestana(1)

    def on_siguiente_paso(self) -> None:
        """Avanza al siguiente paso y actualiza la vista."""
        avanzo = self.modelo.siguiente_paso()
        self._actualizar_vista_paso()

        if not avanzo:
            self.vista.mostrar_info(
                "Ha llegado al último paso.\n"
                "La clave ha sido recuperada exitosamente."
            )

    def on_paso_anterior(self) -> None:
        """Retrocede al paso anterior y actualiza la vista."""
        self.modelo.paso_anterior()
        self._actualizar_vista_paso()

    def on_ir_a_paso(self, indice: int) -> None:
        """Navega a un paso específico."""
        self.modelo.ir_a_paso(indice)
        self._actualizar_vista_paso()

    def on_ir_al_ultimo_paso(self) -> None:
        """Navega al último paso."""
        total = len(self.modelo.estado.pasos)
        if total > 0:
            self.modelo.ir_a_paso(total - 1)
            self._actualizar_vista_paso()

    def on_verificar(self) -> None:
        """
        Responde al botón de verificación.

        Cifra o descifra el texto ingresado usando la clave recuperada.
        """
        texto = self.vista.obtener_entrada_verificacion()
        modo = self.vista.obtener_modo_verificar()

        if not texto:
            self.vista.mostrar_error("Ingrese un texto para verificar.")
            return

        if not self.modelo.estado.clave_recuperada:
            self.vista.mostrar_error(
                "Primero ejecute el ataque para recuperar la clave."
            )
            return

        if modo == "cifrar":
            resultado, error = self.modelo.cifrar_con_clave_recuperada(texto)
        else:
            resultado, error = self.modelo.descifrar_con_clave_recuperada(texto)

        if error:
            self.vista.mostrar_resultado_verificacion(error, es_error=True)
            return

        self.vista.mostrar_resultado_verificacion(
            f"Entrada:   {texto.upper()}\n"
            f"Resultado: {resultado}\n"
            f"Modo: {'Cifrado' if modo == 'cifrar' else 'Descifrado'} "
            f"con clave K recuperada."
        )

    def on_reiniciar(self) -> None:
        """Reinicia el simulador a su estado inicial."""
        self.modelo.reiniciar()
        self.vista._var_texto_claro.set("")
        self.vista._var_texto_cifrado.set("")
        self.vista._var_n.set(2)
        self.vista._var_verificar_entrada.set("")
        self.vista._var_modo_verificar.set("cifrar")
        self.vista.mostrar_matriz_inicial("", "Simulador reiniciado.")
        self.vista._etiqueta_operacion.config(
            text="Presione 'Ejecutar ataque completo' en la pestaña anterior.",
            fg=COLOR_RESALTADO
        )
        self.vista._etiqueta_tipo_operacion.config(text="")
        self.vista._etiqueta_progreso.config(text="Paso 0 / 0")
        self.vista._caja_antes.actualizar("")
        self.vista._caja_despues.actualizar("")
        self.vista.mostrar_clave_recuperada("(pendiente de calcular)")
        self.vista._etiqueta_clave.config(fg=COLOR_TEXTO_SECUNDARIO)
        self.vista.mostrar_resultado_verificacion("")
        self.vista.mostrar_info_clave("")

    # -----------------------------------------------------------------------
    # Métodos auxiliares privados
    # -----------------------------------------------------------------------

    def _actualizar_vista_paso(self) -> None:
        """
        Actualiza la pestaña de simulación con el paso actual del modelo.
        """
        paso = self.modelo.obtener_paso_actual()
        estado = self.modelo.estado

        if paso is None:
            self.vista.actualizar_paso(
                descripcion_operacion="Sin operaciones que mostrar.",
                tipo_operacion="",
                texto_antes="",
                texto_despues="",
                numero_paso=0,
                total_pasos=0,
                n=estado.n
            )
            return

        n = estado.n
        total = len(estado.pasos)
        actual = estado.paso_actual + 1

        texto_antes = self._formatear_matriz_con_encabezado(
            paso.estado_antes, n
        )
        texto_despues = self._formatear_matriz_con_encabezado(
            paso.estado_despues, n
        )

        self.vista.actualizar_paso(
            descripcion_operacion=paso.descripcion,
            tipo_operacion=paso.tipo,
            texto_antes=texto_antes,
            texto_despues=texto_despues,
            numero_paso=actual,
            total_pasos=total,
            n=n
        )

    def _mostrar_clave_recuperada(self) -> None:
        """Muestra la clave recuperada en la interfaz."""
        clave = self.modelo.estado.clave_recuperada

        if not clave:
            return

        n = len(clave)

        # Formato compacto para la barra inferior
        filas_compactas = []
        for fila in clave:
            contenido = " ".join(str(v).rjust(3) for v in fila)
            filas_compactas.append(f"[ {contenido} ]")
        texto_compacto = "  ".join(filas_compactas)

        self.vista.mostrar_clave_recuperada(texto_compacto)

        # Información detallada para la pestaña de verificación
        lineas = [
            "Clave recuperada K (matriz de cifrado Hill):",
            "=" * 40,
            ""
        ]

        for fila in clave:
            contenido = "  ".join(str(v).rjust(4) for v in fila)
            lineas.append(f"  [ {contenido} ]")

        lineas += [
            "",
            f"Dimensión: {n}×{n}",
            f"Módulo: {self.modelo.estado.modulo}",
            "",
            "Ecuación de cifrado:  C = K × P (mod 26)",
            "Ecuación de descifrado: P = K⁻¹ × C (mod 26)",
            "",
            "Esta clave fue recuperada a partir del texto claro",
            "y el texto cifrado conocidos, usando el método",
            "Gauss-Jordan en aritmética modular."
        ]

        self.vista.mostrar_info_clave("\n".join(lineas))

    def _formatear_matriz_con_encabezado(
        self,
        datos: list[list[int]],
        n: int
    ) -> str:
        """
        Formatea una matriz aumentada con encabezado explicativo.

        Parametros:
            datos: Matriz como lista de listas.
            n: Tamaño de la parte izquierda.

        Retorna:
            Cadena de texto formateada para mostrar en la interfaz.
        """
        total_cols = len(datos[0]) if datos else 0

        # Encabezado de columnas
        izq_header = " ".join(
            f"P{j+1}".rjust(4) for j in range(n)
        )
        der_header = " ".join(
            f"C{j+1}".rjust(4) for j in range(total_cols - n)
        )
        encabezado = f"  {izq_header}  ║  {der_header}"

        separador = "-" * len(encabezado)

        lineas = [encabezado, separador]

        for i, fila in enumerate(datos):
            izquierda = "  ".join(str(v).rjust(3) for v in fila[:n])
            derecha = "  ".join(str(v).rjust(3) for v in fila[n:])
            lineas.append(f"F{i+1} │ {izquierda}  ║  {derecha} │")

        return "\n".join(lineas)
