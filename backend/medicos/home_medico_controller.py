# Clase que crea la nueva vista
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

    def abrir_ventana_crear_cita(self):
        self.ventana_home_medico.destroy()
        VentanaCrearCita(self.datos_usuario)

    def abrir_ventana_consultar_cita(self):
        self.ventana_home_medico.destroy()
        VentanaConsultarCitas(self.datos_usuario)