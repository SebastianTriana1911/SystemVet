""" 
Este archivo esta diseñado para manejar la logica de validaciones de usuario, acceder al archivo .json el
cual contiene todos los usuarios registrados y verificar si la informacion ingresada en la ventana de login
corresponde a un usuario ya existente
"""
import json

class LoginController:
    def __init__(self):
        # Cada que se intancie un nuevo objeto el constructor accedera a el archivo .json con los usuarios
        self.archivo = "data/usuarios.json"

    # ==========================================================================
    # LOGICA DE VALIDACION DE DATOS
    # ==========================================================================
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
                return True, datos_usuario["rol"], datos_usuario
            else:
                return False, "Contraseña incorrecta", "null"
        else:
            return False, "Usuario no encontrado en el sistema", "null"
    # ==========================================================================
        

    # ==========================================================================
    # FUNCIONES PARA EFECTOS VISUALES DE LOS CAMPOS DE ENTRADA "ENTRY"
    # ==========================================================================
    def entrada_foco(e):
        e.widget.config(bg="white", fg="#000000") # Fondo blanco puro al escribir
    def salida_foco(e):
        e.widget.config(bg="white", fg="#333333") # Gris claro cuando no está seleccionado
    def entrada_hover(e, ventana):
        if ventana.focus_get() != e.widget: # Solo si el usuario no está escribiendo en él
            e.widget.config(bg="white")
    def salida_hover(e, ventana):
        if ventana.focus_get() != e.widget:
            e.widget.config(bg="#DADADA")


    def on_enter(e):
        e.widget['background'] = "#53339E" # Color más claro al entrar

    def on_leave(e):
        e.widget['background'] = "#6745B8" # Color original al salir
    # ==========================================================================


