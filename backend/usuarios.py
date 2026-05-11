""" 
Este archivo esta diseñado para mantener la logica de los usuarios que ingresan al sistema, los usuarios
permitidos (Administrador, Medico) donde cada uno tienen sus atributos y metodos propios
"""
# Clase principal Usuario
class Usuario:
    def __init__(self, nit, password, nombre, apellido, sexo):
        # Atributos privados
        self.__nit = nit
        self.__password = password

        # Atributos publicos
        self.nombre = nombre
        self.apellido = apellido
        self.sexo = sexo # Se recibe como parametro Masculino o Femenino
        self.estado = True

        # if self.sexo == "Masculino":
        #     self.foto_perfil = "image/foto_perfil_m.png"
        # else:
        #     self.foto_perfil = "image/foto_perfil_f.png" 

    # Metodos para acceder a los atributos privados
    def get_nit(self):
        return self.__nit
    
    def verificar_password(self, psw):
        return self.__password == psw
    

# Clase Administrador que hereda de Usuarios
class Administrador(Usuario):
    def __init__(self, nit, password, nombre, apellido, sexo):
        # Llamamos al constructor del padre
        super().__init__(nit, password, nombre, apellido, sexo)
        self.rol = "Administrador"


# Clase Medico que hereda de Usuario
class Medico(Usuario):
    def __init__(self, nit, password,nombre, apellido, sexo, especialidad):
        super().__init__(nit, password, nombre, apellido, sexo)
        self.especialidad = especialidad
        self.rol = "Medico"
        self.citas_asignadas = []

    def puede_ser_eliminado(self):
        # Retorna True si no tiene citas pendientes, False si tiene citas.
        return len(self.citas_asignadas) == 0