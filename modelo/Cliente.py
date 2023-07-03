from modelo.Persona import Persona


class Cliente(Persona):
    # Lista para almacenar clientes creados
    lista_clientes: list = []

    @classmethod
    def listar_clientes(cls):
        print(f'Listando ({len(cls.lista_clientes)}) clientes...')
        for cliente in cls.lista_clientes:
            print(cliente)

    def __init__(self, nombre, apellido, documento, email, descuento, codigo=0):
        super().__init__(nombre, apellido, documento)
        self._codigo = codigo
        self._email = email
        self._descuento = descuento
        Cliente.lista_clientes.append(self)

    @property
    def codigo(self):
        return self._codigo

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, descuento):
        self._descuento = descuento

    def __str__(self):
        return f'Cliente:\n' \
               f'{super().__str__()} \n' \
               f'\tCódigo: {self._codigo} \n ' \
               f'\tEmail: {self._email} \n ' \
               f'\tDescuento: {self._descuento * 100}%'
