from dao.VentaItemDao import VentaItemDao
from factory.ConnectionFactory import ConnectionFactory
from modelo.VentaItem import VentaItem


class VentaItemController:
    def __init__(self):
        self.venta_item_dao = VentaItemDao(ConnectionFactory().get_connection('VentaItemController'))

    def guardar(self, venta_item: VentaItem):
        return self.venta_item_dao.guardar(venta_item)

    def guardar_varios(self, lista_venta_item: list):
        return self.venta_item_dao.guardar_varios(lista_venta_item)

    def listar(self):
        self.venta_item_dao.listar()

    def actualizar(self, venta_item: VentaItem):
        self.venta_item_dao.actualizar(venta_item)

    def eliminar(self, venta_item: VentaItem):
        self.venta_item_dao.eliminar(venta_item)

    def buscar_por_id_venta(self, id_venta: str):
        return self.venta_item_dao.buscar_por_id_venta(id_venta)
