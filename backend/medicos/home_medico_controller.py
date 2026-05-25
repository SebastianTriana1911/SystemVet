# Clase que crea la nueva vista
from view.medico.crear_cita_view import CrearCitaView
from view.medico.consultar_citas_view import ConsultarCitasView
from tkinter import messagebox
import customtkinter as ctk

class HomeController():
    def _init_(self, ventana_home_medico, datos_usuario, tipo_boton):
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

    def abrir_ventana_crear_cita(self):
        self.ventana_home_medico.destroy()
        ventana_crear_cita = ctk.CTk()
        ventana_crear_cita.after(0, lambda: ventana_crear_cita.state('zoomed'))
        CrearCitaView(ventana_crear_cita, self.datos_usuario)
        ventana_crear_cita.mainloop()

    def abrir_ventana_consultar_cita(self):
        self.ventana_home_medico.destroy()
        ventana_consultar = ctk.CTk()
        ventana_consultar.after(0, lambda: ventana_consultar.state('zoomed'))
        ConsultarCitasView(ventana_consultar, self.datos_usuario, modo="Pendiente")
        ventana_consultar.mainloop()