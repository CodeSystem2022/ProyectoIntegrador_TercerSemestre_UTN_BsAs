from factory.ConnectionFactory import ConnectionFactory
from modelo.VentaItem import VentaItem


class VentaItemDao:

    def __init__(self, con: ConnectionFactory):
        self.con = con

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


    def buscar_por_id_venta(self, id_venta):
        listado_items: list = []
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT * FROM ventas_items WHERE id_venta = %s'
                    cursor.execute(prepared_statement, (id_venta,))
                    registros = cursor.fetchall()
                    for registro in registros:
                        item = VentaItem(codigo=registro[0], id_venta=registro[1], id_producto=registro[2], cantidad=registro[3], precio_unitario=registro[4])
                        listado_items.append(item)
                    return listado_items

        except Exception as e:
            print(f'Ocurrió un error: {e}')
