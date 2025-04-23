# Proyecto_gestor_de_clientes
https://github.com/alex6036/Proyecto_gestor_de_clientes.git

Solo funciona el entorno grafico utiliza el comando python3 gestor/run.py -t



# Proyecto Gestor de Clientes

Este proyecto es una aplicación para la gestión de clientes, que permite realizar operaciones como listar, buscar, añadir, modificar y eliminar clientes. La aplicación cuenta con dos interfaces: una interfaz gráfica basada en `Tkinter` y una interfaz de terminal.


### Archivos principales

- **`gestor/run.py`**: Script principal que inicia la aplicación en modo gráfico o terminal.
- **`gestor/ui.py`**: Implementa la interfaz gráfica utilizando `Tkinter`.
- **`gestor/menu.py`**: Implementa la interfaz de terminal.
- **`gestor/database.py`**: Contiene la lógica para gestionar los datos de los clientes.
- **`gestor/controllers.py`**: Controladores para manejar las operaciones de los clientes.
- **`gestor/config.py`**: Configuración general del proyecto.
- **`gestor/helpers.py`**: Funciones auxiliares de uso general.
- **`tests/`**: Contiene pruebas unitarias para validar la funcionalidad del proyecto.

## Requisitos

Asegúrate de tener instalado Python 3.10 o superior. Las dependencias necesarias están listadas en el archivo `requirements.txt`.

### Instalación de dependencias

Ejecuta el siguiente comando para instalar las dependencias:

```bash
pip install -r [requirements.txt](http://_vscodecontentref_/15)
python [run.py](http://_vscodecontentref_/16)
python [run.py](http://_vscodecontentref_/17) -t
python -m unittest discover tests