from factory.ConnectionFactory import ConnectionFactory
from modelo.Cliente import Cliente


class ClienteDao:
    listado_clientes: list = []

    def __init__(self, con: ConnectionFactory):
        self.con = con

    @staticmethod
    def seleccionar_cliente(codigo: int) -> Cliente:
        for cliente in ClienteDao.listado_clientes:
            if cliente.codigo == codigo:
                return cliente

    def guardar(self, cliente: Cliente):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO clientes (apellido, nombre, documento, email, descuento) VALUES (%s, %s, %s, %s, %s)'
                    cursor.execute(prepared_statement,
                                   (cliente.apellido, cliente.nombre, cliente.documento, cliente.email,
                                    cliente.descuento))
                    registros_insertados = cursor.rowcount
                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
                    print(cliente)
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def listar(self):
        ClienteDao.listado_clientes.clear()
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT * FROM clientes ORDER BY id_cliente'
                    cursor.execute(prepared_statement)
                    registros = cursor.fetchall()
                    if registros:
                        for registro in registros:
                            ClienteDao.listado_clientes.append(
                                Cliente(apellido=registro[1], nombre=registro[2], documento=registro[3],
                                        email=registro[4], descuento=registro[5],
                                        codigo=registro[0]))
                        for cliente in ClienteDao.listado_clientes:
                            print(
                                f'Cliente: {cliente.codigo} - {cliente.nombre} - {cliente.apellido} - {cliente.documento} - {cliente.email} - %{cliente.descuento}')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def eliminar(self, cliente: Cliente):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'DELETE FROM clientes WHERE id_cliente = %s'
                    cursor.execute(prepared_statement, (cliente.codigo,))
                    registros_eliminados = cursor.rowcount
                    print(f'Se eliminó satisfactoriamente {registros_eliminados} registro(s).')
        except Exception as e:
            print(f'Ocurrió un error: {e}')
