""" 
Este archivo esta diseñado para manejar la vista del login y su logica, como validacion de usuario y contraseña
"""
import customtkinter as ctk

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
        
        # Tamaño definido de la ventana
        # ancho_ventana = 460
        # alto_ventana = 490

        # # Se obtiene el ancho y alto de la pantalla del usuario
        # ancho_pantalla = self.ventana.winfo_screenwidth()
        # alto_pantalla = self.ventana.winfo_screenheight()

        # # Se calcular la posición de la pantalla para que la ventana quede en el centro
        # x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        # y = (alto_pantalla // 2) - (alto_ventana // 2)
        # self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Se maneja un minimo de px para la ventana lo que permite que esta no se pueda ampliar
        # self.ventana.minsize(460,490) 
        # self.ventana.maxsize(460,490) 

        # Este metodo permite modificar el color de la barra de la ventana 
        
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
                        pady=10).pack()
        # ==========================================================================
        

        # ==========================================================================
        #  CONFIGURACION DEL CUERPO
        # ========================================================================== 
        # Se instancia un objeto Frame que actua como el contenedor de toda la info del login
        cuerpo = tk.Frame(self.ventana, 
                           bg="#1A1A1E")
        cuerpo.pack()

        self.image_login = tk.PhotoImage(file="image/logotipo.png") # Acceder a la imagen
        imagen_cuerpo = tk.Label(cuerpo,
                                  bg="#1A1A1E",
                                    image=self.image_login).pack(pady=(30,20))
        # ==========================================================================


        # ==========================================================================
        # CAMPOS DE ENTRADA
        # ==========================================================================
        tk.Label(cuerpo,
                  text="Usuario",
                    bg="#1A1A1E",
                      fg="white",
                      font=("Segoe UI", 11, "bold")).pack(anchor="w") # Ocupa todo el ancho
        
        self.ent_nit = tk.Entry(cuerpo, 
                                 width=35,
                                  bg="#DADADA",
                                   fg="#333333",
                                    bd=3, 
                                     highlightthickness=1, 
                                      highlightbackground="#FFFFFF", 
                                       justify="center",
                                        relief="solid", 
                                         font=("Segoe UI", 10, "bold"))
        self.ent_nit.pack(pady=3, ipady=2)
        
        # Vincular eventos y llama de manera anonima metodos de clase
        self.ent_nit.bind("<FocusIn>", lambda e:LoginController.entrada_foco(e))
        self.ent_nit.bind("<FocusOut>", lambda e:LoginController.salida_foco(e))
        self.ent_nit.bind("<Enter>", lambda e:LoginController.entrada_hover(e, self.ventana))
        self.ent_nit.bind("<Leave>", lambda e:LoginController.salida_hover(e, self.ventana))


        tk.Label(cuerpo,
                  text="Contraseña",
                    bg="#1A1A1E",
                      fg="white", 
                       font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(5,0))

        self.ent_pass = tk.Entry(cuerpo,
                                  width=35, 
                                    bg="#DADADA",
                                     fg="#333333",
                                      bd=3, 
                                       highlightthickness=1, 
                                        highlightbackground="white", 
                                         justify="center",
                                          show="*",
                                           relief="solid", 
                                            font=("Segoe UI", 10, "bold"))        
        self.ent_pass.pack(pady=3, ipady=3) # Mantiene una distancia tanto de exterior como interior

        # Vincular eventos y llama de manera anonima metodos de clase
        self.ent_pass.bind("<FocusIn>", lambda e:LoginController.entrada_foco(e))
        self.ent_pass.bind("<FocusOut>", lambda e:LoginController.salida_foco(e))
        self.ent_pass.bind("<Enter>", lambda e:LoginController.entrada_hover(e, self.ventana))
        self.ent_pass.bind("<Leave>", lambda e:LoginController.salida_hover(e, self.ventana))
        # ==========================================================================


        # ==========================================================================
        # BOTON INGRESAR
        # ==========================================================================
        self.btn_ingresar = tk.Button(cuerpo, 
                                        text="INGRESAR", 
                                         bg="#6745B8",
                                           fg="white",
                                            width=15, 
                                              pady=4,
                                              borderwidth=3, # Estilo de boton
                                               font=("Segoe UI", 10, "bold"), 
                                                cursor="hand2", # Cambia el cursor al pasar por encima
                                                 command=self.validar_acceso)
        
        # Vincular eventos y llama de manera anonima metodos de clase
        self.btn_ingresar.bind("<Enter>", lambda e: LoginController.on_enter(e))
        self.btn_ingresar.bind("<Leave>", lambda e: LoginController.on_leave(e))

        self.btn_ingresar.pack(pady=25)
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
                
               # nueva_ventana = ctk.CTk() # Creamos la nueva ventana principal
                
                 
                ventana_home_admin = HomeVentana(datos_usuario) # Se crea una nueva instancia para la vista siguiente
                ventana_home_admin.ventana.after(0, lambda: ventana_home_admin.ventana.state('zoomed')) # Maximizar
                ventana_home_admin.ventana.mainloop() 
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
