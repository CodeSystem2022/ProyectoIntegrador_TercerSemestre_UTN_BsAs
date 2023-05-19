from modelo.Persona import Persona


class Cliente(Persona):
    # Lista para almacenar clientes creados
    lista_clientes: list = []

    def __init__(self, nombre, domicilio, codigo, descuento):
        super().__init__(nombre, domicilio)
        self._codigo = codigo
        self._descuento = descuento
        Cliente.lista_clientes.append(self)

    def __str__(self):
        return f'Cliente:\n' \
               f'{super().__str__()} \n' \
               f'\tCódigo: {self._codigo} \n ' \
               f'\tDescuento: {self._descuento * 100}%'

    @classmethod
    def listar_clientes(cls):
        print(f'Listando ({len(cls.lista_clientes)}) clientes...')
        for cliente in cls.lista_clientes:
            print(cliente)


if __name__ == '__main__':
    cliente1: Cliente = Cliente('Juan', 'Calle Falsa 123', 1, 0.15)
    cliente2: Cliente = Cliente('Maria', 'Charlone 456', 2, 0.10)
    # print(cliente1)
    # print(cliente2)
    Cliente.listar_clientes()
