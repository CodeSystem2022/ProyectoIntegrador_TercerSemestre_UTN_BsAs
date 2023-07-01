from factory.ConnectionFactory import ConnectionFactory
from modelo.Cliente import Cliente


class ClienteDao:
    listado_clientes: list = []

    def __init__(self, con: ConnectionFactory):
        self.con = con

    def guardar(self, cliente: Cliente):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO clientes (nombre, apellido, documento, email, descuento) VALUES (%s, %s, %s, %s, %s)'
                    cursor.execute(prepared_statement,
                                   (cliente.nombre, cliente.apellido, cliente.documento, cliente.email,
                                    cliente.descuento))
                    registros_insertados = cursor.rowcount
                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
                    print(cliente)
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def listar(self):
        clientes: list = []
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT * FROM clientes ORDER BY id_cliente'
                    cursor.execute(prepared_statement)
                    registros = cursor.fetchall()
                    if registros:
                        for registro in registros:
                            cliente = Cliente(nombre=registro[1], apellido=registro[2], documento=registro[3],
                                              email=registro[4], descuento=registro[5], codigo=registro[0])
                            clientes.append(cliente)

                    return clientes

        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def eliminar(self, id_cliente: str):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'DELETE FROM clientes WHERE id_cliente = %s'
                    cursor.execute(prepared_statement, (id_cliente,))
                    registros_eliminados = cursor.rowcount
                    return registros_eliminados
                    # print(f'Se eliminó satisfactoriamente {registros_eliminados} registro(s).')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def actualizar(self, cliente: Cliente):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'UPDATE clientes SET nombre = %s, apellido = %s, documento = %s, email = %s, descuento = %s WHERE id_cliente = %s'
                    cursor.execute(prepared_statement, (
                        cliente.nombre, cliente.apellido, cliente.documento, cliente.email, cliente.descuento,
                        cliente.codigo))
                    registros_actualizados = cursor.rowcount
                    print(f'Se actualizó satisfactoriamente {registros_actualizados} registro(s).')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def buscar_por_id(self, id_cliente):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'SELECT * FROM clientes WHERE id_cliente = %s'
                    cursor.execute(prepared_statement, (id_cliente,))
                    registro = cursor.fetchone()
                    if registro:
                        cliente = Cliente(nombre=registro[1], apellido=registro[2], documento=registro[3],
                                          email=registro[4], descuento=registro[5], codigo=registro[0])
                        return cliente
        except Exception as e:
            print(f'Ocurrió un error: {e}')
