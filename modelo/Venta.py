from datetime import datetime

from modelo.Cliente import Cliente
from modelo.Usuario import Usuario


class Venta:
    lista_ventas: list = []

    def __init__(self, usuario: Usuario, cliente: Cliente, codigo=0, importe=0):
        self._codigo = codigo
        self._fecha_alta = datetime.now()
        self._id_usuario = usuario.codigo
        self._id_cliente = cliente.codigo
        self._importe = importe
        self._comision = usuario.comision
        self._descuento = cliente.descuento
        Venta.lista_ventas.append(self)

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo

    @property
    def fecha_alta(self):
        return self._fecha_alta

    @fecha_alta.setter
    def fecha_alta(self, fecha_alta):
        self._fecha_alta = fecha_alta

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self._id_usuario = id_usuario

    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, id_cliente):
        self._id_cliente = id_cliente

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

    def agregar_producto(self, producto: Usuario, cantidad: int):
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
        total *= (1 - self._id_cliente.descuento)
        self._id_usuario.comisionar_venta(total)
        print(f'Venta confirmada por ${total}')

    def listar_productos(self):
        print(f'Listando ({len(self._productos)}) productos en Pedido No {self._codigo}...')
        for producto, cantidad in self._productos.items():
            print(f'{producto.entryNombre} x {cantidad}')

    def __str__(self):
        return f'Venta: {self._codigo} - {self._fecha_alta} - Cliente: {self._id_cliente} - Usuario: {self._id_usuario} - Importe: ${self._importe} - Comisión: {self._comision} - Descuento: {self._descuento}'
