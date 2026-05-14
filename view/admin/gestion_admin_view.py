# from tkinter import ttk
import customtkinter as ctk
import tkinter as tk
from backend.admin.gestion_admin_controller import *


class GestionAdminVentana:
    def __init__(self, ventana, datos_usuario):
        # ==========================================================================
        # CONFIGURACION DE VENTANA
        # ==========================================================================
        self.ventana = ventana
        self.datos_usuario = datos_usuario

        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico") # Se muesta en ventana un icono
        self.ventana.title("SystemVet / Gestión de Administradores")
        self.ventana.configure(bg="#1A1A1E", bd=10)
        # ===========================================================================


        # ==========================================================================
        # CONFIGURACION DEL HEADER
        # ==========================================================================
        self.header = tk.Frame(self.ventana,
                                bg="#6745B8",)
        self.header.pack(side="top",
                          fill="x") # Mantiene el 100% del ancho en la pantalla
        
        self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2) # Acceder a la imagen
        image_logo = self.image_logo
        image_logo = tk.Label(self.header,
                                  bg="#6745B8",
                                  width=70,
                                  height=70,
                                    image=self.image_logo)
        image_logo.image = self.image_logo
        image_logo.pack(side="left", padx=20, pady=10)

        tk.Label(self.header,
                  text="GESTIÓN DE ADMINISTRADORES",
                    fg="white", 
                     bg="#6745B8", 
                      font=("Segoe UI", 15, "bold")).pack(side="left")
        

        if datos_usuario["sexo"] == "Masculino":
            avatar = "image/avatar_masculino.png"
        else:
            avatar = "image/avatar_femenino.png"

        # Cargar la imagen original y redimensionar usando subsample
        img_original = tk.PhotoImage(file=avatar) 
        self.image_avatar = img_original.subsample(2, 2)

        # El Label debe coincidir con el tamaño resultante
        image_avatar = tk.Label(self.header,
                                 bg="#6745B8", 
                                  image=self.image_avatar,)
        image_avatar.image = self.image_avatar
        image_avatar.pack(side="right", padx=(0,20))

        # Este contenedor permitira acomodar dos Label arriba y abajo
        self.container_usuario = tk.Frame(self.header,
                                           bg="#6745B8")
        self.container_usuario.pack(side="right", padx=20)
        
        # Etiqueta "Administrador" parte superior
        if datos_usuario["sexo"] == "Masculino":
            tk.Label(self.container_usuario,
                     text="Administrador",
                      bg="#6745B8",
                      fg="white",
                       font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")
        else:
            tk.Label(self.container_usuario,
                     text="Administradora",
                      bg="#6745B8",
                      fg="white",
                       font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")
        
        # Contenedor que organiza el nombre del usuario y el boton de manera horizontal
        self.fila_nombre = tk.Frame(self.container_usuario,
                                     bg="#6745B8")
        self.fila_nombre.pack(side="top", anchor="e")
        
        # Nombre del usuario en la parte izquierda
        tk.Label(self.fila_nombre,
                   text=f"{datos_usuario['nombre']} {datos_usuario["apellido"]}    | ",
                    bg="#6745B8",
                     fg="white", 
                      font=("Segoe UI", 13)).pack(side="left", padx=(0, 5))
        
        # Botón Cerrar Sesión (Al lado del nombre)
        self.btn_cerrar_sesion = tk.Button(self.fila_nombre, 
                                            text="Cerrar sesión", 
                                             bg="#6745B8", 
                                                fg="white",
                                                 font=("Segoe UI", 12, "bold"),                                                  
                                                  borderwidth=0,
                                                   cursor="hand2",
                                                    command= lambda:GestionAdminController.cerrar_sesion(ventana) # Cambia el cursor al pasar por encima
                                           )
        self.btn_cerrar_sesion.pack(side="left")
        # ===========================================================================


        # ==========================================================================
        # CONFIGURACION DEL CUERPO
        # ==========================================================================
        # Contenedor titulo
        self.contenedor_titulo = tk.Frame(self.ventana,
                                            bg="#1A1A1E",
                                              padx=40,
                                                pady=20)
        self.contenedor_titulo.pack(fill="x")

        # Título a la izquierda
        tk.Label(self.contenedor_titulo, 
                 text="ADMINISTRADORES REGISTRADOS EN LA BASE DE DATOS", 
                 fg="white", 
                  bg="#1A1A1E", 
                   font=("Segoe UI", 15, "bold")).pack(side="left")

        # Botón a la derecha
        self.btn_crear_admin = tk.Button(self.contenedor_titulo, 
                                            text="+ Registrar Admin", 
                                             bg="#6745B8", 
                                              fg="white",
                                                font=("Segoe UI", 13, "bold"),
                                                 padx=15, pady=5,
                                                  borderwidth=3,
                                                   cursor="hand2")
        self.btn_crear_admin.pack(side="right")

        # --- DIVISOR VISUAL ---
        # Una línea delgada para separar las secciones
        self.linea_divisor = tk.Frame(self.ventana, bg="white", height=2)
        self.linea_divisor.pack(fill="x", padx=40, pady=5)


    # def ejecutar_carga(self):
    #     # Aquí llamas al método del controlador que te mostré antes
    #     # self.controlador.cargar_datos_tabla()
    #     pass