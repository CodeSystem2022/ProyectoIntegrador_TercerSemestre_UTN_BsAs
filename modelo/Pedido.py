from modelo.Cliente import Cliente
from modelo.Producto import Producto
from modelo.Usuario import Usuario


class Pedido:
    lista_pedidos: list = []
    contador_pedidos: int = 0

    def __init__(self, vendedor: Usuario, cliente: Cliente):
        Pedido.contador_pedidos += 1
        self._codigo = Pedido.contador_pedidos
        self._vendedor = vendedor
        self._cliente = cliente
        self._productos: dict = {}
        Pedido.lista_pedidos.append(self)

    def agregar_producto(self, producto: Producto, cantidad: int):
        if producto.stock < cantidad:
            print(f'No hay stock suficiente de {producto.marca}')
            return

        # print(self._productos)
        # print(producto)
        # print(cantidad)
        if producto not in self._productos:
            self._productos[producto] = cantidad
        else:
            self._productos[producto] += cantidad
        producto.stock -= cantidad
        print(f'Se agregaron {cantidad} unidades de {producto.marca} al pedido No {self._codigo}')

    def confirmar_venta(self):
        total: float = 0
        for producto, cantidad in self._productos.items():
            total += producto.precio * cantidad
        total *= (1 - self._cliente.descuento)
        self._vendedor.comisionar_venta(total)
        print(f'Venta confirmada por ${total}')

    def listar_productos(self):
        print(f'Listando ({len(self._productos)}) productos en Pedido No {self._codigo}...')
        for producto, cantidad in self._productos.items():
            print(f'{producto.marca} x {cantidad}')

    def __str__(self):
        return f'Pedido:\n' \
               f'\tCódigo: {self._codigo}\n' \
               f'\t{self._vendedor}\n' \
               f'\tCliente: {self._cliente}\n' \
               f'\tProductos: {self.listar_productos()}\n'


if __name__ == '__main__':
    producto1: Producto = Producto(1, 'Botella Coca Cola 2 Lts', 350, 50)
    producto2: Producto = Producto(2, 'Botella Pepsi 2 Lts', 300, 50)

    cliente1: Cliente = Cliente('Juan', 'Calle Falsa 123', 1, 0.15)
    cliente2: Cliente = Cliente('Maria', 'Charlone 456', 2, 0.10)

    vendedor1: Usuario = Usuario('Lucas', 'Francia 231', 1, 0, 0.10)

    pedido1: Pedido = Pedido(vendedor1, cliente1)
    pedido1.agregar_producto(producto1, 2)
    pedido1.agregar_producto(producto1, 4)
    pedido1.agregar_producto(producto2, 10)

    # pedido1.listar_productos()
    pedido1.confirmar_venta()
    pedido1.listar_productos()
    print(producto1)
    print(producto2)
    print(vendedor1)
