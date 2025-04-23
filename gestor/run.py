'# El script principal que lo pondrá todo en marcha'
# gestor/run.py
import sys
import os

# Agregar el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gestor import menu
from gestor import ui
from gestor import database as db

if __name__ == "__main__":
    # Cargar los datos antes de iniciar
    db.Clientes.cargar()
    
    # Si pasamos un argumento -t, lanzamos el modo terminal
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.iniciar()
    # En cualquier otro caso, lanzamos el modo gráfico
    else:
        app = ui.MainWindow()
        app.mainloop()