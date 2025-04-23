# gestor/controllers.py
from tkinter import messagebox
from . import database as db

class ClienteController:
    @staticmethod
    def crear(dni, nombre, apellido):
        try:
            db.Clientes.crear(dni, nombre, apellido)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def modificar(dni, nombre, apellido):
        try:
            cliente = db.Clientes.modificar(dni, nombre, apellido)
            if cliente is None:
                messagebox.showerror("Error", f"No se encontró un cliente con DNI {dni}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def borrar(dni):
        try:
            cliente = db.Clientes.borrar(dni)
            if cliente is None:
                messagebox.showerror("Error", f"No se encontró un cliente con DNI {dni}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))