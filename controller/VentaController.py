from dao.VentaDao import VentaDao
from factory.ConnectionFactory import ConnectionFactory
from modelo.Venta import Venta


class VentaController:
    def __init__(self):
        self.venta_dao = VentaDao(ConnectionFactory().get_connection('VentaController'))

    def guardar(self, venta: Venta):
        return self.venta_dao.guardar(venta)

    def listar(self):
        return self.venta_dao.listar()

    def actualizar(self, venta: Venta):
        self.venta_dao.actualizar(venta)

    def eliminar(self, venta: Venta):
        self.venta_dao.eliminar(venta)

    def buscar_por_id(self, id_venta: str):
        return self.venta_dao.buscar_por_id(id_venta)

    # Devuelve la ultima venta realizada, para obtener el ID
    def id_ultima_venta(self):
        return self.venta_dao.id_ultima_venta()
