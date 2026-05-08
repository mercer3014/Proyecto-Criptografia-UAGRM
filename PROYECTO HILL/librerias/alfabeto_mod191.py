CARACTERES_CP437 = (
        # === Posiciones 0-31: Caracteres de control con glifos CP437 ===
        '\x00',  # 0   - NUL (carácter nulo)
        '☺',     # 1   - SOH (cara sonriente blanca)
        '☻',     # 2   - STX (cara sonriente negra)
        '♥',     # 3   - ETX (corazón negro)
        '♦',     # 4   - EOT (diamante negro)
        '♣',     # 5   - ENQ (trébol negro)
        '♠',     # 6   - ACK (pica negra)
        '•',     # 7   - BEL (punto)
        '◘',     # 8   - BS (círculo invertido)
        '○',     # 9   - TAB (círculo blanco)
        '◙',     # 10  - LF (círculo con punto)
        '♂',     # 11  - VT (símbolo masculino)
        '♀',     # 12  - FF (símbolo femenino)
        '♪',     # 13  - CR (nota musical)
        '♫',     # 14  - SO (doble nota musical)
        '☼',     # 15  - SI (sol)
        '►',     # 16  - DLE (triángulo derecha)
        '◄',     # 17  - DC1 (triángulo izquierda)
        '↕',     # 18  - DC2 (doble flecha vertical)
        '‼',     # 19  - DC3 (doble exclamación)
        '¶',     # 20  - DC4 (signo de párrafo)
        '§',     # 21  - NAK (signo de sección)
        '▬',     # 22  - SYN (rectángulo horizontal)
        '↨',     # 23  - ETB (doble flecha con base)
        '↑',     # 24  - CAN (flecha arriba)
        '↓',     # 25  - EM (flecha abajo)
        '→',     # 26  - SUB (flecha derecha)
        '←',     # 27  - ESC (flecha izquierda)
        '∟',     # 28  - FS (ángulo recto)
        '↔',     # 29  - GS (doble flecha horizontal)
        '▲',     # 30  - RS (triángulo arriba)
        '▼',     # 31  - US (triángulo abajo)
        
        # === Posiciones 32-126: ASCII imprimible estándar ===
        ' ',     # 32
        '!',     # 33
        '"',     # 34
        '#',     # 35
        '$',     # 36
        '%',     # 37
        '&',     # 38
        "'",     # 39
        '(',     # 40
        ')',     # 41
        '*',     # 42
        '+',     # 43
        ',',     # 44
        '-',     # 45
        '.',     # 46
        '/',     # 47
        '0',     # 48
        '1',     # 49
        '2',     # 50
        '3',     # 51
        '4',     # 52
        '5',     # 53
        '6',     # 54
        '7',     # 55
        '8',     # 56
        '9',     # 57
        ':',     # 58
        ';',     # 59
        '<',     # 60
        '=',     # 61
        '>',     # 62
        '?',     # 63
        '@',     # 64
        'A',     # 65
        'B',     # 66
        'C',     # 67
        'D',     # 68
        'E',     # 69
        'F',     # 70
        'G',     # 71
        'H',     # 72
        'I',     # 73
        'J',     # 74
        'K',     # 75
        'L',     # 76
        'M',     # 77
        'N',     # 78
        'O',     # 79
        'P',     # 80
        'Q',     # 81
        'R',     # 82
        'S',     # 83
        'T',     # 84
        'U',     # 85
        'V',     # 86
        'W',     # 87
        'X',     # 88
        'Y',     # 89
        'Z',     # 90
        '[',     # 91
        '\\',    # 92
        ']',     # 93
        '^',     # 94
        '_',     # 95
        '`',     # 96
        'a',     # 97
        'b',     # 98
        'c',     # 99
        'd',     # 100
        'e',     # 101
        'f',     # 102
        'g',     # 103
        'h',     # 104
        'i',     # 105
        'j',     # 106
        'k',     # 107
        'l',     # 108
        'm',     # 109
        'n',     # 110
        'o',     # 111
        'p',     # 112
        'q',     # 113
        'r',     # 114
        's',     # 115
        't',     # 116
        'u',     # 117
        'v',     # 118
        'w',     # 119
        'x',     # 120
        'y',     # 121
        'z',     # 122
        '{',     # 123
        '|',     # 124
        '}',     # 125
        '~',     # 126
        
        # === Posiciones 127-190: ASCII extendido CP437 ===
        '⌂',     # 127 - DEL (casa)
        'Ç',     # 128
        'ü',     # 129
        'é',     # 130
        'â',     # 131
        'ä',     # 132
        'à',     # 133
        'å',     # 134
        'ç',     # 135
        'ê',     # 136
        'ë',     # 137
        'è',     # 138
        'ï',     # 139
        'î',     # 140
        'ì',     # 141
        'Ä',     # 142
        'Å',     # 143
        'É',     # 144
        'æ',     # 145
        'Æ',     # 146
        'ô',     # 147
        'ö',     # 148
        'ò',     # 149
        'û',     # 150
        'ù',     # 151
        'ÿ',     # 152
        'Ö',     # 153
        'Ü',     # 154
        '¢',     # 155
        '£',     # 156
        '¥',     # 157
        '₧',     # 158
        'ƒ',     # 159
        'á',     # 160
        'í',     # 161
        'ó',     # 162
        'ú',     # 163
        'ñ',     # 164
        'Ñ',     # 165
        'ª',     # 166
        'º',     # 167
        '¿',     # 168
        '⌐',     # 169
        '¬',     # 170
        '½',     # 171
        '¼',     # 172
        '¡',     # 173
        '«',     # 174
        '»',     # 175
        '░',     # 176
        '▒',     # 177
        '▓',     # 178
        '│',     # 179
        '┤',     # 180
        '╡',     # 181
        '╢',     # 182
        '╖',     # 183
        '╕',     # 184
        '╣',     # 185
        '║',     # 186
        '╗',     # 187
        '╝',     # 188
        '╜',     # 189
        '╛',     # 190
    )

