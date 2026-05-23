import customtkinter as ctk
from backend.admin.registro_medico_controller import RegistroMedicoController

class RegistroMedicoView(ctk.CTkToplevel):
    def __init__(self, ventana_padre, controlador_gestion, nit_editar=None):
        super().__init__(ventana_padre)
        self.ventana_padre    = ventana_padre
        self.nit_editar       = nit_editar
        self.controlador_gestion  = controlador_gestion
        self.controlador_registro = RegistroMedicoController(self)

        # ==========================================================================
        # CONFIGURACION DE LA MODAL
        # ==========================================================================
        ctk.set_appearance_mode("dark")
        self.title("SystemVet - Formulario Médicos")

        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto  = self.winfo_screenheight()
        ancho, alto    = 600, 560
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto  // 2) - (alto  // 2)

        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.configure(fg_color="#1A1A1E")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        self.crear_componentes()

        if self.nit_editar:
            self.controlador_registro.cargar_datos_para_editar(self.nit_editar)
        # ==========================================================================


    # ==========================================================================
    # CREACION DE COMPONENTES
    # ==========================================================================
    def crear_componentes(self):
        texto_banner = "📝  ACTUALIZAR MÉDICO" if self.nit_editar else "➕  REGISTRAR NUEVO MÉDICO"
        texto_boton  = "✔ ACTUALIZAR DATOS"   if self.nit_editar else "✔  CREAR MÉDICO"

        # Banner superior
        self.banner_titulo = ctk.CTkFrame(self, fg_color="#45A29E",
                                          corner_radius=10, height=70)
        self.banner_titulo.pack(fill="x", padx=40, pady=(30, 20))
        self.banner_titulo.pack_propagate(False)

        ctk.CTkLabel(self.banner_titulo,
                     text=texto_banner,
                     font=("Segoe UI", 16, "bold"),
                     text_color="white").pack(expand=True)

        # Card del formulario
        self.card_formulario = ctk.CTkFrame(self, fg_color="#242429", corner_radius=15)
        self.card_formulario.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        self.card_formulario.columnconfigure(0, weight=1)
        self.card_formulario.columnconfigure(1, weight=1)

        fuente_labels = ("Segoe UI", 12, "bold")

        # ── FILA 1: NIT + NOMBRE ──────────────────────────────────────────────
        ctk.CTkLabel(self.card_formulario, text="Nit / CC:",
                     font=fuente_labels, text_color="white"
                     ).grid(row=0, column=0, padx=25, pady=(20, 2), sticky="w")

        self.txt_nit = ctk.CTkEntry(self.card_formulario,
                                    placeholder_text=" 🆔 Número de documento",
                                    fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.txt_nit.grid(row=1, column=0, padx=25, pady=(0, 15), sticky="we")

        ctk.CTkLabel(self.card_formulario, text="Nombre:",
                     font=fuente_labels, text_color="white"
                     ).grid(row=0, column=1, padx=25, pady=(20, 2), sticky="w")

        self.txt_nombre = ctk.CTkEntry(self.card_formulario,
                                       placeholder_text=" 👤 Nombres completos",
                                       fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.txt_nombre.grid(row=1, column=1, padx=25, pady=(0, 15), sticky="we")

        # ── FILA 2: APELLIDO + SEXO ───────────────────────────────────────────
        ctk.CTkLabel(self.card_formulario, text="Apellido:",
                     font=fuente_labels, text_color="white"
                     ).grid(row=2, column=0, padx=25, pady=(0, 2), sticky="w")

        self.txt_apellido = ctk.CTkEntry(self.card_formulario,
                                         placeholder_text=" 👤 Apellidos completos",
                                         fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.txt_apellido.grid(row=3, column=0, padx=25, pady=(0, 15), sticky="we")

        ctk.CTkLabel(self.card_formulario, text="Sexo / Género:",
                     font=fuente_labels, text_color="white"
                     ).grid(row=2, column=1, padx=25, pady=(0, 2), sticky="w")

        self.cb_sexo = ctk.CTkComboBox(self.card_formulario,
                                       values=["Masculino", "Femenino"],
                                       fg_color="#1A1A1E", border_color="#45A29E",
                                       height=40, state="readonly")
        self.cb_sexo.set("Seleccione...")
        self.cb_sexo.grid(row=3, column=1, padx=25, pady=(0, 15), sticky="we")

        # ── FILA 3: TELÉFONO + ESPECIALIDAD ──────────────────────────────────
        ctk.CTkLabel(self.card_formulario, text="Teléfono:",
                     font=fuente_labels, text_color="white"
                     ).grid(row=4, column=0, padx=25, pady=(0, 2), sticky="w")

        self.txt_telefono = ctk.CTkEntry(self.card_formulario,
                                         placeholder_text=" 📞 Celular o teléfono fijo",
                                         fg_color="#1A1A1E", border_color="#45A29E", height=40)
        self.txt_telefono.grid(row=5, column=0, padx=25, pady=(0, 15), sticky="we")

        ctk.CTkLabel(self.card_formulario, text="Especialidad:",
                     font=fuente_labels, text_color="white"
                     ).grid(row=4, column=1, padx=25, pady=(0, 2), sticky="w")

        # Campo exclusivo de médicos
        self.cb_especialidad = ctk.CTkComboBox(
            self.card_formulario,
            values=["Cirugía", "Dermatología", "Medicina General",
                    "Ortopedia", "Cardiología", "Odontología",
                    "Oftalmología", "Neurología", "Otra"],
            fg_color="#1A1A1E", border_color="#45A29E",
            height=40, state="readonly")
        self.cb_especialidad.set("Seleccione...")
        self.cb_especialidad.grid(row=5, column=1, padx=25, pady=(0, 15), sticky="we")

        # ── FILA 4: CONTRASEÑA (ocupa columna 0) ─────────────────────────────
        ctk.CTkLabel(self.card_formulario, text="Contraseña:",
                     font=fuente_labels, text_color="white"
                     ).grid(row=6, column=0, padx=25, pady=(0, 2), sticky="w")

        self.txt_password = ctk.CTkEntry(self.card_formulario,
                                         placeholder_text=" 🔑 Asigne una contraseña",
                                         fg_color="#1A1A1E", border_color="#45A29E",
                                         height=40, show="*")
        self.txt_password.grid(row=7, column=0, padx=25, pady=(0, 20), sticky="we")

        # ── BOTONES ───────────────────────────────────────────────────────────
        ctk.CTkButton(self.card_formulario,
                      text="🡰 REGRESAR A GESTIÓN",
                      font=("Segoe UI", 13, "bold"),
                      fg_color="#45A29E", hover_color="#31726F",
                      text_color="white", height=45, corner_radius=8,
                      command=self.al_cerrar
                      ).grid(row=8, column=0, padx=25, pady=(0, 20), sticky="we")

        ctk.CTkButton(self.card_formulario,
                      text=texto_boton,
                      font=("Segoe UI", 13, "bold"),
                      fg_color="#45A24D", hover_color="#3E7231",
                      text_color="white", height=45, corner_radius=10,
                      command=self.ejecutar_accion
                      ).grid(row=8, column=1, padx=25, pady=(0, 20), sticky="we")

    # ==========================================================================
    # ACCIONES
    # ==========================================================================
    def ejecutar_accion(self):
        if self.nit_editar:
            self.controlador_registro.actualizar_medico(self.nit_editar)
        else:
            self.controlador_registro.registrar_medico()

    def al_cerrar(self):
        self.ventana_padre.attributes("-alpha", 1.0)
        self.destroy()