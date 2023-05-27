from modelo.Persona import Persona
from modelo.Vendedor import Vendedor


class Gerente(Persona):
    # Lista para almacenar vendedores creados
    lista_gerentes: list = []

    def __init__(self, nombre, domicilio, codigo):
        super().__init__(nombre, domicilio)
        self._codigo = codigo
        Gerente.lista_gerentes.append(self)

    def __str__(self):
        return f'Gerente:\n' \
               f'{super().__str__()}\n' \
               f'\tCódigo: {self._codigo}\n '

    @classmethod
    def listar_gerentes(cls):
        print(f'Listando ({len(cls.lista_gerentes)}) gerentes...')
        for gerentes in cls.lista_gerentes:
            print(gerentes)

    @staticmethod
    def cambiar_porcentual(vendedor: Vendedor, porcentual: float):
        vendedor.porcentual = porcentual


if __name__ == '__main__':
    gerente1: Gerente = Gerente('Martin', 'Laspiur 123', 1)
    vendedor5: Vendedor = Vendedor('Lucas', 'Francia 231', 1, 0, 0.10)
    print(gerente1)
    print(vendedor5)
    gerente1.cambiar_porcentual(vendedor5, 0.3)
    print(vendedor5)