class AlfabetoMod191:
    def __init__(self):
        self.caracteres = CARACTERES_CP437
        self.modulo = 191
        assert len(self.caracteres) == 191, f"ERROR: La tupla tiene {len(self.caracteres)} elementos, debe tener 191"
        self._indice = {}
        for idx, char in enumerate(self.caracteres):
            if char not in self._indice:
                self._indice[char] = idx

    def obtener_caracter(self, indice: int) -> str:
        return self.caracteres[indice % self.modulo]

    def obtener_indice(self, caracter: str) -> int:
        if caracter not in self._indice:
            raise KeyError(f"Carácter '{caracter}' no encontrado en el alfabeto.")
        return self._indice[caracter]

    def validar_texto(self, texto: str) -> list:
        return [c for c in texto if c not in self._indice]

    def __len__(self):
        return self.modulo

    def __getitem__(self, indice: int) -> str:
        return self.obtener_caracter(indice)

    def generar_diccionario_str(self) -> str:
        lineas = []
        for i in range(0, len(self.caracteres), 10):
            fila = []
            for j in range(i, min(i + 10, len(self.caracteres))):
                rep = repr(self.caracteres[j]) if self.caracteres[j].strip() == '' or len(self.caracteres[j]) != 1 else self.caracteres[j]
                fila.append(f"[{j:3d}] {rep}")
            lineas.append("  ".join(fila))
        return "\n\n".join(lineas)


