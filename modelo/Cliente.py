from modelo.Persona import Persona


class Cliente(Persona):
    # Lista para almacenar clientes creados
    lista_clientes: list = []

    def __init__(self, nombre, apellido, documento, email, descuento, codigo=0):
        super().__init__(nombre, apellido, documento)
        self._codigo = codigo
        self._email = email
        self._descuento = descuento
        Cliente.lista_clientes.append(self)

    def __str__(self):
        return f'Cliente:\n' \
               f'{super().__str__()} \n' \
               f'\tCódigo: {self._codigo} \n ' \
               f'\tEmail: {self._email} \n ' \
               f'\tDescuento: {self._descuento * 100}%'

    @classmethod
    def listar_clientes(cls):
        print(f'Listando ({len(cls.lista_clientes)}) clientes...')
        for cliente in cls.lista_clientes:
            print(cliente)

    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, descuento):
        if 0 < descuento <= 1:
            self._descuento = descuento
        else:
            print('ERROR! El valor debe estar expresado en decimales (Ej: 0.1 para 10%)')


if __name__ == '__main__':
    cliente1: Cliente = Cliente('Juan', 'Calle Falsa 123', 1, 0.15)
    cliente2: Cliente = Cliente('Maria', 'Charlone 456', 2, 0.10)
    # print(cliente1)
    # print(cliente2)
    Cliente.listar_clientes()
