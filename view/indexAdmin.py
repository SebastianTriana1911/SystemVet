import tkinter as tk

class IndexVentanaAdmin():
    def __init__(self, datos_usuario):
        self.datos_usuario = datos_usuario

        # ----------- CONFIGURACION DE LA VENTANA -----------
        self.ventana = tk.Tk()
        self.ventana.geometry("620x460+470+160") # Se inicializan la posicion y el tamaño de la ventana
        self.ventana.minsize(620,460) # Se maneja un minimo de px para la ventana
        self.ventana.maxsize(620,460) # Se maneja un maximo de px para la ventana
        self.ventana.title("SystemVet / Home Administrador") # Titulo de la self.ventana
        self.ventana.config(bg="white", bd=12) # El color de la ventana sera blanco
        # ----------------------------------------------------

        # ----------- CONFIGURACION DEL ENCABEZADO ----------- 
        header = tk.Frame(self.ventana, bg="#2b8ee6")
        header.pack(side="top", fill="x") # Se muestra en la ventana
   
        if datos_usuario["sexo"] == "Masculino":
            avatar = "image/avatar_masculino.png"
        else:
            avatar = "image/avatar_femenino.png"

        # Cargar la imagen original
        img_original = tk.PhotoImage(file=avatar)

        # Redimensionar usando subsample
        self.imageAvatar = img_original.subsample(3, 3) 

        # El Label debe coincidir con el tamaño resultante
        imageAvatar = tk.Label(header, bg="#2b8ee6", image=self.imageAvatar, width=32, height=32)
        imageAvatar.pack(side="right", padx=(10, 10))

        tk.Label(header, text=f"{datos_usuario["nombre"]} | Admin", bg="#2b8ee6", fg="white", 
                font=("Aharoni", 14, "bold"), pady=15).pack(side="right")
        
        tk.Label(header, text="SystemVet", bg="#2b8ee6", fg="white", 
                font=("Aharoni", 14, "bold"), ).pack(side="left", padx=(10,10))
        # ----------------------------------------------------

        # ------------- CONFIGURACION DEL CUERPO ------------- 
        cuerpo = tk.Frame(self.ventana, bg="white")
        cuerpo.pack(fill="both", expand=True) # El cuerpo es "infinito" hacia abajo

        # --- CONFIGURACION TITULO ---
        tk.Label(cuerpo, text="Escritorio", bg="white", fg="black", 
                 font=("Aharoni", 14, "bold")).pack(side="top", anchor="w", padx=10, pady=(15, 0))

        linea = tk.Frame(cuerpo, bg="#e1e1e1", height=2)
        linea.pack(fill="x", padx=10, pady=(5, 20))

        # --- CONFIGURACION OPCIONES ---
        # Cambiamos a side="top" para que siga el flujo natural debajo de la línea
        # Usamos fill="both" y expand=True para que el fondo rojo sea visible
        panel_opciones = tk.Frame(cuerpo, bg="white")
        panel_opciones.pack(side="top", fill="both", expand=True, padx=10)

        # Configuracion de columnas para los botones
        for i in range(2): 
                panel_opciones.columnconfigure(i, weight=100, uniform="col")
        
        self.imageAdministrador = tk.PhotoImage(file="image/avatar_administrador.png", width=90, height=90) # Acceder a la imagen
        self.imageAdministrador = self.imageAdministrador.subsample(1, 1) 

        btn_administrador = tk.Button(panel_opciones, 
                                        text="Admins", 
                                        bg="#8dbb5e",      # Color verde de la imagen
                                        fg="white",
                                        image= self.imageAdministrador,
                                        font=("Aharoni", 10, "bold"),
                                        compound="top",         # Imagen ARRIBA del texto
                                        width=100,              # Ancho fijo para hacerlo cuadrado
                                        height=100,             # Alto fijo
                                        borderwidth=0,
                                        pady=8
                                        )
        btn_administrador.grid(row=0, column=0, ipadx=5, ipady=5)


        self.imageMedico = tk.PhotoImage(file="image/avatar_medico.png", width=100, height=100) # Acceder a la imagen
        self.imageMedico = self.imageMedico.subsample(1, 1) 

        btn_medico = tk.Button(panel_opciones, 
                                        text="Medicos", 
                                        bg="#6C3CDD",      # Color verde de la imagen
                                        fg="white",
                                        image= self.imageMedico,
                                        font=("Aharoni", 10, "bold"),
                                        compound="top",         # Imagen ARRIBA del texto
                                        width=130,              # Ancho fijo para hacerlo cuadrado
                                        height=130,             # Alto fijo
                                        borderwidth=5,
                                        pady=5     
                                        )
        btn_medico.grid(row=0, column=1, pady=5, ipadx=5, ipady=5)

        
        # -----------------------------------------------------


        # tk.Label(cuerpo, text="Gestion de información", bg="white", fg="black", bd=30, 
        #         font=("Ahoroni", 15, "bold")).pack()


        # opcion_administrador = tk.Frame(cuerpo, bg="white")
        # opcion_administrador.pack(side="left", padx=(30,50))
        
        # tk.Label(opcion_administrador, text="Administradores", bg="white", fg="black",
        #         font=("Ahoroni", 13)).pack()
        
        # self.imageAvatarAdministrador = tk.PhotoImage(file="image/avatar_administrador.png") # Acceder a la imagen
        # imageAvatar = tk.Label(opcion_administrador, bg="white", image=self.imageAvatarAdministrador, 
        #                         width=100, height=100)
        # imageAvatar.pack()

        # self.btn_adm = tk.Button(opcion_administrador, text="INGRESAR", bg="#67b68a", fg="white",
        #                           width=10, font=("Aharoni", 13, "bold"), ) # Al hacer click, el boton llama al metodo
        # self.btn_adm.pack()
        

        # opcion_medico = tk.Frame(cuerpo, bg="white")
        # opcion_medico.pack(side="left", padx=30)
        
        # tk.Label(opcion_medico, text="Medicos", bg="white", fg="black",
        #         font=("Ahoroni", 13)).pack()
        
        # self.imageAvatarMedico = tk.PhotoImage(file="image/avatar_medico.png") # Acceder a la imagen
        # imageAvatarM = tk.Label(opcion_medico, bg="white", image=self.imageAvatarMedico, 
        #                         width=100, height=100)
        # imageAvatarM.pack()

        # self.btn_med = tk.Button(opcion_medico, text="INGRESAR", bg="#67b68a", fg="white",
        #                           width=10, font=("Aharoni", 13, "bold"), ) # Al hacer click, el boton llama al metodo
        # self.btn_med.pack()


        # opcion_reporte = tk.Frame(cuerpo, bg="white")
        # opcion_reporte.pack(side="left", padx=30)
        
        # tk.Label(opcion_reporte, text="Reportes", bg="white", fg="black",
        #         font=("Ahoroni", 13)).pack()
        
        # self.imageReporte = tk.PhotoImage(file="image/reporte.png") # Acceder a la imagen
        # imageR = tk.Label(opcion_reporte, bg="white", image=self.imageReporte, 
        #                         width=130, height=100)
        # imageR.pack()

        # self.btn_rep = tk.Button(opcion_reporte, text="INGRESAR", bg="#67b68a", fg="white",
        #                           width=10, font=("Aharoni", 13, "bold"), ) # Al hacer click, el boton llama al metodo
        # self.btn_rep.pack()
