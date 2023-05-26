from factory.ConnectionFactory import ConnectionFactory
from modelo.Producto import Producto


class ProductoDao:
    listado_productos: list = []

    def __init__(self, con: ConnectionFactory):
        self.con = con

    @staticmethod
    def seleccionar_producto(codigo: int) -> Producto:
        for producto in ProductoDao.listado_productos:
            if producto.codigo == codigo:
                return producto

    def guardar(self, producto: Producto):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO producto (descripcion, precio, stock) VALUES (%s, %s, %s)'
                    cursor.execute(prepared_statement, (producto.descripcion, producto.precio, producto.stock))
                    registros_insertados = cursor.rowcount
                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
                    print(producto)
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def listar(self):
        ProductoDao.listado_productos.clear()
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement: str = 'SELECT * FROM producto ORDER BY id'
                    cursor.execute(prepared_statement)
                    registros = cursor.fetchall()
                    if registros:
                        for registro in registros:
                            ProductoDao.listado_productos.append(
                                Producto(registro[1], registro[2], registro[3], registro[0]))
                        for producto in ProductoDao.listado_productos:
                            print(
                                f'Producto: {producto.codigo} - {producto.descripcion} - ${producto.precio} - {producto.stock} unidades')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def eliminar(self, producto: Producto):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'DELETE FROM producto WHERE id = %s'
                    cursor.execute(prepared_statement, (producto.codigo,))
                    registros_eliminados = cursor.rowcount
                    print(f'Se eliminó satisfactoriamente {registros_eliminados} registro(s).')
        except Exception as e:
            print(f'Ocurrió un error: {e}')
