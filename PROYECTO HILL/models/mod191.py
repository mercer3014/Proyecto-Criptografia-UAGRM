from librerias.alfabeto_mod191 import AlfabetoMod191, CifradoMod191


class ModeloMod191:

    def __init__(self):
        self.alfabeto = AlfabetoMod191()
        self.cifrador = CifradoMod191(self.alfabeto)

    def cifrar_cesar(self, texto, clave):
        return self.cifrador.cifrar_cesar_pasos(texto, clave)

    def descifrar_cesar(self, texto, clave):
        return self.cifrador.descifrar_cesar_pasos(texto, clave)

    def cifrar_vigenere(self, texto, clave):
        return self.cifrador.cifrar_vigenere_pasos(texto, clave)

    def descifrar_vigenere(self, texto, clave):
        return self.cifrador.descifrar_vigenere_pasos(texto, clave)

    def obtener_alfabeto_str(self):
        return self.alfabeto.generar_diccionario_str()

    def validar_texto(self, texto):
        return self.alfabeto.validar_texto(texto)