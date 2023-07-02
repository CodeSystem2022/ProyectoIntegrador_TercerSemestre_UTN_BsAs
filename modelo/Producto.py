

class Producto:
    
    lista_productos = []

    def __init__(self, marca, modelo, precio, stock, codigo=0):
        self._codigo = codigo
        self._marca = marca
        self._modelo = modelo
        self._precio = precio
        self._stock = stock
       
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
        return f'Producto:\n' \
               f'\tCódigo: {self._codigo} \n' \
               f'\tMarca: {self._marca}\n' \
               f'\tModelo: {self._modelo}\n' \
               f'\tPrecio: ${self._precio}\n' \
               f'\tStock: {self._stock} unidades\n'

    @classmethod
    def listar_productos(cls):
        print(f'Listando ({len(cls.lista_productos)}) productos...')
        for producto in cls.lista_productos:
            print(producto)


if __name__ == '__main__':
    
    Producto.listar_productos()
