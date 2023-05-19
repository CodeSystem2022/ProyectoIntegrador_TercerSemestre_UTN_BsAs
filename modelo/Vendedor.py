from modelo.Persona import Persona


class Vendedor(Persona):
    # Lista para almacenar vendedores creados
    lista_vendedores: list = []

    def __init__(self, nombre, domicilio, codigo, comision, porcentual_comision):
        super().__init__(nombre, domicilio)
        self._codigo = codigo
        self._comision = comision
        self._porcentual = porcentual_comision
        Vendedor.lista_vendedores.append(self)

    def __str__(self):
        return f'Vendedor:\n' \
               f'{super().__str__()}\n' \
               f'\tCódigo: {self._codigo}\n ' \
               f'\tComisión total: {self._comision}\n' \
               f'\tPorcentual de Comisión actual: {self._porcentual * 100}'

    @classmethod
    def listar_vendedores(cls):
        print(f'Listando ({len(cls.lista_vendedores)}) vendedores...')
        for vendedor in cls.lista_vendedores:
            print(vendedor)

    def comisionar_venta(self, monto_venta):
        self._comision += monto_venta * self._porcentual

    @property
    def porcentual(self):
        return self._porcentual

    @porcentual.setter
    def porcentual(self, porcentaje):
        if 0 < porcentaje <= 1:
            self._porcentual = porcentaje
        else:
            print('ERROR! El valor debe estar expresado en decimales (Ej: 0.1 para 10%)')

    # TODO: Falta código para generar ventas, conectando la orden con el producto
    def generar_venta(self):
        pass


if __name__ == '__main__':
    vendedor1: Vendedor = Vendedor('Lucas', 'Francia 231', 1, 0, 0.10)
    print(vendedor1)
    vendedor1.comisionar_venta(1000)
    vendedor1.comisionar_venta(500)
    print(vendedor1)
    Vendedor.listar_vendedores()
