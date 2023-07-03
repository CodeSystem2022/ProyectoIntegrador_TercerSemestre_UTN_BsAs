from factory.ConnectionFactory import ConnectionFactory
from modelo.VentaItem import VentaItem


class VentaItemDao:

    def __init__(self, con: ConnectionFactory):
        self.con = con

    # Guardar un registro en la tabla ventas_items
    def guardar(self, venta_item: VentaItem):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO ventas_items (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)'
                    cursor.execute(prepared_statement,
                                   (venta_item.id_venta, venta_item.id_producto, venta_item.cantidad,
                                    venta_item.precio_unitario))
                    registros_insertados = cursor.rowcount
                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
                    print(venta_item)
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    # Guardar varios registros
    def guardar_varios(self, venta_items: list):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO ventas_items (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)'
                    cursor.executemany(prepared_statement, venta_items)
                    registros_insertados = cursor.rowcount

                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def listar(self):
        VentaItemDao.listado_ventas.clear()
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT * FROM ventas ORDER BY id_venta'
                    cursor.execute(prepared_statement)
                    registros = cursor.fetchall()
                    if registros:
                        for registro in registros:
                            VentaItemDao.listado_ventas.append(
                                VentaItem(marca=registro[1], modelo=registro[2], precio=registro[3], stock=registro[4],
                                          codigo=registro[0]))
                        for producto in VentaItemDao.listado_ventas:
                            print(
                                f'Producto: {producto.codigo} - {producto.entryNombre} - {producto.modelo} - ${producto.precio} - {producto.stock} unidades')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def eliminar(self, venta: VentaItem):
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
    def ultimaVenta(self) -> VentaItem:
        VentaItemDao.ultima_venta = None
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT max(id_venta) FROM ventas'
                    cursor.execute(prepared_statement)
                    registros = cursor.fetchone()
                    if registros[0]:
                        print(registros[0])
                    else:
                        print("No hay registros de ventas")
        except Exception as e:
            print(f'Ocurrió un error: {e}')

        return VentaItemDao.ultima_venta
