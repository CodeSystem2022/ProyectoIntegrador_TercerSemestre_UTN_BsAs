from factory.ConnectionFactory import ConnectionFactory
from modelo.Venta import Venta


class VentaDao:
    listado_ventas: list = []

    def __init__(self, con: ConnectionFactory):
        self.con = con

    @staticmethod
    def seleccionar_venta(codigo: int) -> Venta:
        for venta in VentaDao.listado_ventas:
            if venta.codigo == codigo:
                return venta

    def guardar(self, venta: Venta):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO ventas (fecha_alta, id_cliente, id_usuario, importe,comision,descuento) VALUES (%s, %s, %s, %s, %s, %s)'
                    cursor.execute(prepared_statement,
                                   (venta.fecha_alta, venta.id_cliente, venta.id_usuario, venta.importe, venta.comision,
                                    venta.descuento))
                    registros_insertados = cursor.rowcount
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
                                f'Producto: {producto.codigo} - {producto.marca} - {producto.modelo} - ${producto.precio} - {producto.stock} unidades')
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
