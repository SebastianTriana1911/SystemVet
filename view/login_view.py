""" 
Este archivo esta diseñado para manejar la vista del login y su logica, como validacion de usuario y contraseña
"""
# Importaciones
import customtkinter as ctk

from customtkinter import *
from tkinter import messagebox
from backend.login_controller import *
from view.admin.home_view import *


# Configuracion de la ventana login 
class LoginVentana:
    def __init__(self, ventana):
        # ==========================================================================
        # CONFIGURACIÓN DE VENTANA
        # ==========================================================================
        self.ventana = ventana 

        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico") # Accedemos al icono
        self.ventana.title("SystemVet - Login") # Titulo de la ventana
        self.ventana.config(bg="#1A1A1E",
                             bd=10) 
        

        # ==========================================================================
        # CONFIGURACIÓN DEL HEADER (Nueva paleta Turquesa)
        # ==========================================================================
        header = tk.Frame(self.ventana, bg="#45A29E")
        header.pack(side="top", fill="x") 

        tk.Label(header, 
                 text="INICIAR SESIÓN", # Titulo principal
                  bg="#45A29E", # Color de fondo
                   fg="white", # Color de letra
                    font=("Segoe UI", 20, "bold"), # Propiedades para la letra
                     pady=10).pack(ipady=10) # Espaciado dentro del contenedor
        
        
        # ==========================================================================
        # CONFIGURACIÓN DEL CUERPO
        # ========================================================================== 
        # Accedemos al logotipo con unas dimensiones 
        self.image_login = tk.PhotoImage(file="image/logotipo_login.png").subsample(2, 2)

        imagen_cuerpo = tk.Label(self.ventana,
                                  bg="#1A1A1E", # Fondo de la imagen igual al fondo de la ventana
                                    image=self.image_login) # Se muestra la imagen en el Label
        imagen_cuerpo.pack(pady=(20,0), padx=(0,25))
        

        cuerpo = tk.Frame(self.ventana,
                           bg="#1A1A1E")
        # Configuracion para central el contenedor de los Entrys en el login
        cuerpo.place(relx=0.5, rely=0.5, anchor="center") 

        # Configuracion del contenedro central
        contenedor_entry = ctk.CTkFrame(cuerpo,
                                         fg_color="#242429",
                                          corner_radius=15, # Radio del contenedor
                                            border_width=2, # Grosor de bordes
                                             border_color="#45A29E")
        contenedor_entry.pack(padx=20, ipady=10, ipadx=75)


        # ==========================================================================
        # CAMPO DEL USUARIO
        # ========================================================================== 
        tk.Label(contenedor_entry,
                  text="👤 Usuario",
                    bg="#242429",
                      fg="white",
                        font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=70, pady=(40, 0))

        self.ent_nit = ctk.CTkEntry(contenedor_entry, 
                                     width=290, # Tamacho en horizontal del Entry
                                      height=38,
                                       placeholder_text="Número de documento",
                                        fg_color="#1A1A1E", # Fondo oscuro integrado
                                         border_color="#45A29E", # Borde turquesa
                                          text_color="white",
                                            border_width=1, # Grosor del borde
                                              corner_radius=10, # Radio del borde
                                                justify="center", # Justificacion del texto
                                                  font=("Segoe UI", 12, "bold"))
        self.ent_nit.pack(pady=(5, 15))

        # ==========================================================================
        # CAMPO DE LA CONTRASEÑA
        # ========================================================================== 
        tk.Label(contenedor_entry,
                  text="🔒 Contraseña",
                   bg="#242429",
                    fg="white", 
                     font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=70)

        self.ent_pass = ctk.CTkEntry(contenedor_entry,
                                      width=290,
                                       height=38,
                                        fg_color="#1A1A1E",      # Fondo oscuro integrado
                                          border_color="#45A29E",  # Borde turquesa
                                            text_color="white",
                                              border_width=1,
                                                corner_radius=10,
                                                  justify="center",
                                                    show="*",
                                                      placeholder_text="Password",
                                                        font=("Segoe UI", 12, "bold"))    
        self.ent_pass.pack(pady=(5, 40))

        # Eventos Hover para los campos
        self.ent_nit.bind("<Enter>", lambda e: LoginController.al_entrar_entry(self.ent_nit))
        self.ent_nit.bind("<Leave>", lambda e: LoginController.al_salir_entry(self.ent_nit))
        self.ent_pass.bind("<Enter>", lambda e: LoginController.al_entrar_entry(self.ent_pass))
        self.ent_pass.bind("<Leave>", lambda e: LoginController.al_salir_entry(self.ent_pass))


        # ==========================================================================
        # CONFIGURACIÓN DEL BOTÓN 
        # ========================================================================== 
        self.btn_ingresar = ctk.CTkButton(contenedor_entry, 
                                          text="INGRESAR", 
                                           fg_color="#45A29E",       # Turquesa principal
                                            text_color="white",       
                                              hover_color="#31726F",    # Turquesa oscuro al pasar el mouse
                                               width=200,                
                                                height=42,                
                                                  border_width=0,           
                                                    corner_radius=12,         
                                                      font=("Segoe UI", 15, "bold"), 
                                                        cursor="hand2",           
                                                          command=self.validar_acceso) # Llama al metodo encontrado en LoginController
        self.btn_ingresar.pack(pady=(0, 25))


    # ==========================================================================
    # MÉTODO DE VALIDACIÓN DE DATOS 
    # ==========================================================================
    def validar_acceso(self):
        nit_ingresado = self.ent_nit.get()
        pass_ingresado = self.ent_pass.get()

        validacion = LoginController()
        exito, resultado, datos_usuario = validacion.validar_login(nit_ingresado, pass_ingresado)

        if (exito):
            if (datos_usuario["sexo"] == "Masculino"):
                messagebox.showinfo("Credenciales correctas", f"Bienvenido {datos_usuario['nombre']} a SystemVet")
            else:
                messagebox.showinfo("Credenciales correctas", f"Bienvenida {datos_usuario['nombre']} a SystemVet")

            if resultado == "administrador":
                self.ventana.destroy() 
                ventana_home_admin = HomeVentana(datos_usuario) 
                # ventana_home_admin.mainloop() 
            else:
                pass 
        else:
            messagebox.showerror("Credenciales incorrectas", resultado) 
            if resultado == "Contraseña incorrecta":
                self.ent_pass.delete(0, tk.END) 
            else:
                self.ent_nit.delete(0, tk.END) 
                self.ent_pass.delete(0, tk.END)