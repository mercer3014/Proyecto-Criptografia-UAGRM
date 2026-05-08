from librerias.matematica import (
    ALFABETO_27, texto_a_numeros, numeros_a_texto, reducir_mod,
    inverso_modular, es_coprimo, char_to_int, int_to_char
)
from librerias.matrices import (
    Matriz, multiplicar_matrices, calcular_determinante, calcular_inversa,
    es_invertible
)


class ModeloCifraHill:

    def __init__(self):
        self.modulo = 27
        self.matriz_clave = None
        self.matriz_inversa = None
        self._alfabeto_mod191 = None

    def _obtener_alfabeto_mod191(self):
        if self._alfabeto_mod191 is None:
            from librerias.alfabeto_mod191 import AlfabetoMod191
            self._alfabeto_mod191 = AlfabetoMod191()
        return self._alfabeto_mod191

    def establecer_modulo(self, modulo):
        if modulo not in (27, 191):
            raise ValueError("El módulo debe ser 27 o 191.")
        self.modulo = modulo
        self.matriz_clave = None
        self.matriz_inversa = None

    def _texto_a_numeros(self, texto):
        if self.modulo == 27:
            return texto_a_numeros(texto, 27)
        alfabeto = self._obtener_alfabeto_mod191()
        resultado = []
        for c in texto:
            resultado.append(alfabeto.obtener_indice(c))
        return resultado

    def _numeros_a_texto(self, numeros):
        if self.modulo == 27:
            return numeros_a_texto(numeros, 27)
        alfabeto = self._obtener_alfabeto_mod191()
        resultado = []
        for n in numeros:
            resultado.append(alfabeto.obtener_caracter(n % self.modulo))
        return ''.join(resultado)

    def construir_matriz_clave(self, clave_texto):
        if self.modulo == 27:
            clave_texto = clave_texto.upper()
        if len(clave_texto) != 4:
            raise ValueError("La clave debe tener 4 caracteres para una matriz 2x2.")
        numeros = self._texto_a_numeros(clave_texto)
        datos = [
            [numeros[0], numeros[1]],
            [numeros[2], numeros[3]],
        ]
        if not es_invertible(datos, self.modulo):
            raise ValueError("La clave no es invertible en el módulo seleccionado.")
        self.matriz_clave = datos
        self.matriz_inversa = calcular_inversa(datos, self.modulo)
        return datos

    def construir_matriz_desde_numeros(self, valores):
        if len(valores) != 4:
            raise ValueError("Se necesitan 4 valores para una matriz 2x2.")
        datos = [
            [reducir_mod(valores[0], self.modulo), reducir_mod(valores[1], self.modulo)],
            [reducir_mod(valores[2], self.modulo), reducir_mod(valores[3], self.modulo)],
        ]
        if not es_invertible(datos, self.modulo):
            raise ValueError("La matriz no es invertible en el módulo seleccionado.")
        self.matriz_clave = datos
        self.matriz_inversa = calcular_inversa(datos, self.modulo)
        return datos

    def es_invertible(self):
        if self.matriz_clave is None:
            return False
        return es_invertible(self.matriz_clave, self.modulo)

    def obtener_determinante(self):
        if self.matriz_clave is None:
            return None
        return calcular_determinante(self.matriz_clave, self.modulo)

    def obtener_inversa(self):
        if self.matriz_inversa is None:
            return None
        return self.matriz_inversa

    def tiene_clave(self):
        return self.matriz_clave is not None

    def _preparar_bloques(self, texto):
        numeros = self._texto_a_numeros(texto)
        if self.modulo == 27:
            relleno = ALFABETO_27.index('X')
        else:
            relleno = ord('X') % self.modulo
        while len(numeros) % 2 != 0:
            numeros.append(relleno % self.modulo)
        bloques = []
        for i in range(0, len(numeros), 2):
            bloques.append(numeros[i:i + 2])
        return bloques

    def cifrar(self, texto):
        if self.matriz_clave is None:
            raise ValueError("No se ha establecido una clave.")
        texto_preparado = texto.upper().replace(" ", "") if self.modulo == 27 else texto
        numeros_originales = self._texto_a_numeros(texto_preparado)
        bloques = self._preparar_bloques(texto)
        clave_mat = Matriz(self.matriz_clave, self.modulo)
        resultado_numeros = []
        pasos = []
        paso_info = {
            "tipo": "info_clave",
            "matriz": self.matriz_clave,
            "determinante": self.obtener_determinante(),
            "modulo": self.modulo,
        }
        inv_det = None
        try:
            inv_det = inverso_modular(self.obtener_determinante() % self.modulo, self.modulo)
        except ValueError:
            pass
        paso_info["inverso_det"] = inv_det
        if self.matriz_inversa is not None:
            paso_info["inversa"] = self.matriz_inversa
        pasos.append(paso_info)
        paso_conversion = {
            "tipo": "conversion_inicial",
            "texto_original": texto,
            "texto_preparado": texto_preparado,
            "numeros": numeros_originales,
            "bloques": bloques,
            "relleno_usado": len(numeros_originales) != len(bloques) * 2,
            "modulo": self.modulo,
        }
        if self.modulo == 27:
            paso_conversion["mapeo_letras"] = [(c, n) for c, n in zip(texto_preparado, numeros_originales)]
        pasos.append(paso_conversion)
        for idx, bloque in enumerate(bloques):
            bloque_mat = Matriz([[v] for v in bloque], self.modulo)
            resultado_mat = multiplicar_matrices(clave_mat, bloque_mat, self.modulo)
            cifrado_bloque = [resultado_mat.obtener(i, 0) for i in range(2)]
            detalle_filas = []
            for i in range(2):
                productos = []
                for j in range(2):
                    productos.append((self.matriz_clave[i][j], bloque[j], self.matriz_clave[i][j] * bloque[j]))
                suma_sin_mod = sum(p[2] for p in productos)
                resultado_mod = reducir_mod(suma_sin_mod, self.modulo)
                detalle_filas.append({
                    "fila": i + 1,
                    "productos": productos,
                    "suma_sin_mod": suma_sin_mod,
                    "resultado_mod": resultado_mod,
                })
            paso_bloque = {
                "tipo": "bloque_cifrado",
                "bloque_numero": idx + 1,
                "texto_claro": self._numeros_a_texto(bloque),
                "valores_claro": bloque,
                "valores_cifrado": cifrado_bloque,
                "texto_cifrado": self._numeros_a_texto(cifrado_bloque),
                "detalle_filas": detalle_filas,
                "matriz_usada": self.matriz_clave,
                "vector_entrada": bloque,
                "modulo": self.modulo,
            }
            if self.modulo == 27:
                paso_bloque["letras_claro"] = [ALFABETO_27[n] for n in bloque]
                paso_bloque["letras_cifrado"] = [ALFABETO_27[n] for n in cifrado_bloque]
            pasos.append(paso_bloque)
            resultado_numeros.extend(cifrado_bloque)
        paso_final = {
            "tipo": "resultado_final",
            "numeros_resultado": resultado_numeros,
            "texto_resultado": self._numeros_a_texto(resultado_numeros),
            "modulo": self.modulo,
            "modo": "Cifrado",
        }
        if self.modulo == 27:
            paso_final["mapeo_resultado"] = [(n, ALFABETO_27[n]) for n in resultado_numeros]
        pasos.append(paso_final)
        return self._numeros_a_texto(resultado_numeros), pasos

    def descifrar(self, texto):
        if self.matriz_clave is None:
            raise ValueError("No se ha establecido una clave.")
        if self.matriz_inversa is None:
            raise ValueError("No se ha calculado la matriz inversa.")
        texto_preparado = texto.upper().replace(" ", "") if self.modulo == 27 else texto
        numeros_originales = self._texto_a_numeros(texto_preparado)
        bloques = self._preparar_bloques(texto)
        inv_mat = Matriz(self.matriz_inversa, self.modulo)
        resultado_numeros = []
        pasos = []
        paso_info = {
            "tipo": "info_clave",
            "matriz": self.matriz_clave,
            "inversa": self.matriz_inversa,
            "determinante": self.obtener_determinante(),
            "modulo": self.modulo,
        }
        inv_det = None
        try:
            inv_det = inverso_modular(self.obtener_determinante() % self.modulo, self.modulo)
        except ValueError:
            pass
        paso_info["inverso_det"] = inv_det
        pasos.append(paso_info)
        paso_conversion = {
            "tipo": "conversion_inicial",
            "texto_original": texto,
            "texto_preparado": texto_preparado,
            "numeros": numeros_originales,
            "bloques": bloques,
            "relleno_usado": len(numeros_originales) != len(bloques) * 2,
            "modulo": self.modulo,
        }
        if self.modulo == 27:
            paso_conversion["mapeo_letras"] = [(c, n) for c, n in zip(texto_preparado, numeros_originales)]
        pasos.append(paso_conversion)
        for idx, bloque in enumerate(bloques):
            bloque_mat = Matriz([[v] for v in bloque], self.modulo)
            resultado_mat = multiplicar_matrices(inv_mat, bloque_mat, self.modulo)
            descifrado_bloque = [resultado_mat.obtener(i, 0) for i in range(2)]
            detalle_filas = []
            for i in range(2):
                productos = []
                for j in range(2):
                    productos.append((self.matriz_inversa[i][j], bloque[j], self.matriz_inversa[i][j] * bloque[j]))
                suma_sin_mod = sum(p[2] for p in productos)
                resultado_mod = reducir_mod(suma_sin_mod, self.modulo)
                detalle_filas.append({
                    "fila": i + 1,
                    "productos": productos,
                    "suma_sin_mod": suma_sin_mod,
                    "resultado_mod": resultado_mod,
                })
            paso_bloque = {
                "tipo": "bloque_descifrado",
                "bloque_numero": idx + 1,
                "texto_cifrado": self._numeros_a_texto(bloque),
                "valores_cifrado": bloque,
                "valores_descifrado": descifrado_bloque,
                "texto_descifrado": self._numeros_a_texto(descifrado_bloque),
                "detalle_filas": detalle_filas,
                "matriz_usada": self.matriz_inversa,
                "nombre_matriz": "K^(-1)",
                "vector_entrada": bloque,
                "modulo": self.modulo,
            }
            if self.modulo == 27:
                paso_bloque["letras_cifrado"] = [ALFABETO_27[n] for n in bloque]
                paso_bloque["letras_descifrado"] = [ALFABETO_27[n] for n in descifrado_bloque]
            pasos.append(paso_bloque)
            resultado_numeros.extend(descifrado_bloque)
        paso_final = {
            "tipo": "resultado_final",
            "numeros_resultado": resultado_numeros,
            "texto_resultado": self._numeros_a_texto(resultado_numeros),
            "modulo": self.modulo,
            "modo": "Descifrado",
        }
        if self.modulo == 27:
            paso_final["mapeo_resultado"] = [(n, ALFABETO_27[n]) for n in resultado_numeros]
        pasos.append(paso_final)
        return self._numeros_a_texto(resultado_numeros), pasos

    def obtener_info_clave(self):
        if self.matriz_clave is None:
            return None
        det = calcular_determinante(self.matriz_clave, self.modulo)
        return {
            "matriz": self.matriz_clave,
            "determinante": det,
            "inversa": self.matriz_inversa,
        }

    def validar_texto(self, texto):
        if self.modulo == 27:
            texto = texto.upper().replace(" ", "")
            for c in texto:
                if c not in ALFABETO_27:
                    return False
            return True
        alfabeto = self._obtener_alfabeto_mod191()
        invalidos = alfabeto.validar_texto(texto)
        return len(invalidos) == 0

    def validar_clave_simbolica(self, clave):
        if len(clave) != 4:
            return False
        try:
            self._texto_a_numeros(clave)
            return True
        except (ValueError, KeyError):
            return False

    def _formatear_matriz(self, datos):
        lineas = []
        for fila in datos:
            partes = [str(val).rjust(3) for val in fila]
            lineas.append("[ " + "  ".join(partes) + " ]")
        return "\n".join(lineas)

    def _formatear_multiplicacion(self, matriz, vector, resultado):
        lineas = []
        for i in range(2):
            componentes = []
            for j in range(2):
                componentes.append(f"{matriz[i][j]}*{vector[j]}")
            suma_expr = " + ".join(componentes)
            valor = sum(matriz[i][j] * vector[j] for j in range(2))
            lineas.append(f"{suma_expr} = {valor} mod {self.modulo} = {resultado[i]}")
        return "\n".join(lineas)