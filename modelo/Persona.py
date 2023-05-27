class Persona:
    def __init__(self, nombre, domicilio):
        self._nombre = nombre
        self._domicilio = domicilio

    def __str__(self):
        return f'\tNombre: {self._nombre} \n ' \
               f'\tDomicilio: {self._domicilio}'


if __name__ == '__main__':
    persona1 = Persona('Max', 'Chacabuco 222')
    print(persona1)
