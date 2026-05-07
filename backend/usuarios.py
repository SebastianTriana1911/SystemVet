""" 
El archivo usuarios.py esta diseñado para la logica de los roles en el sistema, al existir unicamente dos
roles administrador y usuarios, se mantiene un orden utilizando POO utilizando clases que heredan de otras 
"""

class Usuario:
    def __init__(self, username, password, nombre):
        self.__username = username
        self.__password = password
        self.nombre = nombre

    def validar_password(self, password):
        return self.__password == password

    def get_username(self):
        return self.__username

class Administrador(Usuario):
    def __init__(self, username, password, nombre):
        super().__init__(username, password, nombre)
        self.rol = "Admin"

class Medico(Usuario):
    def __init__(self, username, password, nombre, nit, especialidad):
        super().__init__(username, password, nombre)
        self.nit = nit
        self.especialidad = especialidad
        self.rol = "Medico"