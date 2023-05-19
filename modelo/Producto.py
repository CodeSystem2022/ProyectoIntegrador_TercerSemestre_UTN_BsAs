class Producto:
    # Almacenamos objetos tipo Producto en una lista
    lista_productos = []

    def __init__(self, codigo, descripcion, precio, stock):
        self._codigo = codigo
        self._descripcion = descripcion
        self._precio = precio
        self._stock = stock
        # Agregamos el objeto a la lista de productos
        Producto.lista_productos.append(self)

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self._descripcion = descripcion

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, precio):
        self._precio = precio

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, stock):
        self._stock = stock

    def __str__(self):
        return f'Producto:\n' \
               f'\tCódigo: {self._codigo} \n' \
               f'\tDescripción: {self._descripcion}\n' \
               f'\tPrecio: ${self._precio}\n' \
               f'\tStock: {self._stock} unidades\n'

    @classmethod
    def listar_productos(cls):
        print(f'Listando ({len(cls.lista_productos)}) productos...')
        for producto in cls.lista_productos:
            print(producto)


if __name__ == '__main__':
    producto1: Producto = Producto(1, 'Botella Coca Cola 2 Lts', 350, 50)
    producto2: Producto = Producto(2, 'Botella Pepsi 2 Lts', 300, 50)

    # print(producto1)
    # print(producto2)

    Producto.listar_productos()
