import customtkinter as ctk
from backend.admin.home_controller import *
# from backend.admin.gestion_admin_controller import *
import tkinter as tk
class HomeVentana():
    def __init__(self, datos_usuario):
        self.datos_usuario = datos_usuario
        


        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DE LA VENTANA ─────────────────────────────────────────────────────
        # ========================================================================================================
        self.ventana = ctk.CTk()
        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico") # Se muesta en ventana un icono
        self.ventana.title("SystemVet - Gestión de Administradores")
        self.ventana.configure(bg="black", bd=0)


        self.ventana.after(0, lambda: self.ventana.state('zoomed'))
        # ----------------------------------------------------



        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DEL ENCABEZADO ────────────────────────────────────────────────────
        # ========================================================================================================
        self.header = tk.Frame(self.ventana,
                                bg="#45A29E")
        self.header.pack(side="top",
                          fill="x", ipady=2) # Mantiene el 100% del ancho en la pantalla
        
        self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2) # Acceder a la imagen
        image_logo = self.image_logo
        image_logo = tk.Label(self.header,
                                  bg="#45A29E",
                                  width=70,
                                  height=70,
                                  image=self.image_logo)
        image_logo.image = self.image_logo
        image_logo.pack(side="left", padx=20, pady=10)

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

        # Titulo inferior (HOME DE ADMINISTRADORES)
        tk.Label(self.contenedor_titulo_header,
                text="HOME ADMINISTRADOR",
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
        
        # Nombre del usuario en la parte izquierda
        tk.Label(self.container_usuario,
                   text=f"{datos_usuario['nombre']} {datos_usuario["apellido"]}",
                    bg="#45A29E",
                     fg="white", 
                      font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")
        
        # Contenedor que organiza el nombre del usuario y el boton de manera horizontal
        self.fila_nombre = tk.Frame(self.container_usuario,
                                     bg="#45A29E")
        self.fila_nombre.pack(side="top", anchor="e")
        

        # Etiqueta "Administrador" parte superior
        if datos_usuario["sexo"] == "Masculino":
            tk.Label(self.fila_nombre,
                     text="Administrador",
                     bg="#45A29E",
                     fg="white",
                     font=("Segoe UI", 13)).pack(side="left", padx=(0, 5))
        else:
            tk.Label(self.fila_nombre,
                     text="Administradora",
                     bg="#45A29E",
                     fg="white",
                     font=("Segoe UI", 13)).pack(side="left", padx=(0, 5))
        
        
        # Botón Cerrar Sesión (Al lado del nombre)
        self.btn_cerrar_sesion = tk.Button(self.fila_nombre, 
                                            text="|  Cerrar sesión", 
                                            bg="#45A29E", 
                                            fg="white",
                                            font=("Segoe UI", 12, "bold"),                                                  
                                            borderwidth=0,
                                            cursor="hand2",
                                            command= lambda:GestionAdminController.cerrar_sesion(self.ventana) # Cambia el cursor al pasar por encima
                                           )
        self.btn_cerrar_sesion.pack(side="left")
        # ----------------------------------------------------



        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DEL CUERPO ───────────────────────────────────────────────────────
        # ========================================================================================================


        cuerpo = tk.Frame(self.ventana, bg="#1A1A1E")
        cuerpo.pack(fill="both", expand=True, ipadx=155, ipady=30) # padx=155, pady=30

        tk.Label(cuerpo, text="Gestión de información", bg="#1A1A1E", fg="#45A29E",
                 font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=155, pady=(30,10))

        tk.Label(cuerpo,
                 text="Seleccione un módulo para administrar el personal y revisar las estadísticas clínicas.\n"
                      "Asegúrese de mantener los registros actualizados.",
                 bg="#1A1A1E", fg="white", font=("Segoe UI", 12), justify="left").pack(anchor="w", padx=155, pady=(0, 25))

        # --- Contenedor de las tres opciones ---
        opciones = tk.Frame(cuerpo, bg="#1A1A1E")
        opciones.pack(fill="both", expand=True, pady=(28, 0), padx=155)
        opciones.columnconfigure(0, weight=1, uniform="col")
        opciones.columnconfigure(1, weight=1, uniform="col")
        opciones.columnconfigure(2, weight=1, uniform="col")

        #opciones.rowconfigure(0, weight=1)
        

        # ========================================================================================================
        # ────────────────────── ADMINISTRADORES ──────────────────────────────────────────────────
        # ========================================================================================================

        #borde_adm = tk.Frame(opciones, bg="#242424", padx=1, pady=1)
        borde_adm = ctk.CTkFrame(opciones, 
                                fg_color="#242429", 
                                corner_radius=20,
                                border_width=2, 
                                border_color="#7C7C7C"
                                )
        borde_adm.grid(row=0, 
                        column=0,
                            sticky="new", 
                            padx=(0, 14))

        opcion_administrador = ctk.CTkFrame(borde_adm, 
                                          fg_color="#242429")
        opcion_administrador.pack(fill="both", expand=False, padx=20, pady=80)

        self.imageAvatarAdministrador = tk.PhotoImage(file="image/avatar_administrador.png")
        tk.Label(opcion_administrador, bg="#242429", image=self.imageAvatarAdministrador,
                 width=72, height=72).pack()

        tk.Label(opcion_administrador, text="Administradores", bg="#242429", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))

        tk.Label(opcion_administrador,
                 text="En este apartado podra gestionar usuarios con permisos de administracion para acceder al sistema.",
                 bg="#242429", fg="white", font=("Segoe UI",11),
                 justify="center", wraplength=300).pack(pady=(8, 40))

        self.btn_adm = ctk.CTkButton(opcion_administrador,
                                 text="INGRESAR  →",
                                 fg_color="#45A29E", text_color="white",
                                 font=("Segoe UI", 13, "bold"),
                                 hover_color="#2D7773",
                                 width=150, 
                                 height=55, 
                                 corner_radius=10,
                                 command=lambda:HomeController(self.ventana, datos_usuario, "Admin"))
        self.btn_adm.pack(pady=20)


        # ========================================================================================================
        # ────────────────────── MÉDICOS ─────────────────────────────────────────────────────────────────────────
        # ========================================================================================================


        borde_med = ctk.CTkFrame(opciones, 
                                fg_color="#242429", 
                                corner_radius=20,
                                border_width=2, 
                                border_color="#7C7C7C" 
                                
                                )
        #borde_med = tk.Frame(opciones, bg="#1a1a1f", padx=1, pady=1)
        borde_med.grid(row=0, 
                        column=1, 
                        sticky="new", 
                        padx=(0, 14))

        opcion_medico = ctk.CTkFrame(borde_med, 
                                    fg_color="#242429", 
                                    width=24, 
                                    height=200
                                    )
        opcion_medico.pack(fill="both", expand=False, pady=80, padx=20)

        self.imageAvatarMedico = tk.PhotoImage(file="image/avatar_medico.png")
        tk.Label(opcion_medico, bg="#242429", image=self.imageAvatarMedico,
                 width=82, height=72).pack()

        tk.Label(opcion_medico, text="Médicos", bg="#242429", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))

        tk.Label(opcion_medico,
                 text="Administre el personal veterinario, horarios, "
                      "especialidades clínicas y asignaciones de pacientes en curso.",
                 bg="#242429", fg="white", font=("Segoe UI", 11),
                 justify="center", wraplength=300).pack(pady=(8,40))

        self.btn_med = ctk.CTkButton(opcion_medico, text="INGRESAR  →", 
                                 fg_color="#45A29E", 
                                 font=("Segoe UI", 13, "bold"), 
                                 width=150, 
                                 height=55, 
                                 corner_radius=10,
                                 hover_color="#2D7773", 
                                 text_color="white",
                                 cursor="hand2",
                                 command=lambda:HomeController(self.ventana, datos_usuario, "Medico")
                                 )
        self.btn_med.pack(pady=20)

        # ========================================================================================================
        # ────────────────────── REPORTES ────────────────────────────────────────────────────────────────────────
        # ========================================================================================================


        #borde_rep = tk.Frame(opciones, bg="#2a2a35", padx=1, pady=1)
        borde_rep = ctk.CTkFrame(opciones,
                                fg_color="#242429",
                                corner_radius=20, 
                                border_width=2, 
                                border_color="#7C7C7C")
        borde_rep.grid(row=0, column=2, sticky="new",padx=(0, 14))

        opcion_reporte = ctk.CTkFrame(borde_rep,
                                        fg_color="#242429")
        opcion_reporte.pack(fill="both",
                                expand=False,
                                padx=24,
                                pady=80)

        self.imageReporte = tk.PhotoImage(file="image/reporte.png")
        tk.Label(opcion_reporte, 
                        bg="#242429",
                         image=self.imageReporte,
                            width=72, height=76).pack()

        tk.Label(opcion_reporte, text="Reportes", bg="#242429", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))

        tk.Label(opcion_reporte,
                 text="Visualice análisis clínicos, estadísticas financieras y "
                      "rendimiento de la clínica mediante gráficos interactivos.",
                 bg="#242429", fg="white", font=("Segoe UI", 11),
                 justify="center", wraplength=300).pack(pady=(8, 35))

        self.btn_rep = ctk.CTkButton(opcion_reporte, text="INGRESAR  →",
                                 fg_color="#45A29E", text_color="white",
                                 font=("Segoe UI", 13, "bold"), 
                                 width=150,
                                 height=55,
                                 hover_color="#2D7773", 
                                 cursor="hand2",
                                 corner_radius=10)
        self.btn_rep.pack(pady=20)

        # ----------------------------------------------------

        self.ventana.mainloop()
