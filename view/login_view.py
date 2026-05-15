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
        # CONFIGURACION DE VENTANA
        # ==========================================================================
        # Cada que se instancia un objeto el constructor recibe como parametro la ventana
        self.ventana = ventana 

        # Este metodo permite modificar el color de la barra de la ventana 
        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico") # Se muesta en ventana un icono
        self.ventana.title("SystemVet / Login") # Titulo de la ventana
        self.ventana.config(bg="#1A1A1E",
                            bd=10) # El color de la ventana sera blanco
        # ===========================================================================


        # ==========================================================================
        # CONFIGURACION DEL HEADER
        # ==========================================================================
        header = tk.Frame(self.ventana,
                           bg="#6745B8")
        
        header.pack(side="top",
                     fill="x") # Se muestra en la ventana ocupando el espacio en horizontal

        # Dentro del contenedor del header se crea un Label que contiene un texto con las siguientes propiedades
        tk.Label(header, 
                 text="INICIAR SESIÓN",
                    bg="#6745B8",
                      fg="white", 
                      font=("Segoe UI", 18, "bold"),
                        pady=10).pack(ipady=5)
        # ==========================================================================
        

        # ==========================================================================
        #  CONFIGURACION DEL CUERPO
        # ========================================================================== 
        # Acceder a la imagen del Logotipo con el nombre del proyecto
        self.image_login = tk.PhotoImage(file="image/logotipo.png")
        imagen_cuerpo = tk.Label(self.ventana,
                                  bg="#1A1A1E",
                                    image=self.image_login)
        imagen_cuerpo.pack(pady=(35, 5))
        
        tk.Label(self.ventana,
                  text="SYSTEM VET",
                    bg="#1A1A1E",
                      fg="white",
                       font=("Stencil", 24, "bold")).pack(pady=(0, 30))

        # Se crea el cuerpo del login que es el contenedor que va a guardar los entry y el boton
        cuerpo = tk.Frame(self.ventana,
                           bg="#1A1A1E")
        cuerpo.place(relx=0.5,
                      rely=0.5,
                        anchor="center") # Esto centra el login totalmente

        contenedor_entry = ctk.CTkFrame(cuerpo,
                                         fg_color="#404047",
                                          corner_radius=15,
                                           border_width=0)
        contenedor_entry.pack(padx=20, pady=10, ipady=10, ipadx=40)

        # Campo del usuario
        tk.Label(contenedor_entry,
                  text="👤 Usuario",
                    bg="#404047",
                      fg="white",
                        font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=40, pady=(35, 0))

        self.ent_nit = ctk.CTkEntry(contenedor_entry, 
                                    width=290,
                                     height=35,
                                      fg_color="#AAA9A9", 
                                       border_color="white",
                                        text_color="#333333",
                                         border_width=2,
                                          corner_radius=10,
                                           justify="center",
                                            font=("Segoe UI", 14, "bold"))
        self.ent_nit.pack(pady=(5, 20))

        # Campo de la contraseña
        tk.Label(contenedor_entry,
                  text="🔒 Contraseña",
                    bg="#404047",
                      fg="white", 
                        font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=40)

        self.ent_pass = ctk.CTkEntry(contenedor_entry,
                                     width=290,
                                      height=35,
                                       fg_color="#AAA9A9",
                                        text_color="#333333",
                                         border_width=2,
                                          border_color="white",
                                           corner_radius=10,
                                            justify="center",
                                             show="*",
                                              font=("Segoe UI", 14, "bold"))    
        self.ent_pass.pack(pady=(5, 45))

        # Capturar los eventros del mouse al pasar por los Entry
        # Usuario
        self.ent_nit.bind("<Enter>", lambda e: LoginController.al_entrar_entry(self.ent_nit))
        self.ent_nit.bind("<Leave>", lambda e: LoginController.al_salir_entry(self.ent_nit))
        # Contraseña
        self.ent_pass.bind("<Enter>", lambda e: LoginController.al_entrar_entry(self.ent_pass))
        self.ent_pass.bind("<Leave>", lambda e: LoginController.al_salir_entry(self.ent_pass))
        # # ==========================================================================


        # ==========================================================================
        #  CONFIGURACION DEL BOTON
        # ========================================================================== 
        # 3. BOTÓN INGRESAR (Dentro del contenedor gris)
        self.btn_ingresar = ctk.CTkButton(contenedor_entry, 
                                           text="INGRESAR", 
                                            fg_color="#7249D3",       
                                             text_color="white",       
                                              hover_color="#53339E",    
                                               width=220,                
                                                height=40,                
                                                 border_width=0,           
                                                  corner_radius=15,         
                                                   font=("Segoe UI", 14, "bold"), 
                                                    cursor="hand2",           
                                                     command=self.validar_acceso)

        self.btn_ingresar.pack(pady=(0, 30))
        # ==========================================================================


    # ==========================================================================
    # METODO DE VALIDACION DE DATOS 
    # ==========================================================================
    def validar_acceso(self):
        # Le asignamos a las variables la informacion capturada en el Entry
        nit_ingresado = self.ent_nit.get()
        pass_ingresado = self.ent_pass.get()

        # Al instanciar un objeto de esta clase, ejecuta el archivo .json
        validacion = LoginController()
        exito, resultado, datos_usuario = validacion.validar_login(nit_ingresado, 
                                                                   pass_ingresado)

        # Si el usuario ingresado coinside con la informacion guardada en el archivo .json se le muestra
        # un mensaje de bienvenida y se ejecuta una nueva ventana segun el rol
        if (exito):
            if (datos_usuario["sexo"] == "Masculino"):
                messagebox.showinfo("Credenciales correctas",
                                     f"Bienvenido {datos_usuario["nombre"]} a SystemVet")
            else:
                messagebox.showinfo("Credenciales correctas",
                                     f"Bienvenida {datos_usuario["nombre"]} a SystemVet")

            # Se valida el rol del usuario para identificar que vista se le mostrara
            if resultado == "administrador":
                self.ventana.destroy() # Se elimina la pantalla del login
                ventana_home_admin = HomeVentana(datos_usuario) # Se crea una nueva instancia para la vista siguiente
                ventana_home_admin.mainloop() 
            else:
                pass # CODIGO PARA MEDICOS
        else:
            messagebox.showerror("Credenciales incorrectas", resultado) # Mensaje de error
            if resultado == "Contraseña incorrecta":
                self.ent_pass.delete(0, tk.END) # Se borra la informacion del campo contraseña
            else:
                self.ent_nit.delete(0, tk.END) # Se borra la informacion del campo usuario
                self.ent_pass.delete(0, tk.END) # Se borra la informacion del campo contraseña
    # ==========================================================================
