# gestor/database.py
from gestor import config
import csv

class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"

class Clientes:
    # Lista de clientes
    lista = []

    @staticmethod
    def cargar():
        """Carga los datos desde el archivo CSV definido en config.DATABASE_PATH."""
        Clientes.lista = []  # Limpiar la lista antes de cargar
        try:
            with open(config.DATABASE_PATH, newline="\n") as fichero:
                reader = csv.reader(fichero, delimiter=";")
                for dni, nombre, apellido in reader:
                    cliente = Cliente(dni, nombre, apellido)
                    Clientes.lista.append(cliente)
        except FileNotFoundError:
            # Si el archivo no existe, empezar con una lista vacía
            Clientes.lista = []

    @staticmethod
    def guardar():
        """Guarda la lista de clientes en el archivo CSV."""
        with open(config.DATABASE_PATH, "w", newline="\n") as fichero:
            writer = csv.writer(fichero, delimiter=";")
            for c in Clientes.lista:
                writer.writerow((c.dni, c.nombre, c.apellido))

    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
        return None

    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente

    @staticmethod
    def modificar(dni, nombre, apellido):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[i].nombre = nombre
                Clientes.lista[i].apellido = apellido
                Clientes.guardar()
                return Clientes.lista[i]
        return None

    @staticmethod
    def borrar(dni):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(i)
                Clientes.guardar()
                return cliente
        return None

# Opcional: Cargar los datos al importar el módulo (solo si estás seguro de que el archivo existe)
# Clientes.cargar()