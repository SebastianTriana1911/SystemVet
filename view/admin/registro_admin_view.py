import customtkinter as ctk

class RegistroAdminView(ctk.CTkToplevel):
    def __init__(self, ventana_padre):
        super().__init__(ventana_padre)
        self.ventana_padre = ventana_padre
        
        # 1. Configuración de la ventana emergente
        ctk.set_appearance_mode("dark")
        self.title("SystemVet - Formulario Nuevo Administrador")

        # 1. Obtener las dimensiones de la pantalla
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()

        self.update_idletasks() 
        ancho = 600
        alto = 500

        # 2. Calcular las coordenadas X e Y
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)

        # 3. Aplicar la geometría
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        self.configure(fg_color="#1A1A1E")
        # self.ventana.after(0, lambda: self.ventana.state('zoomed'))
        self.resizable(False, False)
        
        # 2. 🌟 EFECTO DE OPACIDAD: Volvemos semitransparente la ventana de atrás
        self.ventana_padre.attributes("-alpha", 0.9)
        
        # 3. Forzar el foco en esta ventana (Modal)
        self.grab_set()
        self.focus_set()
        
        # 4. Asegurar que si cierran la ventana desde la 'X', la de atrás vuelva a la normalidad
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)
        
        # Aquí construirías el diseño (los inputs, labels y botones del formulario)
        self.crear_componentes()
        
    def crear_componentes(self):
        # --- BANNER SUPERIOR DE TÍTULO ---
        self.banner_titulo = ctk.CTkFrame(self, fg_color="#45A29E", corner_radius=10, height=70)
        self.banner_titulo.pack(fill="x", padx=40, pady=(30, 20))
        self.banner_titulo.pack_propagate(False) # Evita que el frame se encoja

        self.label_titulo = ctk.CTkLabel(
            self.banner_titulo, 
            text="➕  REGISTRAR NUEVO ADMINISTRADOR", 
            font=("Segoe UI", 16, "bold"), 
            text_color="white"
        )
        self.label_titulo.pack(expand=True)

        # --- TARJETA CONTENEDORA DEL FORMULARIO ---
        self.card_formulario = ctk.CTkFrame(self, fg_color="#242429", corner_radius=15)
        self.card_formulario.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        # Configuración de las columnas del Grid para que se distribuyan equitativamente
        self.card_formulario.columnconfigure(0, weight=1)
        self.card_formulario.columnconfigure(1, weight=1)

        # FUENTE COMÚN PARA LOS LABELS
        fuente_labels = ("Segoe UI", 12, "bold")

        # =====================================================================
        # FILA 1: NIT (Izquierda) y NOMBRE (Derecha)
        # =====================================================================
        # NIT
        self.lbl_nit = ctk.CTkLabel(self.card_formulario, text="Nit / CC:", font=fuente_labels, text_color="white")
        self.lbl_nit.grid(row=0, column=0, padx=25, pady=(20, 2), sticky="w")
        
        self.txt_nit = ctk.CTkEntry(self.card_formulario, placeholder_text=" 🆔  Número de documento", 
                                    fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.txt_nit.grid(row=1, column=0, padx=25, pady=(0, 15), sticky="we")

        # NOMBRE
        self.lbl_nombre = ctk.CTkLabel(self.card_formulario, text="Nombre:", font=fuente_labels, text_color="white")
        self.lbl_nombre.grid(row=0, column=1, padx=25, pady=(20, 2), sticky="w")
        
        self.txt_nombre = ctk.CTkEntry(self.card_formulario, placeholder_text=" 👤  Nombres completos", 
                                       fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.txt_nombre.grid(row=1, column=1, padx=25, pady=(0, 15), sticky="we")

        # =====================================================================
        # FILA 2: APELLIDO (Izquierda) y SEXO (Derecha)
        # =====================================================================
        # APELLIDO
        self.lbl_apellido = ctk.CTkLabel(self.card_formulario, text="Apellido:", font=fuente_labels, text_color="white")
        self.lbl_apellido.grid(row=2, column=0, padx=25, pady=(0, 2), sticky="w")
        
        self.txt_apellido = ctk.CTkEntry(self.card_formulario, placeholder_text=" 👤  Apellidos completos", 
                                         fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.grid_apellido = self.txt_apellido.grid(row=3, column=0, padx=25, pady=(0, 15), sticky="we")

        # SEXO / GÉNERO (Usamos un ComboBox para obligar a seleccionar una opción válida)
        self.lbl_sexo = ctk.CTkLabel(self.card_formulario, text="Sexo / Género:", font=fuente_labels, text_color="white")
        self.lbl_sexo.grid(row=2, column=1, padx=25, pady=(0, 2), sticky="w")
        
        self.cb_sexo = ctk.CTkComboBox(self.card_formulario, values=["Masculino", "Femenino", "Otro"],
                                       fg_color="#1A1A1E", border_color="#45A29E", height=40, state="readonly")
        self.cb_sexo.set("Seleccione...") # Texto por defecto
        self.cb_sexo.grid(row=3, column=1, padx=25, pady=(0, 15), sticky="we")

        # =====================================================================
        # FILA 3: TELÉFONO (Izquierda) y PASSWORD (Derecha)
        # =====================================================================
        # TELÉFONO
        self.lbl_telefono = ctk.CTkLabel(self.card_formulario, text="Teléfono:", font=fuente_labels, text_color="white")
        self.lbl_telefono.grid(row=4, column=0, padx=25, pady=(0, 2), sticky="w")
        
        self.txt_telefono = ctk.CTkEntry(self.card_formulario, placeholder_text=" 📞  Celular o teléfono fijo", 
                                         fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.txt_telefono.grid(row=5, column=0, padx=25, pady=(0, 25), sticky="we")

        # PASSWORD
        self.lbl_password = ctk.CTkLabel(self.card_formulario, text="Contraseña:", font=fuente_labels, text_color="white")
        self.lbl_password.grid(row=4, column=1, padx=25, pady=(0, 2), sticky="w")
        
        self.txt_password = ctk.CTkEntry(self.card_formulario, placeholder_text=" 🔑  Asigne una contraseña", 
                                         fg_color="#1A1A1E", border_color="#45A29E", height=40, show="*")
        self.txt_password.grid(row=5, column=1, padx=25, pady=(0, 25), sticky="we")

        # =====================================================================
        # FILA 4: BOTÓN DE ACCIÓN PRINCIPAL (Ocupa las dos columnas abajo)
        # =====================================================================
        self.btn_registrar = ctk.CTkButton(
            self.card_formulario, 
            text="✔  CREAR ADMINISTRADOR", 
            font=("Segoe UI", 13, "bold"),
            fg_color="#45A29E", 
            hover_color="#31726F", 
            text_color="white",
            height=45, 
            corner_radius=10,
            command=self.ejecutar_registro # Vincularemos esto al controlador luego
        )
        self.btn_registrar.grid(row=6, column=0, columnspan=2, padx=25, pady=(0, 20), sticky="we")

        # --- BOTÓN INFERIOR DE REGRESAR ---
        self.btn_volver = ctk.CTkButton(
            self, 
            text="🡰  REGRESAR A GESTIÓN", 
            font=("Segoe UI", 11, "bold"),
            fg_color="#6745B8",          # El morado insignia de la cabecera
            hover_color="#513692", 
            text_color="white",
            width=180, 
            height=35, 
            corner_radius=8,
            command=self.al_cerrar
        )
        self.btn_volver.pack(side="right", padx=40, pady=(0, 20))

    def ejecutar_registro(self):
        # Este método servirá de puente para que el RegistroAdminController capture los datos
        pass

    def al_cerrar(self):
        # Al cerrar, devolvemos la opacidad total (1.0) a la ventana de gestión
        self.ventana_padre.attributes("-alpha", 1.0)
        self.destroy()