from tkinter import ttk
import customtkinter as ctk
import tkinter as tk
from backend.admin.gestion_admin_controller import *

class GestionAdminVentana:
    def __init__(self, ventana, datos_usuario):

        self.contador_total = tk.IntVar(value=0)
        self.contador_masculino = tk.IntVar(value=0)
        self.contador_femenino = tk.IntVar(value=0)

        # ==========================================================================
        # CONFIGURACION DE VENTANA
        # ==========================================================================
        self.ventana = ventana
        self.datos_usuario = datos_usuario

        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico") # Se muesta en ventana un icono
        self.ventana.title("SystemVet - Gestión de Administradores")
        self.ventana.configure(bd=10)
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


        # Contenedor titulos header
        self.contenedor_titulo_header = tk.Frame(self.header,
                                                bg="#45A29E")
        # Pegado a la izquierda del header
        self.contenedor_titulo_header.pack(side="left") 

        # Titulo superior (System Vet)
        tk.Label(self.contenedor_titulo_header,
                text="System Vet",
                fg="white", 
                bg="#45A29E", 
                font=("Segoe UI", 11, "bold")).pack(side="top", anchor="w") # anchor="w" alinea a la izquierda interna

        # Titulo inferior (GESTIÓN DE ADMINISTRADORES)
        tk.Label(self.contenedor_titulo_header,
                text="GESTIÓN DE ADMINISTRADORES",
                fg="white", 
                bg="#45A29E", 
                font=("Segoe UI", 15, "bold")).pack(side="top", anchor="w")         

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
                                            background="#1A1A1E",
                                            padx=80,
                                            pady=15)    
        self.contenedor_titulo.pack(fill="x")

        self.contenedor_titulo_separado = tk.Frame(self.contenedor_titulo,
                                                    bg="#1A1A1E")
        self.contenedor_titulo_separado.pack(side="left")

        # Título (PANEL DE CONTROL)
        tk.Label(self.contenedor_titulo_separado, 
                text="PANEL DE CONTRO",
                # textvariable= self.contador_masculino, 
                fg="#45A29E", 
                
                bg="#1A1A1E", 
                font=("Segoe UI", 15, "bold")).pack(side="top", anchor="w")

        # Título (Administradores registrados)
        tk.Label(self.contenedor_titulo_separado, 
                text="Administradores registrados", 
                fg="white", 
                bg="#1A1A1E", 
                font=("Segoe UI", 13, "bold")).pack(side="top", anchor="w")

        tk.Label(self.contenedor_titulo_separado, 
                text="En este apartado podras crear, editar o eliminar cuentas de acceso al sistema", 
                fg="white", 
                bg="#1A1A1E",  
                font=("Segoe UI", 13)).pack(side="top", anchor="w", pady=(12,0))


        # Contenedor (Registrar admin) y cards 
        self.contenedor_btn = tk.Frame(self.contenedor_titulo, bg="#1A1A1E")
        self.contenedor_btn.pack(side="right")

        # Fila de stat cards
        fila_stats = tk.Frame(self.contenedor_btn, bg="#1A1A1E",)
        fila_stats.pack(side="left")

        def crear_stat_card(parent, variable, etiqueta, color_num):

            card = ctk.CTkFrame(parent,
                    fg_color="#242427",
                    border_color="#45A29E",
                    border_width=1,
                    corner_radius=10)

            card.pack(side="left", pady=(10,0), padx=10)

            ctk.CTkLabel(card,
                         textvariable=variable,
                         text_color=color_num,
                         font=("Segoe UI", 20, "bold")).pack(padx=20, pady=(10, 2))

            ctk.CTkLabel(card,
                         text=etiqueta,
                         text_color="#FFFFFF",
                         font=("Segoe UI", 13, "bold")).pack(padx=20, pady=(0, 10))

        crear_stat_card(fila_stats, self.contador_total,     "Total",     "#79FAF3")
        crear_stat_card(fila_stats, self.contador_masculino, "Masculino", "#4DC7FF")
        crear_stat_card(fila_stats, self.contador_femenino,  "Femenino",  "#EE8AFF")

        # Botón registrar (text fijo, nunca textvariable)
        self.btn_crear_admin = ctk.CTkButton(
            self.contenedor_btn,
            text="+ Registrar Admin",          
            fg_color="#076BDF",
            text_color="white",
            hover_color="#002397",
            font=("Segoe UI", 14, "bold"),
            width=160,
            height=45,
            border_width=0,
            corner_radius=10,
            cursor="hand2",
            command=lambda: GestionAdminController.abrir_formulario_registro(self.ventana, self.controlador_admin)
        )
        self.btn_crear_admin.pack(anchor="e", pady=(25,0), padx=(15,0))

        # Línea divisora
        self.linea_divisor = tk.Frame(self.ventana, bg="#45A29E", height=2)
        self.linea_divisor.pack(fill="x")
        # ==========================================================================


        # ==========================================================================
        # CONFIGURACION DE LA TABLA ADMINS
        # ==========================================================================
        self.contenedor_cuerpo_tabla = tk.Frame(self.ventana, bg="#1A1A1E")
        self.contenedor_cuerpo_tabla.pack(fill="both", expand=True)

        # Cabecera de la tabla
        self.header_tabla = ctk.CTkFrame(self.contenedor_cuerpo_tabla,
                                        fg_color="#0A1520",
                                        # border_color="#45A29E",
                                        # border_width=2,
                                        # corner_radius=5,
                                        height=45) 
        self.header_tabla.pack(fill="x", pady=(30, 0), padx=200, )
        self.header_tabla.pack_propagate(False)

        COLS = [
            ("NIT",        0.01),
            ("NOMBRE",     0.10),
            ("APELLIDO",   0.23),
            ("SEXO",       0.36),
            ("TELÉFONO",   0.46),
            ("CONTRASEÑA", 0.58),
            ("ACCIONES",   0.74),
        ]

        # Configuracion para cada uno de los campos del encabezado
        for col_name, relx in COLS:
            tk.Label(self.header_tabla,
                     text=col_name,
                    #  fg="#45A29E",
                     fg="#FFFFFF",
                     bg="#0A1520",
                     font=("Segoe UI", 12, "bold")).place(relx=relx, rely=0.5, anchor="w")


        # Contenedor scrollable para las filas
        self.contenedor_tabla = ctk.CTkScrollableFrame(
            self.contenedor_cuerpo_tabla,
            fg_color="#2D2D31",
            # corner_radius=5,
            # border_color="#45A29E",
            # border_width=1,
            scrollbar_button_color="#DADADA",
            scrollbar_button_hover_color="#acacac"
        )
        self.contenedor_tabla.pack(fill="both", expand=True, padx=200, pady=(0, 40))
                
        # Esta instancia de la clase GestionAdminControler me permite acceder al metodo de cargar tabla
        self.controlador_admin = GestionAdminController(self)

        # Este atributo contiene toda la informacion de la tabla con los registro, por ender, despues de crear
        # un nuevo administrador en el formulario, se pasa este metodo, puesto que es el que permite cargar 
        # y mostrar nuevamente la tabla con todos los datos actualizados
        self.controlador_admin.cargar_datos_tabla()
        # ==========================================================================


    # ==========================================================================
    # METODO QUE DIBUJA UNA FILA EN LA TABLA CUSTOM
    # ==========================================================================
    def agregar_fila(self, nit, nombre, apellido, sexo, telefono):

        # Color de fondo según sexo e índice
        if sexo == "Masculino":
            color_fila = "#18314B" 
            # color_fila = "#1A2E42" if index % 2 == 0 else "#152538"
            color_badge_bg   = "#0D2137"
            color_badge_text = "#4FC3F7"
            icono_sexo       = "♂  Masc."
        else:
            color_fila = "#2A1A2E"
            # color_fila = "#2A1A2E" if index % 2 == 0 else "#221526"
            color_badge_bg   = "#581641"
            color_badge_text = "#F379A1"
            icono_sexo       = "♀  Fem."

        # Frame de la fila
        fila = ctk.CTkFrame(self.contenedor_tabla,
                            fg_color=color_fila,
                            corner_radius=8,
                            height=52)
        fila.pack(fill="x", padx=6, pady=3)
        fila.pack_propagate(False)

        # NIT
        ctk.CTkLabel(fila,
                     text=nit,
                     text_color="#FFFFFF",
                     font=("Consolas", 14, "bold")).place(relx=0.01, rely=0.5, anchor="w")

        # Nombre
        ctk.CTkLabel(fila,
                     text=nombre,
                     text_color="#FFFFFF",
                     font=("Segoe UI", 14, "bold")).place(relx=0.10, rely=0.5, anchor="w")

        # Apellido
        ctk.CTkLabel(fila,
                     text=apellido,
                     text_color="#FFFFFF",
                     font=("Segoe UI", 14, "bold")).place(relx=0.23, rely=0.5, anchor="w")

        # Badge de sexo
        badge = ctk.CTkFrame(fila,
                             fg_color=color_badge_bg,
                             corner_radius=10,
                             width=80,
                             height=30)
        badge.place(relx=0.36, rely=0.5, anchor="w")
        badge.pack_propagate(False)
        ctk.CTkLabel(badge,
                     text=icono_sexo,
                     text_color=color_badge_text,
                     font=("Segoe UI", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        # Teléfono
        ctk.CTkLabel(fila,
                     text=telefono,
                     text_color="#FFFFFF",
                     font=("Consolas", 14, "bold")).place(relx=0.47, rely=0.5, anchor="w")

        # Contraseña
        ctk.CTkLabel(fila,
                     text="● ● ● ● ● ● ● ●",
                     text_color="#FFFFFF",
                     font=("Segoe UI", 14, "bold")).place(relx=0.60, rely=0.5, anchor="w")

        # Botón Editar
        ctk.CTkButton(fila,
                    text="✎ Editar",
                    width=80,
                    height=30,
                    fg_color="#EC8600",
                    border_color="#EC8600",
                    border_width=1,
                    text_color="#000000",
                    hover_color="#C77100",
                    corner_radius=6,
                    cursor="hand2",
                    font=("Segoe UI", 14, "bold"),
                      command=lambda n=nit: self.controlador_admin.abrir_formulario_edicion(n)
                      ).place(relx=0.75, rely=0.5, anchor="w")

        # Botón Borrar
        ctk.CTkButton(fila,
                      text="🗑",
                      width=80,
                      height=30,
                      fg_color="#DD3434",
                      border_color="#DD3434",
                      border_width=1,
                      text_color="#FFFFFF",
                      hover_color="#4E0808",
                      corner_radius=6,
                      cursor="hand2",
                      font=("Segoe UI", 14, "bold"),
                      command=lambda n=nit, nm=nombre: self.controlador_admin.eliminar_administrador(n, nm)
                      ).place(relx=0.83, rely=0.5, anchor="w")
        # ==========================================================================