class CifradoMod191:
    def __init__(self, alfabeto: AlfabetoMod191):
        self.alfabeto = alfabeto
        self.modulo = alfabeto.modulo

    def cifrar_cesar(self, texto_plano: str, clave: int) -> str:
        clave = clave % self.modulo
        resultado = []
        for caracter in texto_plano:
            indice = self.alfabeto.obtener_indice(caracter)
            nuevo_indice = (indice + clave) % self.modulo
            resultado.append(self.alfabeto[nuevo_indice])
        return ''.join(resultado)

    def descifrar_cesar(self, texto_cifrado: str, clave: int) -> str:
        clave = clave % self.modulo
        resultado = []
        for caracter in texto_cifrado:
            indice = self.alfabeto.obtener_indice(caracter)
            nuevo_indice = (indice - clave) % self.modulo
            resultado.append(self.alfabeto[nuevo_indice])
        return ''.join(resultado)

    def cifrar_cesar_pasos(self, texto_plano: str, clave: int) -> tuple:
        clave = clave % self.modulo
        resultado = []
        pasos = []
        for i, caracter in enumerate(texto_plano):
            idx = self.alfabeto.obtener_indice(caracter)
            nuevo = (idx + clave) % self.modulo
            res_char = self.alfabeto[nuevo]
            resultado.append(res_char)
            pasos.append({
                "paso": i + 1,
                "caracter_original": caracter,
                "indice_original": idx,
                "clave": clave,
                "operacion": f"({idx} + {clave}) mod {self.modulo}",
                "resultado_operacion": nuevo,
                "caracter_resultado": res_char
            })
        return ''.join(resultado), pasos

    def descifrar_cesar_pasos(self, texto_cifrado: str, clave: int) -> tuple:
        clave = clave % self.modulo
        resultado = []
        pasos = []
        for i, caracter in enumerate(texto_cifrado):
            idx = self.alfabeto.obtener_indice(caracter)
            nuevo = (idx - clave) % self.modulo
            res_char = self.alfabeto[nuevo]
            resultado.append(res_char)
            pasos.append({
                "paso": i + 1,
                "caracter_original": caracter,
                "indice_original": idx,
                "clave": clave,
                "operacion": f"({idx} - {clave}) mod {self.modulo}",
                "resultado_operacion": nuevo,
                "caracter_resultado": res_char
            })
        return ''.join(resultado), pasos

    def cifrar_vigenere(self, texto_plano: str, clave: str) -> str:
        if not clave:
            raise ValueError("La clave no puede estar vacía.")
        indices_clave = [self.alfabeto.obtener_indice(c) for c in clave]
        longitud_clave = len(indices_clave)
        resultado = []
        for i, caracter in enumerate(texto_plano):
            m_i = self.alfabeto.obtener_indice(caracter)
            k_i = indices_clave[i % longitud_clave]
            c_i = (m_i + k_i) % self.modulo
            resultado.append(self.alfabeto[c_i])
        return ''.join(resultado)

    def descifrar_vigenere(self, texto_cifrado: str, clave: str) -> str:
        if not clave:
            raise ValueError("La clave no puede estar vacía.")
        indices_clave = [self.alfabeto.obtener_indice(c) for c in clave]
        longitud_clave = len(indices_clave)
        resultado = []
        for i, caracter in enumerate(texto_cifrado):
            c_i = self.alfabeto.obtener_indice(caracter)
            k_i = indices_clave[i % longitud_clave]
            m_i = (c_i - k_i) % self.modulo
            resultado.append(self.alfabeto[m_i])
        return ''.join(resultado)

    def cifrar_vigenere_pasos(self, texto_plano: str, clave: str) -> tuple:
        if not clave:
            raise ValueError("La clave no puede estar vacía.")
        indices_clave = [self.alfabeto.obtener_indice(c) for c in clave]
        longitud_clave = len(indices_clave)
        resultado = []
        pasos = []
        for i, caracter in enumerate(texto_plano):
            m_i = self.alfabeto.obtener_indice(caracter)
            k_i = indices_clave[i % longitud_clave]
            c_i = (m_i + k_i) % self.modulo
            resultado.append(self.alfabeto[c_i])
            pasos.append({
                "paso": i + 1,
                "caracter_original": caracter,
                "indice_original": m_i,
                "clave_char": clave[i % longitud_clave],
                "clave_indice": k_i,
                "operacion": f"({m_i} + {k_i}) mod {self.modulo}",
                "resultado_operacion": c_i,
                "caracter_resultado": self.alfabeto[c_i]
            })
        return ''.join(resultado), pasos

    def descifrar_vigenere_pasos(self, texto_cifrado: str, clave: str) -> tuple:
        if not clave:
            raise ValueError("La clave no puede estar vacía.")
        indices_clave = [self.alfabeto.obtener_indice(c) for c in clave]
        longitud_clave = len(indices_clave)
        resultado = []
        pasos = []
        for i, caracter in enumerate(texto_cifrado):
            c_i = self.alfabeto.obtener_indice(caracter)
            k_i = indices_clave[i % longitud_clave]
            m_i = (c_i - k_i) % self.modulo
            resultado.append(self.alfabeto[m_i])
            pasos.append({
                "paso": i + 1,
                "caracter_original": caracter,
                "indice_original": c_i,
                "clave_char": clave[i % longitud_clave],
                "clave_indice": k_i,
                "operacion": f"({c_i} - {k_i}) mod {self.modulo}",
                "resultado_operacion": m_i,
                "caracter_resultado": self.alfabeto[m_i]
            })
        return ''.join(resultado), pasos