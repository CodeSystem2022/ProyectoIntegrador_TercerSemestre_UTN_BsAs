from dao.ProductoDao import ProductoDao
from factory.ConnectionFactory import ConnectionFactory
from modelo.Producto import Producto


# Controlador de la tabla Productos
# se encarga de comunicarse con la
# base de datos y enviar la acción a realizar

class ProductoController:
    def __init__(self):
        self.producto_dao = ProductoDao(ConnectionFactory().get_connection('ProductoController'))

    def guardar(self, producto: Producto):
        self.producto_dao.guardar(producto)

    def listar(self):
        return self.producto_dao.listar()

    def actualizar(self, producto: Producto):
        self.producto_dao.actualizar(producto)

    def eliminar(self, id_producto: str):
        return self.producto_dao.eliminar(id_producto)
