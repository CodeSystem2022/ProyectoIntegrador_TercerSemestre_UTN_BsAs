from modelo.Persona import Persona


class Usuario(Persona):
    # Lista para almacenar vendedores creados
    lista_usuarios: list = []

    def __init__(self, nombre, apellido, documento, porcentualcomision, comision=0, codigo=0):
        super().__init__(nombre, apellido, documento)
        self._codigo = codigo
        self._comision = comision
        self._porcentualcomision = porcentualcomision
        Usuario.lista_usuarios.append(self)

    @property
    def codigo(self):
        return self._codigo

    @property
    def comision(self):
        return self._comision

    @comision.setter
    def comision(self, comision):
        self._comision = comision

    @property
    def porcentualcomision(self):
        return self._porcentualcomision

    @porcentualcomision.setter
    def porcentualcomision(self, porcentaje):
        self._porcentualcomision = porcentaje

    def __str__(self):
        return f'Usuario:\n' \
               f'{super().__str__()}\n' \
               f'\tCódigo: {self._codigo}\n ' \
               f'\tComisión total: {self._comision}\n' \
               f'\tPorcentual de Comisión actual: {self._porcentualcomision * 100}'

    def comisionar_venta(self, monto_venta):
        self._comision += monto_venta * self._porcentualcomision

    # TODO: Falta código para generar ventas, conectando la orden con el producto
    def generar_venta(self):
        pass
