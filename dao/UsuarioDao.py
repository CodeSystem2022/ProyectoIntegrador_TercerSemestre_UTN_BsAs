from factory.ConnectionFactory import ConnectionFactory
from modelo.Usuario import Usuario


class UsuarioDao:
    listado_usuarios: list = []

    # Al inicializar el DAO, se le pasa una conexión
    def __init__(self, con: ConnectionFactory):
        self.con = con

    # Inserta un Usuario a la base de datos
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
        # Se crea una lista para almacenar los usuarios
        usuarios: list = []

        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement: str = 'SELECT * FROM usuarios ORDER BY id_usuario'
                    # Se ejecuta la consulta
                    cursor.execute(prepared_statement)
                    # Se obtienen los registros de la consulta
                    registros = cursor.fetchall()

                    # Se verifica si hay registros
                    if registros:
                        # Se recorren los registros
                        for registro in registros:
                            # Se crea un objeto Usuario con los datos del registro
                            print(registro)
                            usuario = Usuario(
                                nombre=registro[1],
                                apellido=registro[2],
                                documento=registro[3],
                                porcentualcomision=registro[4],
                                comision=registro[5],
                                codigo=registro[0])
                            # Se agrega el usuario a la lista
                            usuarios.append(usuario)

                # Se retorna la lista de usuarios
                return usuarios

        except Exception as e:
            print(f'Ocurrió un error: {e}')

    # Elimina un usuario de la base de datos, recibiendo como parámetro el id del usuario
    def eliminar(self, id_usuario: str):
        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement = 'DELETE FROM usuarios WHERE id_usuario = %s'
                    # Se ejecuta la consulta, pasando como parámetro el id del usuario
                    cursor.execute(prepared_statement, (id_usuario,))
                    # Se obtiene la cantidad de registros eliminados
                    registros_eliminados = cursor.rowcount
                    return registros_eliminados
        # Se captura la excepción
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    # Actualiza un Usuario de la base de datos
    def actualizar(self, usuario: Usuario):
        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement = 'UPDATE usuarios SET nombre = %s, apellido = %s, documento = %s, porcentualcomision = %s, comision = %s ' \
                                         'WHERE id_usuario = %s'
                    # Se ejecuta la consulta, pasando como parámetro los datos del producto
                    cursor.execute(prepared_statement,
                                   (usuario.nombre, usuario.apellido, usuario.documento, usuario.porcentualcomision,
                                    usuario.comision, usuario.codigo))

                    # Se obtiene la cantidad de registros actualizados
                    registros_actualizados = cursor.rowcount
                    # Se imprime la cantidad de registros actualizados
                    print(f'Se actualizó satisfactoriamente {registros_actualizados} registro(s).')
        # Se captura la excepción
        except Exception as e:
            print(f'Ocurrió un error: {e}')
