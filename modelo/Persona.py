class Persona:
    def __init__(self, nombre, apellido, documento):
        self._nombre = nombre
        self._apellido = apellido
        self._documento = documento

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, apellido):
        self._apellido = apellido

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, documento):
        self._documento = documento

    def __str__(self):
        return f'\tNombre: {self._nombre} \n ' \
               f'\tApellido: {self._apellido} \n ' \
               f'\tDocumento: {self._documento}'

