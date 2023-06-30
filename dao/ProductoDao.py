from factory.ConnectionFactory import ConnectionFactory
from modelo.Producto import Producto


# El modelado DAO realiza la logica sobre las acciones de
# # CRUD (Create, Read, Update, Delete) en la base de datos


class ProductoDao:

    # Al inicializar el DAO, se le pasa una conexión
    def __init__(self, con: ConnectionFactory):
        self.con = con

    # Inserta un Producto a la base de datos
    # Funcional OK
    def guardar(self, producto: Producto):
        try:
            with self.con as conexion:
                with conexion.cursor() as cursor:
                    prepared_statement = 'INSERT INTO productos (marca, modelo, precio, stock) VALUES (%s, %s, %s, %s)'
                    cursor.execute(prepared_statement,
                                   (producto.marca, producto.modelo, producto.precio, producto.stock))
                    registros_insertados = cursor.rowcount
                    print(f'Se ingresó satisfactoriamente {registros_insertados} registro(s).')
                    # print(producto)
        # except psycopg2.errors.InvalidTextRepresentation as e:
        #     messagebox.showwarning("Error", "Ocurrio un error al intentar guardar el producto\n"
        #                                     " El formato de los datos ingresados no es correcto")
        #     print(f'Ocurrió un error: {e}')
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    # Devuelve una lista de productos, la cual obtiene de la base de datos
    # Funcional OK
    def listar(self) -> list:
        # Se crea la lista para almacenar los productos
        productos: list = []

        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement: str = 'SELECT * FROM productos ORDER BY id_producto'
                    # Se ejecuta la consulta
                    cursor.execute(prepared_statement)
                    # Se obtienen los registros de la consulta
                    registros = cursor.fetchall()

                    # Se verifica si hay registros
                    if registros:
                        # Se recorren los registros
                        for registro in registros:
                            # Se crea un objeto Producto con los datos del registro
                            producto = Producto(marca=registro[1],
                                                modelo=registro[2],
                                                precio=registro[3],
                                                stock=registro[4],
                                                codigo=registro[0])
                            # Se agrega el producto a la lista
                            productos.append(producto)

                # Se retorna la lista de productos
                return productos

        # Se captura la excepción
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    # Elimina un Producto de la base de datos, recibe como parámetro el id del producto desde el view
    # Funcional OK

    def eliminar(self, id_producto: str):
        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement = 'DELETE FROM productos WHERE id_producto = %s'
                    # Se ejecuta la consulta, pasando como parámetro el id del producto
                    cursor.execute(prepared_statement, (id_producto,))
                    # Se obtiene la cantidad de registros eliminados
                    registros_eliminados = cursor.rowcount
                    # Se imprime la cantidad de registros eliminados
                    # print(f'Se eliminó satisfactoriamente {registros_eliminados} registro(s).')
                    return registros_eliminados
        # Se captura la excepción
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    # Actualiza un Producto de la base de datos
    def actualizar(self, producto: Producto):
        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement = 'UPDATE productos SET marca = %s, modelo = %s, precio = %s, stock = %s ' \
                                         'WHERE id_producto = %s'
                    # Se ejecuta la consulta, pasando como parámetro los datos del producto
                    cursor.execute(prepared_statement,
                                   (producto.marca, producto.modelo, producto.precio, producto.stock,
                                    producto.codigo))
                    # Se obtiene la cantidad de registros actualizados
                    registros_actualizados = cursor.rowcount
                    # Se imprime la cantidad de registros actualizados
                    print(f'Se actualizó satisfactoriamente {registros_actualizados} registro(s).')
        # Se captura la excepción
        except Exception as e:
            print(f'Ocurrió un error: {e}')

    def buscar_por_id(self, codigo_producto: str):
        # Se crea un bloque try-except para manejar errores
        try:
            # Se crea un bloque with para manejar la conexión
            with self.con as conexion:
                # Se crea un bloque with para manejar el cursor
                with conexion.cursor() as cursor:
                    # Se crea un prepared statement con la consulta sql a ejecutar
                    prepared_statement = 'SELECT * FROM productos WHERE id_producto = %s'
                    # Se ejecuta la consulta, pasando como parámetro el id del producto
                    cursor.execute(prepared_statement, (codigo_producto,))
                    # Se obtiene el registro de la consulta
                    registro = cursor.fetchone()

                    # Se verifica si hay registros
                    if registro:
                        # Se crea un objeto Producto con los datos del registro
                        producto = Producto(marca=registro[1],
                                            modelo=registro[2],
                                            precio=registro[3],
                                            stock=registro[4],
                                            codigo=registro[0])
                        # Se retorna el producto
                        return producto

        # Se captura la excepción
        except Exception as e:
            print(f'Ocurrió un error: {e}')
