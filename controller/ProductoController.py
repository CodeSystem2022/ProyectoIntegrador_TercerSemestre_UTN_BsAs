from dao.ProductoDao import ProductoDao
from factory.ConnectionFactory import ConnectionFactory
from modelo.Producto import Producto


class ProductoController:
    def __init__(self):
        self.producto_dao = ProductoDao(ConnectionFactory.get_connection('ProductoController'))

    def guardar(self, producto: Producto):
        self.producto_dao.guardar(producto)

    def listar(self):
        self.producto_dao.listar()

    def actualizar(self, producto: Producto):
        self.producto_dao.actualizar(producto)

    def eliminar(self, producto: Producto):
        self.producto_dao.eliminar(producto)
