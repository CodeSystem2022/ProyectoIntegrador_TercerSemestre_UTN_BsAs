class Producto:
    # Almacenamos objetos tipo Producto en una lista
    lista_productos = []

    def __init__(self, marca, modelo, precio, stock, codigo=0):
        self._codigo = codigo
        self._marca = marca
        self._modelo = modelo
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
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, marca):
        self._marca = marca

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, modelo):
        self._modelo = modelo

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
        return '{} -> {} {} [ ${} ]'.format(self._codigo, self._marca, self._modelo, self._precio)
