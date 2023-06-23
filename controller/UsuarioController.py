from dao.UsuarioDao import UsuarioDao
from factory.ConnectionFactory import ConnectionFactory
from modelo.Usuario import Usuario


class UsuarioController:
    def __init__(self):
        self.usuario_dao = UsuarioDao(ConnectionFactory.get_connection('UsuarioController'))

    def guardar(self, usuario: Usuario):
        self.usuario_dao.guardar(usuario)

    def listar(self):
        self.usuario_dao.listar()

    def actualizar(self, usuario: Usuario):
        self.usuario_dao.actualizar(usuario)

    def eliminar(self, usuario: Usuario):
        self.usuario_dao.eliminar(usuario)
