from tkinter import ttk
import customtkinter as ctk
import tkinter as tk
from backend.admin.gestion_admin_controller import *
from backend.login_controller import LoginController


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
        self.ventana.configure(bg="black", bd=10)
        # self.ventana.configure(bg="#1A1A1E", bd=10)
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
        # CONFIGURACION DEL TITULO DEL CUERPO
        # ==========================================================================
        # Contenedor titulo
        self.contenedor_titulo = tk.Frame(self.ventana,
                                          background="#242427",
                                            padx=40,
                                             pady=20)    
        self.contenedor_titulo.pack(fill="x")

        # Título a la izquierda
        tk.Label(self.contenedor_titulo, 
                 text="ADMINISTRADORES REGISTRADOS EN LA BASE DE DATOS", 
                 fg="white", 
                  bg="#242427", 
                   font=("Segoe UI", 15, "bold")).pack(side="left")

        # Botón a la derecha
        self.btn_crear_admin = tk.Button(self.contenedor_titulo, 
                                            text="+ Registrar Admin", 
                                             bg="#6745B8", 
                                              fg="white",
                                                font=("Segoe UI", 12, "bold"),
                                                 padx=10, pady=4,
                                                  borderwidth=3, # Diseño del boton
                                                   cursor="hand2") # Cambia el raton cuando se pasa por encima
        self.btn_crear_admin.pack(side="right") # El boton se encontrara a la derecha del contenedor

        # Se genera una linea para separar las secciones
        self.linea_divisor = tk.Frame(self.ventana,
                                       bg="white",
                                         height=2)
        self.linea_divisor.pack(fill="x", padx=40, pady=5)
        # ==========================================================================


        # ==========================================================================
        # CONFIGURACION DE LA TABLA ADMINS
        # ==========================================================================
        # --- CONFIGURACIÓN DE ESTILOS MODERNOS ---
        style = ttk.Style()
        style.theme_use("clam")

        # Personalizamos el cuerpo de la tabla (Full Dark)
        style.configure("Treeview", 
                        background="#242427", 
                        foreground="#E0E0E0", 
                        fieldbackground="#242427", 
                        rowheight=45, # Más alto para que se vea premium
                        font=("Segoe UI", 11),
                        borderwidth=0)

        # Encabezado Morado con altura y fuente clara
        style.configure("Treeview.Heading", 
                        background="#6745B8", 
                        foreground="white", 
                        relief="flat",
                        font=("Segoe UI", 12, "bold"))

        # Color al seleccionar una fila (Morado eléctrico)
        style.map("Treeview", background=[('selected', '#53339E')])
        


        # --- CONTENEDOR DE LA TABLA (Pantalla Completa) ---
        # Usamos fill="both" y expand=True para que ocupe todo el ancho y alto
        self.contenedor_tabla = tk.Frame(self.ventana, bg="#1A1A1E")
        self.contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        # Definición de columnas
        columnas = ("Nit", "Nombre", "Apellido", "Sexo", "Telefono", "Password", "Acciones")

        self.tabla = ttk.Treeview(self.contenedor_tabla, 
                                  columns=columnas, 
                                  show="headings", 
                                  selectmode="browse")

        # Scrollbar estilizado
        self.scroll_y = ttk.Scrollbar(self.contenedor_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll_y.set)

        # --- CONFIGURACIÓN DINÁMICA DE COLUMNAS ---
        # Al usar stretch=True, las columnas se repartirán el ancho de la pantalla
        self.tabla.column("Nit", width=100, anchor="center", stretch=True)
        self.tabla.column("Nombre", width=150, anchor="w", stretch=True)
        self.tabla.column("Apellido", width=150, anchor="w", stretch=True)
        self.tabla.column("Sexo", width=80, anchor="center", stretch=True)
        self.tabla.column("Telefono", width=120, anchor="center", stretch=True)
        self.tabla.column("Password", width=120, anchor="center", stretch=True)
        self.tabla.column("Acciones", width=150, anchor="center", stretch=True)

        # Cabeceras
        for col in columnas:
            self.tabla.heading(col, text=col.upper())

        # Empaquetado
        self.scroll_y.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)
        
        
        
        # style = ttk.Style()
        # style.theme_use("clam")
        
        # style.configure("Treeview", 
        #                  background="#1A1A1E", 
        #                   foreground="white", 
        #                    fieldbackground="#1A1A1E", 
        #                     rowheight=35, 
        #                      font=("Segoe UI", 10))
        
        # style.configure("Treeview.Heading", 
        #                  background="#6745B8", 
        #                   foreground="white", 
        #                    relief="flat",
        #                     font=("Segoe UI", 10, "bold"))
        
        # style.map("Treeview", background=[('selected', '#53339E')])

        # # # --- CONTENEDOR ---
        # self.contenedor_tabla = tk.Frame(self.ventana, bg="#1A1A1E", pady=20)
        # self.contenedor_tabla.pack(fill="x", expand=True)

        # # --- CREACIÓN DEL TREEVIEW ---
        # # Asegúrate de que estos nombres coincidan con los de abajo
        # self.columnas = ("Nit", "Nombre", "Apellido", "Sexo", "Telefono", "Password", "Acciones")
        
        # self.tabla = ttk.Treeview(self.contenedor_tabla, 
        #                           columns=self.columnas, 
        #                           show="headings", 
        #                           height=12)

        # # Scrollbar
        # self.scroll_y = ttk.Scrollbar(self.contenedor_tabla, orient="vertical", command=self.tabla.yview)
        # self.tabla.configure(yscrollcommand=self.scroll_y.set)

        # # --- CONFIGURACIÓN DE COLUMNAS (CORREGIDO) ---
        # # Los nombres deben ser idénticos a los de la tupla self.columnas
        # self.tabla.column("Nit", width=100, anchor="center")
        # self.tabla.column("Nombre", width=120)
        # self.tabla.column("Apellido", width=120)
        # self.tabla.column("Sexo", width=80, anchor="center")
        # self.tabla.column("Telefono", width=120, anchor="center")
        # self.tabla.column("Password", width=100, anchor="center")
        # self.tabla.column("Acciones", width=100, anchor="center")

        # # Cabeceras
        # self.tabla.heading("Nit", text="NIT / ID")
        # self.tabla.heading("Nombre", text="NOMBRE")
        # self.tabla.heading("Apellido", text="APELLIDO")
        # self.tabla.heading("Sexo", text="SEXO")
        # self.tabla.heading("Telefono", text="TELÉFONO")
        # self.tabla.heading("Password", text="CONTRASEÑA")
        # self.tabla.heading("Acciones", text="ACCIONES")

        # # Empaquetado
        # self.tabla.pack(side="left")
        # self.scroll_y.pack(side="right", fill="y")







    def cargar_datos_tabla(self):
        # 1. Obtener el diccionario (NIT como llave)
        data = LoginController.obtener_usuarios()
        
        # 2. Limpiar la tabla para evitar duplicados
        for row in self.vista.tabla.get_children():
            self.vista.tabla.delete(row)
    
        # 3. Validar si data tiene contenido
        if not data:
            print("DEBUG: El diccionario 'data' está vacío.")
            return
    
        # 4. Iterar usando el NIT como llave primaria
        for nit, info in data.items():
            # Limpiamos el valor del rol para comparar correctamente
            rol_usuario = str(info.get('rol', '')).strip().lower()
            
            if rol_usuario == 'administrador':
                self.vista.tabla.insert("", "end", values=(
                    nit,                           # Nuestra Llave Primaria
                    info.get('nombre', 'N/A'),
                    info.get('apellido', 'N/A'),
                    info.get('sexo', 'N/A'),
                    info.get('telefono', 'N/A'),
                    "********",                    # No mostramos la clave
                    "  ✎ Modificar  |  🗑 Borrar  "
                ))