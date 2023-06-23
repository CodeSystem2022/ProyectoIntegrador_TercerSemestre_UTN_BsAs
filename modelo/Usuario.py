from modelo.Persona import Persona


class Usuario(Persona):
    # Lista para almacenar vendedores creados
    lista_usuarios: list = []

    @classmethod
    def listar_usuarios(cls):
        print(f'Listando ({len(cls.lista_usuarios)}) usuarios...')
        for usuario in cls.lista_usuarios:
            print(usuario)

    def __init__(self, apellido, nombre, documento, porcentualcomision, comision=0, codigo=0):
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
        if 0 < porcentaje <= 1:
            self._porcentualcomision = porcentaje
        else:
            print('ERROR! El valor debe estar expresado en decimales (Ej: 0.1 para 10%)')

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


if __name__ == '__main__':
    vendedor1: Usuario = Usuario('Lucas', 'Francia 231', 1, 0, 0.10)
    print(vendedor1)
    vendedor1.comisionar_venta(1000)
    vendedor1.comisionar_venta(500)
    print(vendedor1)
    Usuario.listar_usuarios()
