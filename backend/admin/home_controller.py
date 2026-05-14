# Clase que crea la nueva vista
from view.admin.gestion_admin_view import * 
import customtkinter as ctk

class HomeController():
    def __init__(self, ventana_home_admin, datos_usuario):
        # Guardamos la ventana que recibimos de la vista Home
        self.ventana_home_admin = ventana_home_admin
        self.datos_usuario = datos_usuario

        # Ejecutamos el método para cambiar de pantalla de una vez
        self.abrir_ventana_gestion_admin()

    def abrir_ventana_gestion_admin(self):
        # Cerramos la ventana Home, que es la que recibimos como parametro
        self.ventana_home_admin.destroy()

        # Creamos la nueva raíz para la gestión
        ventana_gestion_admin= ctk.CTk()
        ventana_gestion_admin.after(0, lambda: ventana_gestion_admin.state('zoomed'))

        
        # Instanciamos la vista de gestión pasando la nueva raíz
        GestionAdminVentana(ventana_gestion_admin, self.datos_usuario)

        ventana_gestion_admin.mainloop()