from librerias.matematica import ALFABETO_27, reducir_mod, inverso_modular, es_coprimo
from librerias.matrices import Matriz, calcular_determinante, multiplicar_matrices, es_invertible
from librerias.matematica import numeros_a_texto


class ModeloVectoresUnitarios:
    MODULO = 27

    VECTORES_UNITARIOS = {
        0: {
            "vector": [1, 0, 0],
            "texto": "BAA",
            "columna": 0,
        },
        1: {
            "vector": [0, 1, 0],
            "texto": "ABA",
            "columna": 1,
        },
        2: {
            "vector": [0, 0, 1],
            "texto": "AAB",
            "columna": 2,
        },
    }

    def __init__(self):
        self.clave = None
        self.clave_datos = None
        self.invertible = False
        self.determinante = None

    def _parsear_entrada(self, valor, fila, col):
        valor = str(valor).strip()
        if valor == "":
            raise ValueError(f"Celda [{fila},{col}] vacía.")
        try:
            numero = int(valor)
            if numero < 0 or numero > 26:
                raise ValueError(f"Número {numero} fuera de rango (0-26) en [{fila},{col}].")
            return numero
        except ValueError:
            if len(valor) == 1 and valor.upper() in ALFABETO_27:
                return ALFABETO_27.index(valor.upper())
            raise ValueError(f"Entrada inválida '{valor}' en [{fila},{col}]. Use número (0-26) o letra del alfabeto.")

    def establecer_clave(self, entradas):
        datos = []
        for i in range(3):
            fila = []
            for j in range(3):
                fila.append(self._parsear_entrada(entradas[i][j], i, j))
            datos.append(fila)

        det = calcular_determinante(datos, self.MODULO)
        det_mod = det % self.MODULO
        inv = None
        try:
            inv = inverso_modular(det_mod, self.MODULO)
        except ValueError:
            pass

        self.clave_datos = datos
        self.clave = Matriz(datos, self.MODULO)
        self.determinante = det_mod
        self.invertible = es_invertible(datos, self.MODULO)

        return {
            "clave_datos": datos,
            "determinante": det_mod,
            "invertible": self.invertible,
        }

    def cifrar_vector_unitario(self, indice):
        if indice not in self.VECTORES_UNITARIOS:
            raise ValueError(f"Índice de vector unitario inválido: {indice}")
        if self.clave is None:
            raise ValueError("No se ha establecido una clave.")

        info = self.VECTORES_UNITARIOS[indice]
        vector = info["vector"]

        vector_matriz = Matriz([[v] for v in vector], self.MODULO)
        resultado_mat = multiplicar_matrices(self.clave, vector_matriz, self.MODULO)
        resultado_nums = [resultado_mat.obtener(i, 0) for i in range(3)]
        resultado_texto = numeros_a_texto(resultado_nums, self.MODULO)

        columna_k = [self.clave.obtener(i, indice) for i in range(3)]
        columna_texto = numeros_a_texto(columna_k, self.MODULO)

        pasos = []
        for i in range(3):
            componentes = []
            for j in range(3):
                k_val = self.clave.obtener(i, j)
                v_val = vector[j]
                componentes.append(f"{k_val}*{v_val}")
            suma = " + ".join(componentes)
            paso = {
                "fila": i,
                "operacion": suma,
                "resultado_parcial": sum(self.clave.obtener(i, j) * vector[j] for j in range(3)),
                "resultado_mod": resultado_nums[i],
                "caracter": resultado_texto[i],
            }
            pasos.append(paso)

        return {
            "indice": indice,
            "vector": vector,
            "texto_vector": info["texto"],
            "resultado_numeros": resultado_nums,
            "resultado_texto": resultado_texto,
            "columna_k": columna_k,
            "columna_texto": columna_texto,
            "pasos": pasos,
        }

    def cifrar_todos(self):
        if self.clave is None:
            raise ValueError("No se ha establecido una clave.")
        resultados = []
        for i in range(3):
            resultados.append(self.cifrar_vector_unitario(i))
        return resultados