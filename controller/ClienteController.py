from dao.ClienteDao import ClienteDao
from factory.ConnectionFactory import ConnectionFactory
from modelo.Cliente import Cliente


class ClienteController:
    def __init__(self):
        self.cliente_dao = ClienteDao(ConnectionFactory().get_connection('ClienteController'))

    def guardar(self, cliente: Cliente):
        self.cliente_dao.guardar(cliente)

    def listar(self):
        return self.cliente_dao.listar()

    def actualizar(self, cliente: Cliente):
        self.cliente_dao.actualizar(cliente)

    def eliminar(self, id_cliente: str):
        return self.cliente_dao.eliminar(id_cliente)

    def buscar_por_id(self, id_cliente: str):
        return self.cliente_dao.buscar_por_id(id_cliente)
