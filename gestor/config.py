#gestor/config.py
import sys
DATABASE_PATH = 'clientes.csv'

if 'pytest' in sys.argv[0]:
    DATABASE_PATH = 'tests/clientes_test.csv'


BUTTON_TEXTS = {
    "CREATE": "Crear",
    "MODIFY": "Modificar",
    "DELETE": "Borrar",
    "UPDATE": "Actualizar",
    "CANCEL": "Cancelar"
}

LABEL_TEXTS = {
    "DNI": "DNI (2 ints y 1 upper char)",
    "NOMBRE": "Nombre (2 a 30 chars)",
    "APELLIDO": "Apellido (2 a 30 chars)"
}

TREEVIEW_COLUMNS = ("DNI", "Nombre", "Apellido")