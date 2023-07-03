from factory.ConnectionFactory import ConnectionFactory
from modelo.Venta import Venta


class VentaDao:
    listado_ventas: list = []
    ultima_venta: Venta = None

    def __init__(self, con: ConnectionFactory):
        self.con = con

    def guardar(self, venta: Venta):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO ventas (fecha_alta, id_cliente, id_usuario, importe,comision,descuento) VALUES (%s, %s, %s, %s, %s, %s)'
                    cursor.execute(prepared_statement,
                                   (venta.fecha_alta, venta.id_cliente, venta.id_usuario, venta.importe, venta.comision,
                                    venta.descuento))
                    registros_insertados = cursor.rowcount
                    print(registros_insertados)
                    # return venta
                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
                    print(venta)
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def listar(self):
        VentaDao.listado_ventas.clear()
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT * FROM ventas ORDER BY id_venta'
                    cursor.execute(prepared_statement)
                    registros = cursor.fetchall()
                    if registros:
                        for registro in registros:
                            VentaDao.listado_ventas.append(
                                Venta(marca=registro[1], modelo=registro[2], precio=registro[3], stock=registro[4],
                                      codigo=registro[0]))
                        for producto in VentaDao.listado_ventas:
                            print(
                                f'Producto: {producto.codigo} - {producto.entryNombre} - {producto.modelo} - ${producto.precio} - {producto.stock} unidades')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def eliminar(self, venta: Venta):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'DELETE FROM ventas WHERE id_venta = %s'
                    cursor.execute(prepared_statement, (venta.codigo,))
                    registros_eliminados = cursor.rowcount
                    print(f'Se eliminó satisfactoriamente {registros_eliminados} registro(s).')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    # Devuelve el último id ingresado
    def id_ultima_venta(self) -> Venta:
        VentaDao.ultima_venta = None
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT max(id_venta) FROM ventas'
                    cursor.execute(prepared_statement)
                    registro = cursor.fetchone()
                    if registro:
                        return registro[0]
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def actualizar(self, venta: Venta):
        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement = 'UPDATE ventas SET ' \
                                         'importe = %s, ' \
                                         'comision = %s, ' \
                                         'descuento = %s ' \
                                         'WHERE id_venta = %s'
                    # Se ejecuta la consulta, pasando como parámetro los datos del producto
                    cursor.execute(prepared_statement,
                                   (venta.importe, venta.comision, venta.descuento, venta.codigo))
                    # Se obtiene la cantidad de registros actualizados
                    registros_actualizados = cursor.rowcount
                    # Se imprime la cantidad de registros actualizados
                    print(f'Se actualizó satisfactoriamente {registros_actualizados} registro(s).')
        # Se captura la excepción
        except Exception as e:
            print(f'Ocurrió un error: {e}')
