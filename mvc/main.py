import sys
import os

# Añadir el directorio raíz al path para que el paquete 'mvc' sea visible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mvc.view.vista import Vista
from mvc.controllers.controlador import Controlador

if __name__ == "__main__":
    app = Vista()
    controlador = Controlador(app)
    app.set_controlador(controlador)
    # Inicializar con tamaño por defecto
    app.crear_cuadricula_entrada(2)
    app.mainloop()