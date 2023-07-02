from dao.VentaDao import VentaDao
from factory.ConnectionFactory import ConnectionFactory
from modelo.Venta import Venta


class VentaController:
    def __init__(self):
        self.venta_dao = VentaDao(ConnectionFactory.get_connection('VentaController'))

    def guardar(self, venta: Venta):
        self.venta_dao.guardar(venta)

    def listar(self):
        self.venta_dao.listar()

    def actualizar(self, venta: Venta):
        self.venta_dao.actualizar(venta)

    def eliminar(self, venta: Venta):
        self.venta_dao.eliminar(venta)
