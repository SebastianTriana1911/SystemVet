# Clase que crea la nueva vista

from view.medicos.crear_citas_medico import VentanaCrearCita
from view.medicos.consultar_citas_medico import VentanaConsultarCitas

from view.medicos.crear_citas_medico import VentanaCrearCita
from view.medicos.consultar_citas_medico import VentanaConsultarCitas

from tkinter import messagebox
import customtkinter as ctk

class HomeControllerMedicos():  
    def __init__(self, ventana_home_medico, datos_usuario, tipo_boton):
        self.ventana_home_medico = ventana_home_medico
        self.datos_usuario = datos_usuario
        self.tipo_boton = tipo_boton

        if tipo_boton == "CrearCita":
            self.abrir_ventana_crear_cita()
        elif tipo_boton == "ConsultarCita":
            self.abrir_ventana_consultar_cita()
        elif tipo_boton == "CitasCompletadas":
            self.abrir_ventana_citas_completadas()
        else:
            messagebox.showerror("Error de apertura de ventana", "Hubo un error al querer abrir la ventana")

    # def abrir_ventana_crear_cita(self):
    #     self.ventana_home_medico.destroy()
    #     ventana_crear_cita = ctk.CTk()
    #     ventana_crear_cita.after(0, lambda: ventana_crear_cita.state('zoomed'))
    #     VentanaCrearCita(self.datos_usuario)
    #     ventana_crear_cita.mainloop()

    def abrir_ventana_crear_cita(self):
        # 1. Cerramos la ventana actual del Home
        self.ventana_home_medico.destroy()
        
        # 2. Instanciamos la vista pasándole ÚNICAMENTE los datos del usuario
        # (El constructor de VentanaCrearCita se encargará de crear el ctk.CTk() interno)
        nueva_ventana = VentanaCrearCita(self.datos_usuario)
        
        # 3. Arrancamos el bucle de la ventana que se creó dentro de la clase
        nueva_ventana.ventana.mainloop()

    def abrir_ventana_consultar_cita(self):
        self.ventana_home_medico.destroy()
        ventana_consultar = ctk.CTk()
        ventana_consultar.after(0, lambda: ventana_consultar.state('zoomed'))
        VentanaConsultarCitas(ventana_consultar, self.datos_usuario, modo="Pendiente")
        ventana_consultar.mainloop()

    def cerrar_sesion(ventana_actual):
        respuesta = messagebox.askyesno("Cierre de sesión", "¿Está seguro de cerrar la sesión?")
        if respuesta:
            ventana_actual.destroy()
            from main import iniciar_app
            iniciar_app()    
        VentanaCrearCita(self.datos_usuario)

    def abrir_ventana_consultar_cita(self):
        self.ventana_home_medico.destroy()
        VentanaConsultarCitas(self.datos_usuario)
