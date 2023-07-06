from modelo.Producto import Producto
from modelo.Venta import Venta


class VentaItem:
    lista_ventas_items: list = []

    def __init__(self, cantidad, venta: Venta = None, producto: Producto = None, codigo=0, id_venta=0, id_producto=0, precio_unitario=0):
        self._codigo = codigo
        self._id_venta = venta.codigo if venta else id_venta
        self._id_producto = producto.codigo if producto else id_producto
        self._cantidad = cantidad
        self._precio_unitario = producto.precio if producto else precio_unitario
        self._producto = producto
        self._venta = venta
        self._id_usuario = venta.id_usuario if venta else None

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo

    @property
    def id_venta(self):
        return self._id_venta

    @id_venta.setter
    def id_venta(self, id_venta):
        self._id_venta = id_venta

    @property
    def id_producto(self):
        return self._id_producto

    @id_producto.setter
    def id_producto(self, id_producto):
        self._id_producto = id_producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        self._cantidad = cantidad

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, precio_unitario):
        self._precio_unitario = precio_unitario

    @property
    def producto(self):
        return self._producto

    @producto.setter
    def producto(self, producto):
        self._producto = producto

    @property
    def venta(self):
        return self._venta

    @venta.setter
    def venta(self, venta):
        self._venta = venta

    def __str__(self):
        return f'{self._id_venta},{self._id_producto} {self._cantidad} {self._precio_unitario}'
