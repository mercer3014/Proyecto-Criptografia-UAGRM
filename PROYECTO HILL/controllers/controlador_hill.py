from models.cifra_hill import ModeloCifraHill
from librerias.matematica import ALFABETO_27
from estilos import COLOR_EXITO, COLOR_ERROR


class ControladorCifraHill:
    def __init__(self, vista):
        self.modelo = ModeloCifraHill()
        self.vista = vista
        self.vista.establecer_controlador(self)

    def cambiar_modulo(self, modulo):
        try:
            self.modelo.establecer_modulo(modulo)
            self.vista.limpiar_campos()
            self.vista.etiqueta_estado.config(text=f"Modulo cambiado a {modulo}", fg=COLOR_EXITO)
        except ValueError as e:
            self.vista.etiqueta_estado.config(text=str(e), fg=COLOR_ERROR)

    def establecer_clave(self):
        try:
            modo = self.vista.obtener_modo_clave()
            if modo == "simbolica":
                clave = self.vista.obtener_clave_simbolica()
                if not clave:
                    self.vista.etiqueta_estado.config(text="Ingrese una clave", fg=COLOR_ERROR)
                    return
                self.modelo.construir_matriz_clave(clave)
            else:
                valores = self.vista.obtener_valores_numericos()
                flat = []
                for fila in valores:
                    for v in fila:
                        try:
                            flat.append(int(v))
                        except (ValueError, TypeError):
                            self.vista.etiqueta_estado.config(text="Valores invalidos", fg=COLOR_ERROR)
                            return
                self.modelo.construir_matriz_desde_numeros(flat)
            info = self.modelo.obtener_info_clave()
            self.vista.etiqueta_estado.config(text="Clave valida", fg=COLOR_EXITO)
            det = info["determinante"]
            mod = self.modelo.modulo
            lineas = [f"Matriz K (mod {mod}):"]
            for fila in info["matriz"]:
                lineas.append("  " + " ".join(f"{v:>3}" for v in fila))
            lineas.append(f"\ndet(K) = {det} mod {mod}")
            if info["inversa"]:
                lineas.append("\nMatriz K^(-1):")
                for fila in info["inversa"]:
                    lineas.append("  " + " ".join(f"{v:>3}" for v in fila))
            self.vista.caja_simulacion.actualizar("\n".join(lineas))
        except ValueError as e:
            self.vista.etiqueta_estado.config(text="Clave invalida", fg=COLOR_ERROR)
            self.vista.caja_simulacion.actualizar(str(e), COLOR_ERROR)

    def cifrar(self):
        if not self.modelo.tiene_clave():
            self.vista.caja_resultado.actualizar("Establezca una clave primero.", COLOR_ERROR)
            return
        texto = self.vista.obtener_texto()
        if not texto:
            self.vista.caja_resultado.actualizar("Ingrese un texto.", COLOR_ERROR)
            return
        try:
            resultado, pasos = self.modelo.cifrar(texto)
            self.vista.caja_resultado.actualizar(f"Cifrado: {resultado}", COLOR_EXITO)
            self._mostrar_pasos(pasos=pasos, modo="Cifrado")
        except Exception as e:
            self.vista.caja_resultado.actualizar(str(e), COLOR_ERROR)

    def descifrar(self):
        if not self.modelo.tiene_clave():
            self.vista.caja_resultado.actualizar("Establezca una clave primero.", COLOR_ERROR)
            return
        texto = self.vista.obtener_texto()
        if not texto:
            self.vista.caja_resultado.actualizar("Ingrese un texto.", COLOR_ERROR)
            return
        try:
            resultado, pasos = self.modelo.descifrar(texto)
            self.vista.caja_resultado.actualizar(f"Descifrado: {resultado}", COLOR_EXITO)
            self._mostrar_pasos(pasos=pasos, modo="Descifrado")
        except Exception as e:
            self.vista.caja_resultado.actualizar(str(e), COLOR_ERROR)

    def _mostrar_pasos(self, pasos, modo):
        mod = self.modelo.modulo
        lineas = []
        for paso in pasos:
            if paso.get("tipo") == "info_clave":
                lineas.append("=" * 55)
                lineas.append(f"  {modo} Hill (modulo {mod}) — Informacion de la clave")
                lineas.append("=" * 55)
                lineas.append("")
                lineas.append("Matriz clave K:")
                mat = paso["matriz"]
                if mod == 27:
                    for fila in mat:
                        nums = "  ".join(f"{v:>3}" for v in fila)
                        letras = "  ".join(ALFABETO_27[v] for v in fila)
                        lineas.append(f"  [ {nums} ]   ({letras})")
                else:
                    for fila in mat:
                        lineas.append("  [ " + "  ".join(f"{v:>3}" for v in fila) + " ]")
                det = paso["determinante"]
                det_mod = det % mod
                lineas.append("")
                lineas.append(f"det(K) = {det}")
                lineas.append(f"det(K) mod {mod} = {det_mod}")
                if paso.get("inverso_det") is not None:
                    lineas.append(f"det(K)^(-1) mod {mod} = {paso['inverso_det']}")
                lineas.append(f"Invertible: det(K)={det_mod} y mcd({det_mod}, {mod}) = 1")
                if paso.get("inversa") is not None:
                    lineas.append("")
                    lineas.append("Matriz inversa K^(-1):")
                    inv = paso["inversa"]
                    if mod == 27:
                        for fila in inv:
                            nums = "  ".join(f"{v:>3}" for v in fila)
                            letras = "  ".join(ALFABETO_27[v] for v in fila)
                            lineas.append(f"  [ {nums} ]   ({letras})")
                    else:
                        for fila in inv:
                            lineas.append("  [ " + "  ".join(f"{v:>3}" for v in fila) + " ]")
                lineas.append("")

            elif paso.get("tipo") == "conversion_inicial":
                lineas.append("-" * 55)
                texto_orig = paso.get("texto_original", "")
                texto_prep = paso.get("texto_preparado", "")
                if texto_orig != texto_prep:
                    lineas.append(f"Texto original:  \"{texto_orig}\"")
                    lineas.append(f"Texto preparado: \"{texto_prep}\"")
                else:
                    lineas.append(f"Texto de entrada: \"{texto_prep}\"")
                lineas.append("")
                if paso.get("mapeo_letras"):
                    pares = []
                    for c, n in paso["mapeo_letras"]:
                        pares.append(f"{c}={n}")
                    lineas.append("Conversion letra a numero:")
                    lineas.append("  " + ", ".join(pares))
                else:
                    lineas.append("Conversion a numeros:")
                    lineas.append("  " + ", ".join(str(n) for n in paso["numeros"]))
                bloques = paso["bloques"]
                lineas.append("")
                lineas.append(f"Division en bloques de 2:")
                for i, b in enumerate(bloques):
                    if mod == 27:
                        letras_bloque = "".join(ALFABETO_27[n] for n in b)
                        lineas.append(f"  Bloque {i+1}: [{b[0]}, {b[1]}] = \"{letras_bloque}\"")
                    else:
                        lineas.append(f"  Bloque {i+1}: [{b[0]}, {b[1]}]")
                if paso.get("relleno_usado"):
                    lineas.append("(Se agrego relleno para completar el ultimo bloque)")
                lineas.append("")

            elif paso.get("tipo") in ("bloque_cifrado", "bloque_descifrado"):
                es_cifrado = paso["tipo"] == "bloque_cifrado"
                num = paso["bloque_numero"]
                nombre_mat = "K" if es_cifrado else paso.get("nombre_matriz", "K^(-1)")
                mat_usada = paso.get("matriz_usada", self.modelo.matriz_clave if es_cifrado else self.modelo.matriz_inversa)
                vector = paso["vector_entrada"]
                detalle = paso.get("detalle_filas", [])
                lineas.append("-" * 55)
                if es_cifrado:
                    lineas.append(f"  BLOQUE {num}: Cifrado con {nombre_mat}")
                    if mod == 27:
                        letras_entrada = "".join(paso.get("letras_claro", []))
                        letras_salida = "".join(paso.get("letras_cifrado", []))
                        lineas.append(f"  Entrada: \"{letras_entrada}\" = [{vector[0]}, {vector[1]}]")
                        vals_salida = paso["valores_cifrado"]
                        lineas.append(f"  Salida:  \"{letras_salida}\" = [{vals_salida[0]}, {vals_salida[1]}]")
                    else:
                        lineas.append(f"  Entrada: [{vector[0]}, {vector[1]}]")
                        vals_salida = paso["valores_cifrado"]
                        lineas.append(f"  Salida:  [{vals_salida[0]}, {vals_salida[1]}]")
                else:
                    lineas.append(f"  BLOQUE {num}: Descifrado con {nombre_mat}")
                    if mod == 27:
                        letras_entrada = "".join(paso.get("letras_cifrado", []))
                        letras_salida = "".join(paso.get("letras_descifrado", []))
                        lineas.append(f"  Entrada: \"{letras_entrada}\" = [{vector[0]}, {vector[1]}]")
                        vals_salida = paso["valores_descifrado"]
                        lineas.append(f"  Salida:  \"{letras_salida}\" = [{vals_salida[0]}, {vals_salida[1]}]")
                    else:
                        lineas.append(f"  Entrada: [{vector[0]}, {vector[1]}]")
                        vals_salida = paso["valores_descifrado"]
                        lineas.append(f"  Salida:  [{vals_salida[0]}, {vals_salida[1]}]")
                lineas.append("")
                lineas.append(f"  Multiplicacion {nombre_mat} x vector:")
                if mod == 27:
                    v_letters = [ALFABETO_27[v] for v in vector]
                    lineas.append(f"         [{vector[0]:>3}] ({v_letters[0]})")
                    lineas.append(f"  {nombre_mat} x  [{vector[1]:>3}] ({v_letters[1]})")
                else:
                    lineas.append(f"         [{vector[0]:>3}]")
                    lineas.append(f"  {nombre_mat} x  [{vector[1]:>3}]")
                lineas.append("")
                for fila_info in detalle:
                    i = fila_info["fila"]
                    productos = fila_info["productos"]
                    suma_bruta = fila_info["suma_sin_mod"]
                    res_mod = fila_info["resultado_mod"]
                    mult_parts = []
                    sum_parts = []
                    for k_ij, v_j, prod_val in productos:
                        mult_parts.append(f"{k_ij}*{v_j}")
                        sum_parts.append(str(prod_val))
                    expr_mult = " + ".join(mult_parts)
                    expr_sum = " + ".join(sum_parts)
                    if mod == 27:
                        letra_res = ALFABETO_27[res_mod]
                        lineas.append(f"  Fila {i}: {expr_mult} = {expr_sum} = {suma_bruta}")
                        lineas.append(f"         {suma_bruta} mod {mod} = {res_mod} -> \"{letra_res}\"")
                    else:
                        lineas.append(f"  Fila {i}: {expr_mult} = {expr_sum} = {suma_bruta}")
                        lineas.append(f"         {suma_bruta} mod {mod} = {res_mod}")
                    lineas.append("")
                lineas.append(f"  Resultado del bloque {num}: [{vals_salida[0]}, {vals_salida[1]}]")
                if mod == 27 and es_cifrado:
                    lineas.append(f"  = \"" + "".join(paso.get("letras_cifrado", [])) + "\"")
                elif mod == 27 and not es_cifrado:
                    lineas.append(f"  = \"" + "".join(paso.get("letras_descifrado", [])) + "\"")
                lineas.append("")

            elif paso.get("tipo") == "resultado_final":
                lineas.append("=" * 55)
                lineas.append(f"  RESULTADO FINAL — {paso['modo']}")
                lineas.append("=" * 55)
                lineas.append("")
                nums = paso["numeros_resultado"]
                texto = paso["texto_resultado"]
                if paso.get("mapeo_resultado"):
                    pares = []
                    for n, l in paso["mapeo_resultado"]:
                        pares.append(f"{n}={l}")
                    lineas.append("Numeros -> Letras:")
                    lineas.append("  " + ", ".join(pares))
                else:
                    lineas.append("Numeros resultado: " + ", ".join(str(n) for n in nums))
                lineas.append("")
                lineas.append(f"{paso['modo']}: \"{texto}\"")
                lineas.append("")

        self.vista.caja_simulacion.actualizar("\n".join(lineas))

    def limpiar(self):
        self.vista.limpiar_campos()