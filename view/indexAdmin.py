import tkinter as tk

class IndexVentanaAdmin():
    def __init__(self, datos_usuario):
        self.datos_usuario = datos_usuario

        # ----------- CONFIGURACION DE LA VENTANA -----------
        self.ventana = tk.Tk()
        self.ventana.geometry("620x460+470+160") # Se inicializan la posicion y el tamaño de la ventana
        self.ventana.minsize(620,460) # Se maneja un minimo de px para la ventana
        self.ventana.maxsize(620,460) # Se maneja un maximo de px para la ventana
        self.ventana.title("Sistema Veterinaria - Home Administrador") # Titulo de la self.ventana
        self.ventana.config(bg="white", bd=5) # El color de la ventana sera blanco
        # ----------------------------------------------------

        # ----------- CONFIGURACION DEL ENCABEZADO ----------- 
        header = tk.Frame(self.ventana, bg="#00539c")
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
        imageAvatar = tk.Label(header, bg="#00539c", image=self.imageAvatar, width=32, height=32)
        imageAvatar.pack(side="right", padx=(10, 10))

        tk.Label(header, text=f"{datos_usuario["nombre"]} | Admin", bg="#00539c", fg="white", 
                font=("Aharoni", 14, "bold"), pady=15).pack(side="right")
        
        tk.Label(header, text="Panel de control", bg="#00539c", fg="white", 
                font=("Aharoni", 14, "bold"), ).pack(side="left", padx=(10,10))
        # ----------------------------------------------------

        # ------------- CONFIGURACION DEL CUERPO ------------- 
        cuerpo = tk.Frame(self.ventana, bg="white") # Contenedor de los elementos contenidos en el cuerpo
        cuerpo.pack()

        tk.Label(cuerpo, text="Gestion de información", bg="white", fg="black", bd=30, 
                font=("Ahoroni", 15, "bold")).pack()


        opcion_administrador = tk.Frame(cuerpo, bg="white")
        opcion_administrador.pack(side="left", padx=(30,50))
        
        tk.Label(opcion_administrador, text="Administradores", bg="white", fg="black",
                font=("Ahoroni", 13)).pack()
        
        self.imageAvatarAdministrador = tk.PhotoImage(file="image/avatar_administrador.png") # Acceder a la imagen
        imageAvatar = tk.Label(opcion_administrador, bg="white", image=self.imageAvatarAdministrador, 
                                width=100, height=100)
        imageAvatar.pack()

        self.btn_adm = tk.Button(opcion_administrador, text="INGRESAR", bg="#67b68a", fg="white",
                                  width=10, font=("Aharoni", 13, "bold"), ) # Al hacer click, el boton llama al metodo
        self.btn_adm.pack()
        

        opcion_medico = tk.Frame(cuerpo, bg="white")
        opcion_medico.pack(side="left", padx=30)
        
        tk.Label(opcion_medico, text="Medicos", bg="white", fg="black",
                font=("Ahoroni", 13)).pack()
        
        self.imageAvatarMedico = tk.PhotoImage(file="image/avatar_medico.png") # Acceder a la imagen
        imageAvatarM = tk.Label(opcion_medico, bg="white", image=self.imageAvatarMedico, 
                                width=100, height=100)
        imageAvatarM.pack()

        self.btn_med = tk.Button(opcion_medico, text="INGRESAR", bg="#67b68a", fg="white",
                                  width=10, font=("Aharoni", 13, "bold"), ) # Al hacer click, el boton llama al metodo
        self.btn_med.pack()


        opcion_reporte = tk.Frame(cuerpo, bg="white")
        opcion_reporte.pack(side="left", padx=30)
        
        tk.Label(opcion_reporte, text="Reportes", bg="white", fg="black",
                font=("Ahoroni", 13)).pack()
        
        self.imageReporte = tk.PhotoImage(file="image/reporte.png") # Acceder a la imagen
        imageR = tk.Label(opcion_reporte, bg="white", image=self.imageReporte, 
                                width=130, height=100)
        imageR.pack()

        self.btn_rep = tk.Button(opcion_reporte, text="INGRESAR", bg="#67b68a", fg="white",
                                  width=10, font=("Aharoni", 13, "bold"), ) # Al hacer click, el boton llama al metodo
        self.btn_rep.pack()
