from modelo.Producto import Producto
from modelo.Venta import Venta


class VentaItem:
    lista_ventas_items: list = []

    def __init__(self, venta: Venta, producto: Producto, cantidad, codigo=0):
        self._codigo = codigo
        self._id_venta = venta.codigo
        self._id_producto = producto.codigo
        self._cantidad = cantidad
        self._precio_unitario = producto.precio

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

    def __str__(self):
        return f'{self._codigo} {self._id_venta} {self._id_producto} {self._cantidad} {self._precio_unitario}'
