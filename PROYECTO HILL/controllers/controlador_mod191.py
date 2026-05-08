from models.mod191 import ModeloMod191


class ControladorMod191:
    def __init__(self, vista):
        self.modelo = ModeloMod191()
        self.vista = vista
        self.vista.establecer_controlador(self)
        self._cargar_alfabeto()

    def cifrar(self):
        try:
            texto = self.vista.obtener_texto_entrada()
            clave = self.vista.obtener_clave()
            es_vig = self.vista.es_vigenere()
            if not texto:
                self.vista.mostrar_error("El texto no puede estar vacio.")
                return
            invalidos = self.modelo.validar_texto(texto)
            if invalidos:
                self.vista.mostrar_error(f"Caracteres invalidos: {', '.join(repr(c) for c in invalidos[:10])}")
                return
            if es_vig:
                if not clave:
                    self.vista.mostrar_error("La clave no puede estar vacia.")
                    return
                invalidos_clave = self.modelo.validar_texto(clave)
                if invalidos_clave:
                    self.vista.mostrar_error(f"Caracteres invalidos en clave: {', '.join(repr(c) for c in invalidos_clave[:10])}")
                    return
                resultado, pasos = self.modelo.cifrar_vigenere(texto, clave)
            else:
                try:
                    clave_num = int(clave)
                except ValueError:
                    self.vista.mostrar_error("Para Cesar, la clave debe ser un numero.")
                    return
                resultado, pasos = self.modelo.cifrar_cesar(texto, clave_num)
            self.vista.caja_resultado.actualizar(f"Resultado: {resultado}")
            self._mostrar_pasos(pasos, es_vig)
        except Exception as e:
            self.vista.mostrar_error(f"Error: {e}")

    def descifrar(self):
        try:
            texto = self.vista.obtener_texto_entrada()
            clave = self.vista.obtener_clave()
            es_vig = self.vista.es_vigenere()
            if not texto:
                self.vista.mostrar_error("El texto no puede estar vacio.")
                return
            invalidos = self.modelo.validar_texto(texto)
            if invalidos:
                self.vista.mostrar_error(f"Caracteres invalidos: {', '.join(repr(c) for c in invalidos[:10])}")
                return
            if es_vig:
                if not clave:
                    self.vista.mostrar_error("La clave no puede estar vacia.")
                    return
                invalidos_clave = self.modelo.validar_texto(clave)
                if invalidos_clave:
                    self.vista.mostrar_error(f"Caracteres invalidos en clave: {', '.join(repr(c) for c in invalidos_clave[:10])}")
                    return
                resultado, pasos = self.modelo.descifrar_vigenere(texto, clave)
            else:
                try:
                    clave_num = int(clave)
                except ValueError:
                    self.vista.mostrar_error("Para Cesar, la clave debe ser un numero.")
                    return
                resultado, pasos = self.modelo.descifrar_cesar(texto, clave_num)
            self.vista.caja_resultado.actualizar(f"Resultado: {resultado}")
            self._mostrar_pasos(pasos, es_vig)
        except Exception as e:
            self.vista.mostrar_error(f"Error: {e}")

    def _mostrar_pasos(self, pasos, es_vig):
        lineas = [f"Simulacion ({'Vigenere' if es_vig else 'Cesar'}):", ""]
        for p in pasos:
            linea = f"Paso {p['paso']}: '{p['caracter_original']}' [{p['indice_original']}]"
            linea += f" -> {p['operacion']} = {p['resultado_operacion']} -> '{p['caracter_resultado']}'"
            lineas.append(linea)
        self.vista.caja_simulacion.actualizar("\n".join(lineas))

    def _cargar_alfabeto(self):
        alfabeto_str = self.modelo.obtener_alfabeto_str()
        self.vista.mostrar_alfabeto(alfabeto_str)