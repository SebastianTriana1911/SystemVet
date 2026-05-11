""" 
Este archivo esta diseñado para manejar la logica de validaciones de usuario, acceder al archivo .json el
cual contiene todos los usuarios registrados y verificar si la informacion ingresada en la ventana de login
corresponde a un usuario ya existente
"""
import json

class GestionUsuarios:
    def __init__(self):
        # Cada que se intancie un nuevo objeto el constructor accedera a el archivo .json con los usuarios
        self.archivo = "data/usuarios.json"

    def obtener_usuarios(self):
        # Abrir archivo en forma de lectura con el apostrofe "r" 
        with open(self.archivo, 'r') as f:
            return json.load(f)
        
    def validar_login(self, nit_ingresado, pass_ingresado):
        usuarios = self.obtener_usuarios() # Accedemos al metodo que abre el archivo de usuarios registrados

        # Validamos si el nit ingresado en la ventana del login pertenece a las claves del diccionario
        if nit_ingresado in usuarios:
            datos_usuario = usuarios[nit_ingresado] # Abre un nuevo diccionario con la informacion correspondiente al nit

            # Verificamos contraseña
            if datos_usuario["password"] == pass_ingresado:
                # Retornamos si la validacion fue exitosa, el rol del usuario y el nombre
                return True, datos_usuario["rol"], datos_usuario["nombre"], datos_usuario
            else:
                return False, "Contraseña incorrecta", "null", "null"
        else:
            return False, "Usuario no encontrado en el sistema", "null", "null"