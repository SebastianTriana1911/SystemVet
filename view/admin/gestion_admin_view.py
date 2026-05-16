from tkinter import ttk
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
        self.ventana.title("SystemVet - Gestión de Administradores")
        self.ventana.configure(bg="black", bd=10)
        # ===========================================================================

        # ==========================================================================
        # CONFIGURACION DEL HEADER
        # ==========================================================================
        self.header = tk.Frame(self.ventana,
                                bg="#45A29E",)
        self.header.pack(side="top",
                          fill="x") # Mantiene el 100% del ancho en la pantalla
        
        # Se crea un boton que contenga la imagen del logo que permita volver hacia atras
        self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2)

        # Crear el Botón en lugar del Label
        self.btn_regresar = tk.Button(self.header,
                                       image=self.image_logo,
                                        bg="#45A29E",          # Mismo color del header
                                         activebackground="#45A29E", # Color cuando se presiona
                                          bd=0,                  # Quita el borde relieve default
                                           cursor="hand2",        # Cambia el cursor a manito
                                            width=70,
                                             height=70,
                                              command= lambda: GestionAdminController.regresar_ventana(self.ventana, datos_usuario))

        # Mantener la referencia de la imagen (evita que desaparezca)
        self.btn_regresar.image = self.image_logo
        self.btn_regresar.pack(side="left", padx=20, pady=10)

        tk.Label(self.header,
                  text="GESTIÓN DE ADMINISTRADORES",
                    fg="white", 
                     bg="#45A29E", 
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
                                 bg="#45A29E", 
                                  image=self.image_avatar,)
        image_avatar.image = self.image_avatar
        image_avatar.pack(side="right", padx=(0,20))

        # Este contenedor permitira acomodar dos Label arriba y abajo
        self.container_usuario = tk.Frame(self.header,
                                           bg="#45A29E")
        self.container_usuario.pack(side="right", padx=20)
        
        # Etiqueta "Administrador" parte superior
        if datos_usuario["sexo"] == "Masculino":
            tk.Label(self.container_usuario,
                     text="Administrador",
                      bg="#45A29E",
                       fg="white",
                        font=("Segoe UI", 15, "bold")).pack(side="top", anchor="e")
        else:
            tk.Label(self.container_usuario,
                     text="Administradora",
                      bg="#45A29E",
                      fg="white",
                       font=("Segoe UI", 14, "bold")).pack(side="top", anchor="e")
        
        # Contenedor que organiza el nombre del usuario y el boton de manera horizontal
        self.fila_nombre = tk.Frame(self.container_usuario,
                                     bg="#45A29E")
        self.fila_nombre.pack(side="top", anchor="e")
        
        # Nombre del usuario en la parte izquierda
        tk.Label(self.fila_nombre,
                   text=f"{datos_usuario['nombre']} {datos_usuario["apellido"]}    | ",
                    bg="#45A29E",
                     fg="white", 
                      font=("Segoe UI", 13)).pack(side="left", padx=(0, 5))
        
        # Botón Cerrar Sesión (Al lado del nombre)
        self.btn_cerrar_sesion = tk.Button(self.fila_nombre, 
                                            text="Cerrar sesión", 
                                             bg="#45A29E", 
                                                fg="white",
                                                 font=("Segoe UI", 13, "bold"),                                                  
                                                  borderwidth=0,
                                                   cursor="hand2",
                                                    command= lambda:GestionAdminController.cerrar_sesion(ventana) # Cambia el cursor al pasar por encima
                                           )
        self.btn_cerrar_sesion.pack(side="left")
        # ===========================================================================


        # ==========================================================================
        # CONFIGURACION DEL TITULO DEL CUERPO
        # ==========================================================================
        # Contenedor titulo
        self.contenedor_titulo = tk.Frame(self.ventana,
                                          background="#242427",
                                            padx=40,
                                             pady=15)    
        self.contenedor_titulo.pack(fill="x")

        # Título a la izquierda
        tk.Label(self.contenedor_titulo, 
                 text="ADMINISTRADORES REGISTRADOS EN LA BASE DE DATOS", 
                 fg="white", 
                  bg="#242427", 
                   font=("Segoe UI", 15, "bold")).pack(side="left")

        # Botón a la derecha
        self.btn_crear_admin = ctk.CTkButton(self.contenedor_titulo, 
                                      text="+ Registrar Admin", 
                                       fg_color="#0A6DDF",       # Reemplaza 'bg' (Azul)
                                        text_color="white",       # Reemplaza 'fg'
                                         hover_color="#294BBB",    
                                          font=("Segoe UI", 15, "bold"),
                                           width=160,                # Ancho adaptado en píxeles para este botón
                                            height=50,                
                                             border_width=0,           # Eliminamos el borde antiguo de tk
                                              corner_radius=15,         
                                               cursor="hand2",
                                                command= lambda: GestionAdminController.abrir_formulario_registro(self.ventana, self.controlador_admin)
                                                                  )
        self.btn_crear_admin.pack(side="right", padx=10, pady=5)

        # Se genera una linea para separar las secciones
        self.linea_divisor = tk.Frame(self.ventana,
                                       bg="white",
                                         height=2)
        self.linea_divisor.pack(fill="x", padx=40, pady=(0,50))
        # ==========================================================================


        # ==========================================================================
        # CONFIGURACION DE LA TABLA ADMINS
        # ==========================================================================
        style = ttk.Style()
        style.theme_use("clam")

        # --- CUERPO DE LA TABLA (Ajuste de contraste) ---
        style.configure("Treeview",
                         background="#C2C2C2",       # Color base de la tabla
                          foreground="black",  # Color de la letra
                           fieldbackground="#C2C2C2",
                            rowheight=50,
                             font=("Segoe UI", 11, "bold"))
        
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) 
        
        # Color de selección
        style.map("Treeview",
                  background=[("selected", "#838282")], # Hover de los encabezados
                   foreground=[("selected", "black")])
        
        # Configuracion de los encabezados
        style.configure("Treeview.Heading",
                         background="#19191A",      
                          foreground="white",
                           font=("Segoe UI", 12, "bold"),
                            bordercolor="#1A1A1E",      # Esto ayuda a definir la intersección superior
                             borderwidth=3)
        
        style.map("Treeview.Heading", background=[("active", "#818385")])
                
        # Contenedor de la tabla
        self.contenedor_tabla = ctk.CTkFrame(self.ventana, fg_color="#1A1A1E", corner_radius=15)
        self.contenedor_tabla.pack(fill="both",
                                    expand=True,
                                      padx=200,
                                        pady=(20,70))

        # Nombre de las columnas
        columnas = ("Nit", "Nombre", "Apellido", "Sexo", "Telefono", "Password", "Acciones")

        # Creacion de los apartados de la tabla
        self.tabla = ttk.Treeview(self.contenedor_tabla, 
                                   columns=columnas, 
                                    show="headings", 
                                     selectmode="browse",
                                      style="Treeview")

        # Dibujo de la separacion entre las filas
        self.tabla.tag_configure('par', background="#C7C7C7")
        self.tabla.tag_configure('impar', background="#B1B1B1") # Un gris mas oscuro para diferenciar

        # Scrollbar
        self.scroll_y = ttk.Scrollbar(self.contenedor_tabla,
                                       orient="vertical",
                                         command=self.tabla.yview)
        
        self.tabla.configure(yscrollcommand=self.scroll_y.set)


        # Configuracion de las columnas
        self.tabla.column("Nit", width=80, anchor="center", stretch=True)
        self.tabla.column("Nombre", width=80, anchor="center", stretch=True)
        self.tabla.column("Apellido", width=80, anchor="center", stretch=True)
        self.tabla.column("Sexo", width=80, anchor="center", stretch=True)
        self.tabla.column("Telefono", width=80, anchor="center", stretch=True)
        self.tabla.column("Password", width=80, anchor="center", stretch=True)
        self.tabla.column("Acciones", width=80, anchor="center", stretch=True)



        # Cabeceras
        for col in columnas:
            self.tabla.heading(col, text=col.upper())



        # Empaquetado
        self.scroll_y.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)



        # Esta instancia de la clase GestionAdminControler me permite acceder al metodo de cargar tabla
        self.controlador_admin = GestionAdminController(self)

        # Este atributo contiene toda la informacion de la tabla con los registro, por ender, despues de crear
        # un nuevo administrador en el formulario, se pasa este metodo, puesto que es el que permite cargar 
        # y mostrar nuevamente la tabla con todos los datos actualizados
        self.controlador_admin.cargar_datos_tabla() 
        # ==========================================================================
