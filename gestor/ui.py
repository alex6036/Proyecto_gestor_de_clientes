# gestor/ui.py
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
from gestor import database as db
from gestor import helpers
from gestor import config
from gestor import controllers

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        self.geometry(f"{w}x{h}+{x}+{y}")

class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Crear cliente')
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Labels
        Label(frame, text=config.LABEL_TEXTS["DNI"]).grid(row=0, column=0)
        Label(frame, text=config.LABEL_TEXTS["NOMBRE"]).grid(row=0, column=1)
        Label(frame, text=config.LABEL_TEXTS["APELLIDO"]).grid(row=0, column=2)

        # Entries
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 2))

        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)

        # Buttons
        crear = Button(frame, text=config.BUTTON_TEXTS["CREATE"], command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text=config.BUTTON_TEXTS["CANCEL"], command=self.close).grid(row=0, column=1)

        # Class exports
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.validaciones = [0, 0, 0]  # False, False, False

    def validate(self, event, index):
        valor = event.widget.get()
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 else (
            valor.isalpha() and 2 <= len(valor) <= 30
        )
        event.widget.configure({"bg": "Green" if valido else "Red"})
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if all(self.validaciones) else DISABLED)

    def create_client(self):
        dni = self.dni.get()
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        controllers.ClienteController.crear(dni, nombre, apellido)
        self.master.refresh_treeview()
        self.close()

    def close(self):
        self.destroy()
        self.update()

class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Actualizar cliente')
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Labels
        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text=config.LABEL_TEXTS["NOMBRE"]).grid(row=0, column=1)
        Label(frame, text=config.LABEL_TEXTS["APELLIDO"]).grid(row=0, column=2)

        # Entries
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.config(state=DISABLED)

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))

        # Set entries initial values
        cliente = self.master.treeview.focus()
        if cliente:
            campos = self.master.treeview.item(cliente, 'values')
            dni.insert(0, campos[0])
            nombre.insert(0, campos[1])
            apellido.insert(0, campos[2])

        # Bottom frame
        frame = Frame(self)
        frame.pack(pady=10)

        # Buttons
        actualizar = Button(frame, text=config.BUTTON_TEXTS["UPDATE"], command=self.update_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text=config.BUTTON_TEXTS["CANCEL"], command=self.close).grid(row=0, column=1)

        # Update button activation
        self.validaciones = [1, 1]  # True, True
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def validate(self, event, index):
        valor = event.widget.get()
        valido = valor.isalpha() and 2 <= len(valor) <= 30
        event.widget.configure({"bg": "Green" if valido else "Red"})
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if all(self.validaciones) else DISABLED)

    def update_client(self):
        cliente = self.master.treeview.focus()
        if cliente:
            dni = self.dni.get()
            nombre = self.nombre.get()
            apellido = self.apellido.get()
            self.master.treeview.item(cliente, values=(dni, nombre, apellido))
            controllers.ClienteController.modificar(dni, nombre, apellido)
            self.close()

    def close(self):
        self.destroy()
        self.update()

class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.center()

    def build(self):
        # Top Frame (para el Treeview y la barra de desplazamiento)
        frame = Frame(self)
        frame.pack()

        # Treeview
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        treeview = ttk.Treeview(frame, yscrollcommand=scrollbar.set)
        treeview['columns'] = config.TREEVIEW_COLUMNS

        # Configuración de columnas
        treeview.column("#0", width=0, stretch=NO)
        for col in config.TREEVIEW_COLUMNS:
            treeview.column(col, anchor=CENTER)

        # Configuración de encabezados
        treeview.heading("#0", anchor=CENTER)
        for col in config.TREEVIEW_COLUMNS:
            treeview.heading(col, text=col, anchor=CENTER)

        # Cargar datos desde la base de datos
        self.refresh_treeview()

        treeview.pack()

        # Exportar treeview como atributo de clase
        self.treeview = treeview

        # Bottom Frame (para los botones)
        frame = Frame(self)
        frame.pack(pady=20)

        # Botones
        Button(frame, text=config.BUTTON_TEXTS["CREATE"], command=self.create_client_window).grid(row=1, column=0)
        Button(frame, text=config.BUTTON_TEXTS["MODIFY"], command=self.edit_client_window).grid(row=1, column=1)
        Button(frame, text=config.BUTTON_TEXTS["DELETE"], command=self.delete).grid(row=1, column=2)

    def create_client_window(self):
        CreateClientWindow(self)

    def edit_client_window(self):
        if self.treeview.focus():
            EditClientWindow(self)
        else:
            from tkinter.messagebox import showwarning
            showwarning("Advertencia", "Por favor, seleccione un cliente para modificar.")

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, 'values')
            confirmar = askokcancel(
                title='Confirmación',
                message=f'¿Borrar a {campos[1]} {campos[2]}?',
                icon=WARNING
            )
            if confirmar:
                self.treeview.delete(cliente)
                controllers.ClienteController.borrar(campos[0])

    def refresh_treeview(self):
        # Limpiar el Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        # Recargar los datos
        for cliente in db.Clientes.lista:
            self.treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )