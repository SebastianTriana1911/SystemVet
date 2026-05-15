import customtkinter as ctk
from backend.admin.gestion_admin_controller import *
from backend.admin.home_controller import *
import tkinter as tk
class HomeVentana():
    def __init__(self, datos_usuario):
        self.datos_usuario = datos_usuario

        # ----------- CONFIGURACION DE LA VENTANA -----------
        self.ventana = ctk.CTk()
        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico") # Se muesta en ventana un icono
        self.ventana.title("SystemVet / Gestión de Administradores")
        self.ventana.configure(bg="black", bd=10)
        # ----------------------------------------------------

        # ----------- CONFIGURACION DEL ENCABEZADO -----------
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
                                                    command= lambda:GestionAdminController.cerrar_sesion(self.ventana) # Cambia el cursor al pasar por encima
                                           )
        self.btn_cerrar_sesion.pack(side="left")
        # ----------------------------------------------------

        # ------------- CONFIGURACION DEL CUERPO -------------
        cuerpo = tk.Frame(self.ventana, bg="#242424")
        cuerpo.pack(fill="both", expand=True, padx=55, pady=30)

        tk.Label(cuerpo, text="Gestión de información", bg="#242424", fg="white",
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")

        tk.Label(cuerpo,
                 text="Seleccione un módulo para administrar el personal y revisar las estadísticas clínicas.\n"
                      "Asegúrese de mantener los registros actualizados.",
                 bg="#242424", fg="#9090a8", font=("Segoe UI", 12), justify="left").pack(anchor="w", pady=(5, 0))

        # --- Contenedor de las tres opciones ---
        opciones = tk.Frame(cuerpo, bg="#242424")
        opciones.pack(fill="both", expand=True, pady=(28, 0))
        opciones.columnconfigure(0, weight=1, uniform="col")
        opciones.columnconfigure(1, weight=1, uniform="col")
        opciones.columnconfigure(2, weight=1, uniform="col")

        #opciones.rowconfigure(0, weight=1)
        

        # ── ADMINISTRADORES ──────────────────────────────────────────────────
        borde_adm = tk.Frame(opciones, bg="#242424", padx=1, pady=1)
        borde_adm.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        opcion_administrador = tk.Frame(borde_adm, bg="#1a1a1f", padx=20, pady=200)
        opcion_administrador.pack(fill="both", expand=True)

        self.imageAvatarAdministrador = tk.PhotoImage(file="image/avatar_administrador.png")
        tk.Label(opcion_administrador, bg="#1a1a1f", image=self.imageAvatarAdministrador,
                 width=72, height=72).pack()

        tk.Label(opcion_administrador, text="Administradores", bg="#1a1a1f", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))

        tk.Label(opcion_administrador,
                 text="Gestione cuentas con acceso total al sistema, "
                      "configuraciones de la clínica y permisos de seguridad del personal.",
                 bg="#1a1a1f", fg="#9090a8", font=("Segoe UI",10),
                 justify="center", wraplength=230).pack(pady=(8, 20))

        self.btn_adm = tk.Button(opcion_administrador, text="INGRESAR  →", bg="#7c3aed", fg="white",
                                 font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                                 activebackground="#6d28d9", activeforeground="white",
                                 padx=10, pady=10, bd=0, command=lambda:HomeController(self.ventana, datos_usuario))
        self.btn_adm.pack(fill="x")

        # ── MÉDICOS ──────────────────────────────────────────────────────────
        borde_med = tk.Frame(opciones, bg="#2a2a35", padx=1, pady=1)
        borde_med.grid(row=0, column=1, sticky="nsew", padx=(0, 14))

        opcion_medico = tk.Frame(borde_med, bg="#1a1a1f", padx=24, pady=200)
        opcion_medico.pack(fill="both", expand=True)

        self.imageAvatarMedico = tk.PhotoImage(file="image/avatar_medico.png")
        tk.Label(opcion_medico, bg="#1a1a1f", image=self.imageAvatarMedico,
                 width=72, height=72).pack()

        tk.Label(opcion_medico, text="Médicos", bg="#1a1a1f", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))

        tk.Label(opcion_medico,
                 text="Administre el personal veterinario, horarios, "
                      "especialidades clínicas y asignaciones de pacientes en curso.",
                 bg="#1a1a1f", fg="#9090a8", font=("Segoe UI", 10),
                 justify="center", wraplength=230).pack(pady=(8, 20))

        self.btn_med = tk.Button(opcion_medico, text="INGRESAR  →", bg="#7c3aed", fg="white",
                                 font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                                 activebackground="#6d28d9", activeforeground="white",
                                 padx=10, pady=10, bd=0)
        self.btn_med.pack(fill="x")

        # ── REPORTES ─────────────────────────────────────────────────────────
        borde_rep = tk.Frame(opciones, bg="#2a2a35", padx=1, pady=1)
        borde_rep.grid(row=0, column=2, sticky="nsew")

        opcion_reporte = tk.Frame(borde_rep, bg="#1a1a1f", padx=24, pady=200)
        opcion_reporte.pack(fill="both", expand=True)

        self.imageReporte = tk.PhotoImage(file="image/reporte.png")
        tk.Label(opcion_reporte, bg="#1a1a1f", image=self.imageReporte,
                 width=62, height=70).pack()

        tk.Label(opcion_reporte, text="Reportes", bg="#1a1a1f", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))

        tk.Label(opcion_reporte,
                 text="Visualice análisis clínicos, estadísticas financieras y "
                      "rendimiento de la clínica mediante gráficos interactivos.",
                 bg="#1a1a1f", fg="#9090a8", font=("Segoe UI", 10),
                 justify="center", wraplength=230).pack(pady=(8, 20))

        self.btn_rep = tk.Button(opcion_reporte, text="INGRESAR  →", bg="#7c3aed", fg="white",
                                 font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                                 activebackground="#6d28d9", activeforeground="white",
                                 padx=10, pady=10, bd=0)
        self.btn_rep.pack(fill="x")
        # ----------------------------------------------------


if __name__ == "__main__":
    # Datos de prueba para poder visualizar la ventana
    datos_prueba = {"nombre": "Admin", "sexo": "Masculino"}
    app = HomeVentana(datos_prueba)
    app.ventana.mainloop()
