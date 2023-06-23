from factory.ConnectionFactory import ConnectionFactory
from modelo.Usuario import Usuario


class UsuarioDao:
    listado_usuarios: list = []

    def __init__(self, con: ConnectionFactory):
        self.con = con

    @staticmethod
    def seleccionar_usuario(codigo: int) -> Usuario:
        for usuario in UsuarioDao.listado_usuarios:
            if usuario.codigo == codigo:
                return usuario

    def guardar(self, usuario: Usuario):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO usuarios (apellido, nombre, documento, porcentualcomision, comision) VALUES (%s, %s, %s, %s, %s)'
                    cursor.execute(prepared_statement,
                                   (usuario.apellido, usuario.nombre, usuario.documento, usuario.porcentualcomision,
                                    usuario.comision))
                    registros_insertados = cursor.rowcount
                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
                    print(usuario)
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def listar(self):
        UsuarioDao.listado_usuarios.clear()
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT * FROM usuarios ORDER BY id_usuario'
                    cursor.execute(prepared_statement)
                    registros = cursor.fetchall()
                    if registros:
                        for registro in registros:
                            UsuarioDao.listado_usuarios.append(
                                Usuario(apellido=registro[1], nombre=registro[2], documento=registro[3],
                                        porcentualcomision=registro[4], comision=registro[5],
                                        codigo=registro[0]))
                        for usuario in UsuarioDao.listado_usuarios:
                            print(
                                f'Usuario: {usuario.codigo} - {usuario.nombre} - {usuario.apellido} - {usuario.documento} - %{usuario.porcentualcomision} - ${usuario.comision}')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def eliminar(self, usuario: Usuario):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'DELETE FROM usuarios WHERE id = %s'
                    cursor.execute(prepared_statement, (usuario.codigo,))
                    registros_eliminados = cursor.rowcount
                    print(f'Se eliminó satisfactoriamente {registros_eliminados} registro(s).')
        except Exception as e:
            print(f'Ocurrió un error: {e}')
