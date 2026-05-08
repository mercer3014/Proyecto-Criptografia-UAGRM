from models.vectores_unitarios import ModeloVectoresUnitarios
from librerias.matematica import ALFABETO_27
from estilos import COLOR_EXITO, COLOR_ERROR


class ControladorVectoresUnitarios:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloVectoresUnitarios()
        self.vista.establecer_controlador(self)

    def establecer_clave(self):
        try:
            entradas = self.vista.obtener_clave()
            resultado = self.modelo.establecer_clave(entradas)
            det_mod = resultado["determinante"]
            inv = resultado["invertible"]
            inv_str = "Si" if inv else "No"
            self.vista.etiqueta_estado.config(
                text=f"det(K)={det_mod} mod 27 | Invertible: {inv_str}",
                fg=COLOR_EXITO if inv else COLOR_ERROR
            )
        except ValueError as e:
            self.vista.etiqueta_estado.config(text=str(e), fg=COLOR_ERROR)

    def cifrar_vector(self, indice):
        try:
            resultado = self.modelo.cifrar_vector_unitario(indice)
            lineas = []
            lineas.append("=" * 50)
            lineas.append(f"Cifrado del vector {resultado['texto_vector']} = {resultado['vector']}")
            lineas.append("=" * 50)
            lineas.append("")
            lineas.append("Matriz K:")
            for fila in self.modelo.clave_datos:
                nums = " ".join(f"{v:>3}" for v in fila)
                letras = " ".join(ALFABETO_27[v] for v in fila)
                lineas.append(f"  [{nums}]  ({letras})")
            lineas.append("")
            for paso in resultado["pasos"]:
                lineas.append(f"  Fila {paso['fila']+1}: {paso['operacion']} = {paso['resultado_parcial']} mod 27 = {paso['resultado_mod']} -> {paso['caracter']}")
            lineas.append("")
            lineas.append(f"Resultado: {resultado['resultado_numeros']} -> {resultado['resultado_texto']}")
            lineas.append(f"Columna {resultado['indice']+1} de K: {resultado['columna_k']} -> {resultado['columna_texto']}")
            if resultado["resultado_numeros"] == resultado["columna_k"]:
                lineas.append(f"Verificado: K x {resultado['texto_vector']} = Columna {resultado['indice']+1} de K")
            self.vista.caja_resultado.actualizar("\n".join(lineas))
        except ValueError as e:
            self.vista.caja_resultado.actualizar(f"Error: {e}", COLOR_ERROR)

    def cifrar_todos(self):
        try:
            resultados = self.modelo.cifrar_todos()
            lineas = []
            for r in resultados:
                lineas.append("=" * 50)
                lineas.append(f"Cifrado del vector {r['texto_vector']} = {r['vector']}")
                lineas.append("=" * 50)
                for paso in r["pasos"]:
                    lineas.append(f"  Fila {paso['fila']+1}: {paso['operacion']} = {paso['resultado_parcial']} mod 27 = {paso['resultado_mod']} -> {paso['caracter']}")
                lineas.append(f"Resultado: {r['resultado_numeros']} -> {r['resultado_texto']}")
                lineas.append(f"Columna {r['indice']+1} de K: {r['columna_k']} -> {r['columna_texto']}")
                lineas.append("")
            clave_lineas = ["Clave completa K:"]
            for fila in self.modelo.clave_datos:
                clave_lineas.append("  " + " ".join(f"{v:>3}" for v in fila))
            lineas.extend(clave_lineas)
            self.vista.caja_resultado.actualizar("\n".join(lineas))
        except ValueError as e:
            self.vista.caja_resultado.actualizar(f"Error: {e}", COLOR_ERROR)