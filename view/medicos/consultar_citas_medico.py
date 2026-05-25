import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from backend.medicos.citas import BackendCitas

# Configuración general del tema
ctk.set_appearance_mode("dark")

# Datos de usuario simulados por si se ejecuta de forma independiente
datos_usuario = {"id_medico": "1", "sexo": "Masculino", "nombre": "Juan", "apellido": "Pérez"}

class GestionMedicoController:
    @staticmethod
    def cerrar_sesion(ventana):
        print("Cerrando sesión...")
        ventana.destroy()

class VentanaConsultarCitas():
    def __init__(self, datos_usuario_login=None):
        self.datos_usuario = datos_usuario_login if datos_usuario_login else datos_usuario
        self.cita_seleccionada = None
        self.todas_las_citas = []

        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DE LA VENTANA ─────────────────────────────────────────────────────
        # ========================================================================================================
        self.ventana = ctk.CTk()
        ctk.set_appearance_mode("dark")
        
        self.ventana.iconbitmap("image/huella_icono.ico") 
        self.ventana.title("SystemVet / Consultar Cita")
        self.ventana.after(0, lambda: self.ventana.state('zoomed'))

        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DEL ENCABEZADO ────────────────────────────────────────────────────
        # ========================================================================================================
        self.header = tk.Frame(self.ventana, bg="#45A29E")
        self.header.pack(side="top", fill="x") 
        
        # Logotipo de la clínica
        try:
            self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2)
        except:
            self.image_logo = tk.PhotoImage()

        image_logo = tk.Label(
            self.header,
            bg="#45A29E",
            width=70,
            height=70,
            image=self.image_logo,
            cursor="hand2"
        )
        image_logo.image = self.image_logo
        image_logo.pack(side="left", padx=20, pady=10)
        image_logo.bind("<Button-1>", lambda event: self.ir_a_home())

        # Título "Home Médico / Médica"
        titulo_home = "Home Médico" if self.datos_usuario["sexo"] == "Masculino" else "Home Médica"
        tk.Label(
            self.header,
            text=titulo_home,
            fg="white",
            bg="#45A29E",
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")
        
        # Avatar de usuario según corresponda del sexo
        avatar = "image/avatar_masculino.png" if self.datos_usuario["sexo"] == "Masculino" else "image/avatar_femenino.png"
        try:
            img_original = tk.PhotoImage(file=avatar) 
            self.image_avatar = img_original.subsample(2, 2)
        except:
            self.image_avatar = tk.PhotoImage()

        image_avatar = tk.Label(
            self.header,
            bg="#45A29E",
            image=self.image_avatar
        )
        image_avatar.image = self.image_avatar
        image_avatar.pack(side="right", padx=(0, 20))

        # Información de sesión a la derecha del Header
        self.container_usuario = tk.Frame(self.header, bg="#45A29E")
        self.container_usuario.pack(side="right", padx=20)
        
        rol = "Médico" if self.datos_usuario["sexo"] == "Masculino" else "Médica"
        tk.Label(
            self.container_usuario,
            text=rol,
            bg="#45A29E",
            fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(side="top", anchor="e")
        
        self.fila_nombre = tk.Frame(self.container_usuario, bg="#45A29E")
        self.fila_nombre.pack(side="top", anchor="e")
        
        tk.Label(
            self.fila_nombre,
            text=f"{self.datos_usuario['nombre']} {self.datos_usuario['apellido']}    | ",
            bg="#45A29E",
            fg="white",
            font=("Segoe UI", 13)
        ).pack(side="left", padx=(0, 5))
        
        self.btn_cerrar_sesion = tk.Button(
            self.fila_nombre,
            text="Cerrar sesión",
            bg="#45A29E",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            borderwidth=0,
            cursor="hand2",
            command=lambda: GestionMedicoController.cerrar_sesion(self.ventana)
        )
        self.btn_cerrar_sesion.pack(side="left")

        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DEL CUERPO (CENTRADOS) ────────────────────────────────────────────
        # ========================================================================================================
        cuerpo = ctk.CTkFrame(self.ventana, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, pady=30, padx=40)

        # Panel de título principal
        title_frame = ctk.CTkFrame(cuerpo, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        
        lbl_title = ctk.CTkLabel(
            title_frame,
            text="Consultar Citas",
            font=("Segoe UI", 26, "bold"),
            text_color="#45A29E"
        )
        lbl_title.pack(side="left")

        # --- FILTRO Y BÚSQUEDA PANEL ---
        card_filtros = ctk.CTkFrame(
            cuerpo,
            fg_color="#1a1a1f",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        card_filtros.pack(fill="x", pady=(0, 15), ipady=10)

        # Campo: Buscar por paciente / dueño
        ctk.CTkLabel(
            card_filtros,
            text="Buscar paciente / dueño:",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(10, 2))

        self.entry_busqueda = ctk.CTkEntry(
            card_filtros,
            placeholder_text="Escriba nombre o dueño para filtrar...",
            height=35,
            fg_color="#121212",
            border_width=1,
            border_color="#333333"
        )
        self.entry_busqueda.grid(row=1, column=0, sticky="ew", padx=(20, 10))
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.aplicar_filtros())

        # Campo: Filtrar por Estado
        ctk.CTkLabel(
            card_filtros,
            text="Filtrar por Estado:",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))

        self.cmb_estado_filtro = ctk.CTkComboBox(
            card_filtros,
            values=["Todos", "Pendiente", "Completada", "Cancelada"],
            height=35,
            fg_color="#ffffff",
            text_color="black",
            border_width=0,
            state="readonly",
            command=lambda val: self.aplicar_filtros()
        )
        self.cmb_estado_filtro.set("Todos")
        self.cmb_estado_filtro.grid(row=1, column=1, sticky="ew", padx=(10, 20))

        card_filtros.grid_columnconfigure(0, weight=3)
        card_filtros.grid_columnconfigure(1, weight=1)

        # --- PANEL DE LA TABLA ---
        card_tabla = ctk.CTkFrame(
            cuerpo,
            fg_color="#1a1a1f",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        card_tabla.pack(fill="both", expand=True, pady=(0, 15))

        # Estilo personalizado para la tabla ttk.Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1a1a1f",
            foreground="white",
            rowheight=35,
            fieldbackground="#1a1a1f",
            bordercolor="#333333",
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        # Cambios de selección y focus
        style.map('Treeview', background=[('selected', '#45A29E')], foreground=[('selected', 'white')])
        style.configure(
            "Treeview.Heading",
            background="#45A29E",
            foreground="white",
            relief="flat",
            font=('Segoe UI', 11, 'bold')
        )
        style.map("Treeview.Heading", background=[('active', '#3b8b87')])

        # Contenedor para Treeview y sus scrollbars
        tabla_frame = tk.Frame(card_tabla, bg="#1a1a1f")
        tabla_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Definición de las columnas de la tabla
        columnas = (
            "id_cita",
            "id_medico",
            "nombre_paciente",
            "nombre_propietario",
            "tipo_animal",
            "fecha",
            "hora",
            "tipo_servicio",
            "motivo",
            "estado"
        )
        
        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # Encabezados y anchos de las columnas
        cabeceras = {
            "id_cita": "ID Cita",
            "id_medico": "ID Médico",
            "nombre_paciente": "Paciente",
            "nombre_propietario": "Propietario",
            "tipo_animal": "Animal",
            "fecha": "Fecha",
            "hora": "Hora",
            "tipo_servicio": "Servicio",
            "motivo": "Motivo de Consulta",
            "estado": "Estado"
        }

        anchos = {
            "id_cita": 60,
            "id_medico": 80,
            "nombre_paciente": 110,
            "nombre_propietario": 120,
            "tipo_animal": 80,
            "fecha": 100,
            "hora": 90,
            "tipo_servicio": 120,
            "motivo": 200,
            "estado": 100
        }

        for col, text in cabeceras.items():
            self.tabla.heading(col, text=text, anchor="center")
            self.tabla.column(col, width=anchos[col], anchor="center" if col != "motivo" else "w")

        # Scrollbars
        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(fill="both", expand=True)

        # Evento de selección de fila
        self.tabla.bind("<<TreeviewSelect>>", self.on_fila_seleccionada)

        # --- TARJETA DE GESTIÓN Y DETALLES DE CITA ---
        self.card_gestion = ctk.CTkFrame(
            cuerpo,
            fg_color="#1a1a1f",
            corner_radius=10,
            border_width=1,
            border_color="#333333",
            height=130
        )
        self.card_gestion.pack(fill="x", pady=5)
        self.card_gestion.pack_propagate(False) # Mantener el tamaño fijo para evitar saltos

        self.lbl_gestion_info = ctk.CTkLabel(
            self.card_gestion,
            text="Seleccione una cita de la lista para gestionar su estado.",
            font=("Segoe UI", 13, "italic"),
            text_color="gray"
        )
        self.lbl_gestion_info.pack(expand=True)

        # Contenedor de acciones (inicialmente oculto o vacío)
        self.frame_acciones = ctk.CTkFrame(self.card_gestion, fg_color="transparent")

        # Cargar los datos iniciales
        self.recargar_datos_desde_csv()

        self.ventana.mainloop()

    # ========================================================================================================
    # ────────────────────── MÉTODOS DE LA LOGICA Y EVENTOS ──────────────────────────────────────────────────
    # ========================================================================================================
    def ir_a_home(self):
        """Cierra la ventana actual y regresa al home del médico."""
        self.ventana.destroy()
        from view.medicos.home_medico import HomeMedico
        HomeMedico(self.datos_usuario)

    def ir_a_crear_cita(self):
        """Cierra la ventana actual y regresa a la creación de citas."""
        self.ventana.destroy()
        from view.medicos.crear_citas_medico import VentanaCrearCita
        app_crear = VentanaCrearCita(self.datos_usuario)

    def recargar_datos_desde_csv(self):
        """Carga todas las citas desde el backend y las aplica al Treeview."""
        self.todas_las_citas = BackendCitas.obtener_todas_citas()
        self.aplicar_filtros()

    def aplicar_filtros(self):
        """Aplica la búsqueda por texto y el filtro de estado sobre los datos cargados."""
        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        texto_busqueda = self.entry_busqueda.get().lower().strip()
        filtro_estado = self.cmb_estado_filtro.get()

        for cita in self.todas_las_citas:
            # Filtro por estado
            if filtro_estado != "Todos" and cita.get("estado") != filtro_estado:
                continue

            # Filtro por búsqueda
            paciente = cita.get("nombre_paciente", "").lower()
            dueno = cita.get("nombre_propietario", "").lower()
            id_cita = str(cita.get("id_cita", "")).lower()

            if texto_busqueda and (texto_busqueda not in paciente and texto_busqueda not in dueno and texto_busqueda not in id_cita):
                continue

            # Insertar en la tabla
            self.tabla.insert(
                "",
                "end",
                values=(
                    cita.get("id_cita"),
                    cita.get("id_medico"),
                    cita.get("nombre_paciente"),
                    cita.get("nombre_propietario"),
                    cita.get("tipo_animal"),
                    cita.get("fecha"),
                    cita.get("hora"),
                    cita.get("tipo_servicio"),
                    cita.get("motivo"),
                    cita.get("estado")
                )
            )
        
        # Deseleccionar al filtrar
        self.limpiar_seleccion_gestion()

    def on_fila_seleccionada(self, event):
        """Manejador del evento de selección en la tabla. Habilita los botones de gestión."""
        seleccion = self.tabla.selection()
        if not seleccion:
            self.limpiar_seleccion_gestion()
            return

        item = self.tabla.item(seleccion[0])
        valores = item["values"]
        
        if not valores:
            self.limpiar_seleccion_gestion()
            return

        # Estructurar la cita seleccionada
        self.cita_seleccionada = {
            "id_cita": valores[0],
            "id_medico": valores[1],
            "nombre_paciente": valores[2],
            "nombre_propietario": valores[3],
            "tipo_animal": valores[4],
            "fecha": valores[5],
            "hora": valores[6],
            "tipo_servicio": valores[7],
            "motivo": valores[8],
            "estado": valores[9]
        }

        # Ocultar etiqueta vacía y mostrar frame de acciones
        self.lbl_gestion_info.pack_forget()
        self.frame_acciones.pack(fill="both", expand=True, padx=20, pady=10)

        # Limpiar frame de acciones previo
        for widget in self.frame_acciones.winfo_children():
            widget.destroy()

        # Grid layout para detalles y botones
        self.frame_acciones.grid_columnconfigure(0, weight=2)
        self.frame_acciones.grid_columnconfigure(1, weight=3)

        # Panel izquierdo del frame de acciones: Detalles de la cita
        frame_detalles = ctk.CTkFrame(self.frame_acciones, fg_color="transparent")
        frame_detalles.grid(row=0, column=0, sticky="nsew", padx=(10, 20))

        lbl_det_title = ctk.CTkLabel(
            frame_detalles,
            text=f"Gestionar Cita #{self.cita_seleccionada['id_cita']} | Paciente: {self.cita_seleccionada['nombre_paciente']}",
            font=("Segoe UI", 13, "bold"),
            text_color="#45A29E"
        )
        lbl_det_title.pack(anchor="w")

        lbl_det_sub = ctk.CTkLabel(
            frame_detalles,
            text=f"Propietario: {self.cita_seleccionada['nombre_propietario']}  •  Servicio: {self.cita_seleccionada['tipo_servicio']}\nFecha: {self.cita_seleccionada['fecha']} a las {self.cita_seleccionada['hora']}  •  Estado actual: {self.cita_seleccionada['estado']}",
            font=("Segoe UI", 11),
            text_color="gray",
            justify="left"
        )
        lbl_det_sub.pack(anchor="w", pady=(5, 0))

        # Panel derecho: Botones de cambio de estado
        frame_botones = ctk.CTkFrame(self.frame_acciones, fg_color="transparent")
        frame_botones.grid(row=0, column=1, sticky="nsew")
        
        # Centrar verticalmente los botones
        frame_botones.grid_rowconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(0, weight=1)
        frame_botones.grid_columnconfigure(1, weight=1)
        frame_botones.grid_columnconfigure(2, weight=1)

        # Botón Completada
        btn_completada = ctk.CTkButton(
            frame_botones,
            text="✓ Completar",
            font=("Segoe UI", 12, "bold"),
            fg_color="#45A29E",
            hover_color="#2C7A7B",
            height=38,
            command=lambda: self.cambiar_estado_cita("Completada")
        )
        btn_completada.grid(row=0, column=0, padx=5, sticky="ew")

        # Botón Pendiente
        btn_pendiente = ctk.CTkButton(
            frame_botones,
            text="⏳ Pendiente",
            font=("Segoe UI", 12, "bold"),
            fg_color="#D69E2E",
            hover_color="#B7791F",
            height=38,
            command=lambda: self.cambiar_estado_cita("Pendiente")
        )
        btn_pendiente.grid(row=0, column=1, padx=5, sticky="ew")

        # Botón Cancelada
        btn_cancelada = ctk.CTkButton(
            frame_botones,
            text="✕ Cancelar",
            font=("Segoe UI", 12, "bold"),
            fg_color="#E53E3E",
            hover_color="#C53030",
            height=38,
            command=lambda: self.cambiar_estado_cita("Cancelada")
        )
        btn_cancelada.grid(row=0, column=2, padx=5, sticky="ew")

    def limpiar_seleccion_gestion(self):
        """Restablece la sección de gestión al estado inicial 'sin selección'."""
        self.cita_seleccionada = None
        self.frame_acciones.pack_forget()
        self.lbl_gestion_info.pack(expand=True)

    def cambiar_estado_cita(self, nuevo_estado):
        """Envía la orden al backend para actualizar el estado en el CSV y refresca la vista."""
        if not self.cita_seleccionada:
            return

        id_cita = self.cita_seleccionada["id_cita"]
        
        # Validar si ya está en ese estado
        if self.cita_seleccionada["estado"] == nuevo_estado:
            messagebox.showinfo("Información", f"La cita ya se encuentra en estado '{nuevo_estado}'.")
            return

        # Confirmar cambio de estado
        confirmar = messagebox.askyesno(
            "Confirmar Cambio de Estado", 
            f"¿Está seguro de cambiar el estado de la cita #{id_cita} a '{nuevo_estado}'?"
        )
        
        if confirmar:
            exito, mensaje = BackendCitas.actualizar_estado_cita(id_cita, nuevo_estado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.recargar_datos_desde_csv()
            else:
                messagebox.showerror("Error", mensaje)

if __name__ == "__main__":
    app = VentanaConsultarCitas()
