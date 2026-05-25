""" 
Este archivo esta diseñado para manejar la logica de validaciones de usuario, acceder al archivo .json el
cual contiene todos los usuarios registrados y verificar si la informacion ingresada en la ventana de login
corresponde a un usuario ya existente
"""
import json
from customtkinter import *

class LoginController:
    def __init__(self):
        # Cada que se intancie un nuevo objeto el constructor accedera a el archivo .json con los usuarios
        self.archivo = "data/usuarios.json"

    # ==========================================================================
    # LOGICA DE VALIDACION DE DATOS
    # ==========================================================================
    def obtener_usuarios(self):
        # Abrir archivo en forma de lectura con el apostrofe "r" 
        with open(self.archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def validar_login(self, nit_ingresado, pass_ingresado):
        usuarios = self.obtener_usuarios() # Accedemos al metodo que abre el archivo de usuarios registrados

        # Validamos si el nit ingresado en la ventana del login pertenece a las claves del diccionario
        if nit_ingresado in usuarios:
            datos_usuario = usuarios[nit_ingresado] # Abre un nuevo diccionario con la informacion correspondiente al nit

            # Verificamos contraseña
            if datos_usuario["password"] == pass_ingresado:
                # Agregamos el NIT / usuario al diccionario de datos del usuario
                datos_usuario["nit"] = nit_ingresado
                datos_usuario["id_medico"] = nit_ingresado
                # Retornamos si la validacion fue exitosa, el rol del usuario y el nombre
                return True, datos_usuario["rol"], datos_usuario
            else:
                return False, "Contraseña incorrecta", "null"
        else:
            return False, "Usuario no encontrado en el sistema", "null"
    # ==========================================================================
        

    # ==========================================================================
    # FUNCIONES PARA EFECTOS VISUALES DE LOS CAMPOS DE ENTRADA "ENTRY"
    # ==========================================================================
    def al_entrar_entry(widget):
        # Si el entry está vacío, aplicamos el efecto de "encendido"
        if len(widget.get()) == 0:
            widget.configure(fg_color="#0D0D0F") 
        else:
            widget.configure(fg_color="#1A1A1E")
        widget.update_idletasks()
    
    def al_salir_entry(widget):
        # Si el usuario NO ha escrito nada, vuelve al grisáceo original
        if len(widget.get()) == 0:
            widget.configure(fg_color="#1A1A1E")
        else:
            widget.configure(fg_color="#1A1A1E")
        widget.update_idletasks()
    # ==========================================================================


