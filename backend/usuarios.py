""" 
El archivo usuarios.py esta diseñado para la logica de los roles en el sistema, al existir unicamente dos
roles administrador y usuarios, se mantiene un orden utilizando POO utilizando clases que heredan de otras 
"""

# Clase principal Usuario
class Usuario:
    def __init__(self, username, password, nombre, apellido):
        self.__username = username # Username es un atributo privado
        self.__password = password # Password es un atributo privado
        self.nombre = nombre
        self.apellido = apellido

    def validar_password(self, password):
        return self.__password == password

    def get_username(self):
        return self.__username

# Clase Administrador, hereda los atributos y metodos de la clase Usuario
class Administrador(Usuario):
    def __init__(self, username, password, nombre, apellido):
        super().__init__(username, password, nombre, apellido)
        self.rol = "Admin"

class Medico(Usuario):
    def __init__(self, username, password, nombre, apellido, nit, especialidad):
        super().__init__(username, password, nombre, apellido)
        self.nit = nit
        self.especialidad = especialidad
        self.rol = "Medico"