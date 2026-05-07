"""
Punto de entrada principal del simulador de ataque Gauss-Jordan.

Ejecuta la aplicación instanciando los tres componentes MVC
y delegando el control al controlador.

Uso:
    python main.py
"""

from mvc.modelo import ModeloSimulador
from mvc.vista import VistaPrincipal
from mvc.controlador import Controlador


def main() -> None:
    """Inicializa y arranca la aplicación."""
    modelo = ModeloSimulador()
    vista = VistaPrincipal()
    controlador = Controlador(modelo, vista)
    controlador.iniciar()


if __name__ == "__main__":
    main()
