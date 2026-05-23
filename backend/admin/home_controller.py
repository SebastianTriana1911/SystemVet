# Clase que crea la nueva vista
from view.admin.gestion_admin_view import * 
from view.admin.gestion_medico_view import * 
from tkinter import messagebox
import customtkinter as ctk

class HomeController():
    def __init__(self, ventana_home_admin, datos_usuario, tipo_boton):
        # Guardamos la ventana que recibimos de la vista Home
        self.ventana_home_admin = ventana_home_admin
        self.datos_usuario = datos_usuario
        self.tipo_boton = tipo_boton


        # Validacion del tipo de boton que se esta precionando para que asi mismo ejecute el metodo correspondiente 
        if tipo_boton == "Admin":
            # Ejecutamos el método para cambiar de pantalla de una vez
            self.abrir_ventana_gestion_admin()

        elif tipo_boton == "Medico":
            self.abrir_ventana_gestion_medico()

        elif tipo_boton == "Reporte":
            pass
            # self.abrir_ventana_gestion_reporte()

        else:
            messagebox.showerror("Error de apertura de ventana", "Hubo un error al querer abrir la ventanta")

    def abrir_ventana_gestion_admin(self):
        # Cerramos la ventana Home, que es la que recibimos como parametro
        self.ventana_home_admin.destroy()

        # Creamos la nueva raíz para la gestión
        ventana_gestion_admin= ctk.CTk()
        ventana_gestion_admin.after(0, lambda: ventana_gestion_admin.state('zoomed'))

        
        # Instanciamos la vista de gestión pasando la nueva raíz
        GestionAdminVentana(ventana_gestion_admin, self.datos_usuario)

        ventana_gestion_admin.mainloop()

    
    def abrir_ventana_gestion_medico(self):
        # Cerramos la ventana Home, que es la que recibimos como parametro
        self.ventana_home_admin.destroy()

        # Creamos la nueva raíz para la gestión
        ventana_gestion_medico= ctk.CTk()
        ventana_gestion_medico.after(0, lambda: ventana_gestion_medico.state('zoomed'))

        
        # Instanciamos la vista de gestión pasando la nueva raíz
        GestionMedicosVentana(ventana_gestion_medico, self.datos_usuario)

        ventana_gestion_medico.mainloop()
        