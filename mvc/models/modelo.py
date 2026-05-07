from librerias.matrices import Matriz
from librerias.matematica import inverso_modular

class SimuladorGaussJordan:
    def __init__(self, modulo=26):
        self.modulo = modulo
        self.matriz_aumentada = None
        self.n = 0
        self.pasos = []          # cada paso: {'descripcion': str, 'matriz': Matriz}
        self.paso_actual = -1
        self.finalizado = False
        self.exito = False

    def establecer_matrices(self, matriz_plana, matriz_cifrada):
        if matriz_plana.filas != matriz_plana.columnas:
            raise ValueError("La matriz de texto claro debe ser cuadrada")
        if matriz_plana.filas != matriz_cifrada.filas or matriz_plana.columnas != matriz_cifrada.columnas:
            raise ValueError("Las dimensiones de las matrices deben coincidir")
        n = matriz_plana.filas
        datos = []
        for i in range(n):
            datos.append(matriz_plana[i][:] + matriz_cifrada[i][:])
        self.matriz_aumentada = Matriz(datos)
        self.n = n
        self.pasos = []
        self.paso_actual = -1
        self.finalizado = False
        self.exito = False
        self._agregar_paso("Matriz aumentada inicial [P | C]", self.matriz_aumentada.copiar())

    def _agregar_paso(self, descripcion, matriz_copia):
        self.pasos.append({'descripcion': descripcion, 'matriz': matriz_copia})
        self.paso_actual = len(self.pasos) - 1

    def ejecutar_gauss_jordan(self):
        if self.matriz_aumentada is None:
            raise ValueError("No se ha cargado ninguna matriz")
        M = self.matriz_aumentada.copiar()
        n = self.n
        mod = self.modulo

        for col in range(n):
            # Buscar pivote invertible
            pivote_fila = -1
            for fila in range(col, n):
                val = M[fila][col]
                if val != 0 and inverso_modular(val % mod, mod) is not None:
                    pivote_fila = fila
                    break
            if pivote_fila == -1:
                self._agregar_paso(f"No se encontró pivote invertible en columna {col+1}. "
                                   f"La matriz P no es invertible módulo {mod}. Ataque fallido.", M.copiar())
                self.finalizado = True
                self.exito = False
                return

            if pivote_fila != col:
                M.intercambiar_filas(col, pivote_fila)
                self._agregar_paso(f"Intercambiar fila {col+1} con fila {pivote_fila+1}", M.copiar())

            pivote = M[col][col] % mod
            inv_pivote = inverso_modular(pivote, mod)
            M.multiplicar_fila(col, inv_pivote, mod)
            self._agregar_paso(f"Multiplicar fila {col+1} por {inv_pivote} (inverso de {pivote})", M.copiar())

            # Hacer ceros en las demás filas
            for fila in range(n):
                if fila != col:
                    factor = (-M[fila][col]) % mod
                    if factor != 0:
                        M.sumar_fila_multiplo(fila, col, factor, mod)
                        self._agregar_paso(f"Fila {fila+1} = Fila {fila+1} + ({factor}) * Fila {col+1}", M.copiar())

        # Verificar identidad izquierda
        identidad = True
        for i in range(n):
            for j in range(n):
                if i == j:
                    if M[i][j] != 1:
                        identidad = False
                else:
                    if M[i][j] != 0:
                        identidad = False
        if identidad:
            self._agregar_paso("¡Proceso completado! La parte izquierda es la identidad. "
                               "La clave (K) es la parte derecha.", M.copiar())
            self.exito = True
        else:
            self._agregar_paso("La matriz P no pudo ser reducida a la identidad. Ataque fallido.", M.copiar())
            self.exito = False
        self.finalizado = True

    def obtener_pasos(self):
        return self.pasos

    def obtener_paso(self, indice):
        if 0 <= indice < len(self.pasos):
            return self.pasos[indice]
        return None

    def obtener_clave(self):
        if self.exito and self.finalizado:
            ultimo = self.pasos[-1]['matriz']
            n = self.n
            clave_datos = [ultimo[i][n:] for i in range(n)]
            return Matriz(clave_datos)
        return None
