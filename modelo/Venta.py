from datetime import datetime

from modelo.Cliente import Cliente
from modelo.Producto import Producto
from modelo.Usuario import Usuario


class Venta:
    lista_ventas: list = []

    def __init__(self, usuario: Usuario, cliente: Cliente, codigo=0, importe=0, comision=0, descuento=0):
        self._codigo = codigo
        self._fecha_alta = datetime.now()
        self._usuario = usuario
        self._cliente = cliente
        self._importe = importe
        self._comision = comision
        self._descuento = descuento
        self._productos: dict = {}
        Venta.lista_ventas.append(self)

    @property
    def codigo(self):
        return self._codigo

    @property
    def fecha_alta(self):
        return self._fecha_alta

    @fecha_alta.setter
    def fecha_alta(self, fecha_alta):
        self._fecha_alta = fecha_alta

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, usuario):
        self._usuario = usuario

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, cliente):
        self._cliente = cliente

    @property
    def importe(self):
        return self._importe

    @importe.setter
    def importe(self, importe):
        self._importe = importe

    @property
    def comision(self):
        return self._comision

    @comision.setter
    def comision(self, comision):
        self._comision = comision

    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, descuento):
        self._descuento = descuento

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
        self._usuario.comisionar_venta(total)
        print(f'Venta confirmada por ${total}')

    def listar_productos(self):
        print(f'Listando ({len(self._productos)}) productos en Pedido No {self._codigo}...')
        for producto, cantidad in self._productos.items():
            print(f'{producto.entryMarca} x {cantidad}')

    def __str__(self):
        return f'Pedido:\n' \
               f'\tCódigo: {self._codigo}\n' \
               f'\t{self._usuario}\n' \
               f'\tCliente: {self._cliente}\n' \
               f'\tProductos: {self.listar_productos()}\n'
