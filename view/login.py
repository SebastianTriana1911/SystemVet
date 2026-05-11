""" 
Este archivo esta diseñado para manejar la vista del login y su logica, como validacion de usuario y contraseña
"""

from backend.registro import *
from view.indexAdmin import *
from tkinter import messagebox
import tkinter as tk

# Configuracion de la ventana login 
class LoginVentana:
    def __init__(self, ventana):
        # ----------- CONFIGURACION DE LA VENTANA -----------
        self.ventana = ventana
        self.ventana.geometry("430x440+540+180") # Se inicializan la posicion y el tamaño de la ventana
        self.ventana.minsize(430,440) # Se maneja un minimo de px para la ventana
        self.ventana.maxsize(430,440) # Se maneja un maximo de px para la ventana
        self.ventana.title("Sistema Veterinario / Login") # Titulo de la ventana
        self.ventana.config(bg="white", bd=12) # El color de la ventana sera blanco
        # ----------------------------------------------------

        # ----------- CONFIGURACION DEL ENCABEZADO ----------- 
        header = tk.Frame(self.ventana, bg="#2b8ee6")
        header.pack(side="top", fill="x") # Se muestra en la ventana

        tk.Label(header, text="INICIAR SESIÓN", bg="#2b8ee6", fg="white", 
                font=("Aharoni", 18, "bold"), pady=12).pack()
        # ----------------------------------------------------

        # ------------- CONFIGURACION DEL CUERPO -------------
        cuerpo = tk.Frame(self.ventana, bg="white") # Contenedor de los elementos contenidos en el cuerpo
        cuerpo.pack()

        self.imageLogin = tk.PhotoImage(file="image/result_acceso_login.png") # Acceder a la imagen
        imagenCuerpo = tk.Label(cuerpo, bg="white", image=self.imageLogin, pady=3)
        imagenCuerpo.pack()

        # ---- CAMPOS DE ENTRADA DE TEXTO ----
        tk.Label(cuerpo, text="Usuario", bg="white", fg="black",
                font=("Ahoroni", 10)).pack(anchor="w") # El mensaje Usuario ocupara todo el anchor
        self.ent_nit = tk.Entry(cuerpo, width=48, bd=1, relief="solid", # Campo de texto mantiene un borde solido con un grosor de 1 px
                                font=("Aharoni", 10))
        self.ent_nit.pack(pady=5, ipady=4) # Mantiene una distancia tanto de exterior como interior

        tk.Label(cuerpo, text="Contraseña", bg="white", fg="black",
                font=("Ahoroni", 10)).pack(anchor="w") # El mensaje Contraseña ocupara todo el anchor
        self.ent_pass = tk.Entry(cuerpo, width=48, bd=1, relief="solid", show="*", # El parametro show permite visualizar cada caracter con un *
                                font=("Aharoni", 10))
        self.ent_pass.pack(pady=5, ipady=4) # Mantiene una distancia tanto de exterior como interior
        # ------------------------------------

        # ---- BOTON PARA INGRESAR ----
        self.btn_ingresar = tk.Button(cuerpo, text="INGRESAR", bg="#61a781", fg="white", width=34, pady=5,
                                    font=("Aharoni", 12, "bold"), 
                                    command=self.validar_acceso) # Al hacer click, el boton llama al metodo
        self.btn_ingresar.pack(pady=20)
        # -----------------------------
        # ----------------------------------------------

    def validar_acceso(self):
        # Le asignamos a las variables la informacion capturada en el Entry
        nit_ingresado = self.ent_nit.get()
        pass_ingresado = self.ent_pass.get()

        # Al instanciar un objeto de esta clase, ejecuta el archivo .json
        validacion = GestionUsuarios()
        exito, resultado, nombre_usuario, datos_usuario = validacion.validar_login(nit_ingresado, pass_ingresado)

        # Si el usuario ingresado coinside con la informacion guardada en el archivo .json se le muestra
        # un mensaje de bienvenida y se ejecuta una nueva ventana segun el rol
        if (exito):
            if (datos_usuario["sexo"] == "Masculino"):
                messagebox.showinfo("Credenciales correctas", f"Bienvenido {nombre_usuario}.")
            else:
                messagebox.showinfo("Credenciales correctas", f"Bienvenida {nombre_usuario}.")

            # Se valida el rol del usuario para identificar que vista se le mostrara
            if resultado == "administrador":
                self.ventana.destroy() # Se elimina la pantalla del login
                ventana_index_admin = IndexVentanaAdmin(datos_usuario) # Se crea una nueva instancia para la vista siguiente
                ventana_index_admin.mainloop() 
            else:
                pass # CODIGO PARA MEDICOS
        else:
            messagebox.showerror("Credenciales incorrectas", resultado) # Mensaje de error
            if resultado == "Contraseña incorrecta":
                self.ent_pass.delete(0, tk.END) # Se borra la informacion del campo contraseña
            else:
                self.ent_nit.delete(0, tk.END) # Se borra la informacion del campo usuario
                self.ent_pass.delete(0, tk.END) # Se borra la informacion del campo contraseña
