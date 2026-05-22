import customtkinter as ctk
from backend.admin.gestion_medico_controller import *

class GestionMedicoVentana(ctk.CTkFrame):
    def __init__(self, ventana_padre, controlador_home):
        super().__init__(ventana_padre, fg_color="#1A1A1E")
        self.ventana_padre = ventana_padre
        self.controlador_home = controlador_home
        
        # Instanciar nuestro nuevo controlador
        self.controlador = (self)
        
        # Estructura principal en dos columnas (Izquierda: Médicos, Derecha: Citas)
        self.columnconfigure(0, weight=3) # Contenedor de Médicos
        self.columnconfigure(1, weight=1) # Panel lateral derecho
        self.rowconfigure(0, weight=1)
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # ---------------------------------------------------------------------
        # COLUMNA IZQUIERDA: CONTENEDOR PRINCIPAL DE MÉDICOS
        # ---------------------------------------------------------------------
        self.frame_izquierdo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        
        # Encabezado informativo (Panel de Control)
        self.lbl_sub = ctk.CTkLabel(self.frame_izquierdo, text="PANEL DE CONTROL", font=("Segoe UI", 11, "bold"), text_color="#45A29E")
        self.lbl_sub.pack(anchor="w", padx=10)
        
        self.lbl_titulo = ctk.CTkLabel(self.frame_izquierdo, text="Médicos registrados", font=("Segoe UI", 22, "bold"), text_color="white")
        self.lbl_titulo.pack(anchor="w", padx=10, pady=(0, 2))
        
        self.lbl_desc = ctk.CTkLabel(self.frame_izquierdo, text="Haz clic en una tarjeta para ver las citas asignadas", font=("Segoe UI", 12), text_color="gray")
        self.lbl_desc.pack(anchor="w", padx=10, pady=(0, 15))

        # --- SECCIÓN SUPERIOR: CONTENEDORES KPI (CONTADORES) ---
        self.frame_kpis = ctk.CTkFrame(self.frame_izquierdo, fg_color="transparent")
        self.frame_kpis.pack(fill="x", padx=10, pady=(0, 15))
        
        # Botón Registrar Médico a la derecha de los KPIs
        self.btn_registrar = ctk.CTkButton(
            self.frame_kpis, text="+ Registrar médico", font=("Segoe UI", 13, "bold"),
            fg_color="#242429", hover_color="#2F2F35", border_color="#45A29E", border_width=1,
            height=40, command=lambda: print("Abrir registro médico")
        )
        self.btn_registrar.pack(side="right", padx=(10, 0), alignment="center")

        # Obtenemos datos para inflar las tarjetas superiores
        self.medicos_dict = self.controlador.obtain_medicos() if hasattr(self.controlador, 'obtain_medicos') else self.controlador.obtener_medicos()
        tot, masc, fem, citas_hoy = self.controlador.obtener_estadisticas(self.medicos_dict)

        self.crear_kpi_card("Total", tot, "#45A29E")
        self.crear_kpi_card("Masculino", masc, "#17A2B8")
        self.crear_kpi_card("Femenino", fem, "#6745B8")
        self.crear_kpi_card("Citas hoy", citas_hoy, "#E67E22")

        # --- GRID SCROLLABLE PARA LAS TARJETAS DE MÉDICOS ---
        self.scroll_medicos = ctk.CTkScrollableFrame(self.frame_izquierdo, fg_color="#242429", corner_radius=15)
        self.scroll_medicos.pack(fill="both", expand=True, padx=10)
        
        # Configuramos columnas del grid interno (2 columnas de tarjetas)
        self.scroll_medicos.columnconfigure(0, weight=1)
        self.scroll_medicos.columnconfigure(1, weight=1)
        
        self.dibujar_tarjetas_medicos()

        # ---------------------------------------------------------------------
        # COLUMNA DERECHA: PANEL LATERAL FIJO (CITAS)
        # ---------------------------------------------------------------------
        self.panel_lateral = ctk.CTkFrame(self, fg_color="#242429", corner_radius=0)
        self.panel_lateral.grid(row=0, column=1, sticky="nsew")
        
        self.lbl_citas_titulo = ctk.CTkLabel(self.panel_lateral, text="📅 Citas del médico", font=("Segoe UI", 14, "bold"), text_color="white")
        self.lbl_citas_titulo.pack(anchor="w", padx=20, pady=(25, 15))
        
        # Contenedor scrollable para meter las filas de las citas
        self.scroll_citas = ctk.CTkScrollableFrame(self.panel_lateral, fg_color="transparent")
        self.scroll_citas.pack(fill="both", expand=True, padx=10, pady=5)

    def crear_kpi_card(self, titulo, valor, color):
        card = ctk.CTkFrame(self.frame_kpis, fg_color="#242429", border_color=color, border_width=1, width=100, height=55)
        card.pack(side="right", padx=5)
        card.pack_propagate(False)
        
        lbl_val = ctk.CTkLabel(card, text=str(valor), font=("Segoe UI", 16, "bold"), text_color=color)
        lbl_val.pack(pady=(5, 0))
        lbl_tit = ctk.CTkLabel(card, text=titulo, font=("Segoe UI", 10), text_color="gray")
        lbl_tit.pack()

    def dibujar_tarjetas_medicos(self):
        fila, columna = 0, 0
        
        for nit, datos in self.medicos_dict.items():
            nombre_completo = f"{datos.get('nombre', '')} {datos.get('apellido', '')}"
            especialidad = datos.get("especialidad", "General")
            telefono = datos.get("telefono", "")
            sexo = datos.get("sexo", "Masculino")
            
            # Contar citas asignadas para este médico en el CSV
            num_citas = self.controlador.contar_citas_medico(nit)
            
            # Contenedor de la Tarjeta del Médico
            card = ctk.CTkFrame(self.scroll_medicos, fg_color="#1A1A1E", border_color="#333338", border_width=1, height=190, corner_radius=12)
            card.grid(row=fila, column=columna, padx=12, pady=12, sticky="nsew")
            card.grid_propagate(False)
            
            # Hacer que la tarjeta escuche el clic para cargar sus citas a la derecha
            card.bind("<Button-1>", lambda e, n=nit, nom=nombre_completo: self.controlador.cargar_citas_medico_lateral(n, nom))
            
            # --- COMPONENTES INTERNOS DE LA CARD ---
            # Iniciales en Círculo (Avatar)
            iniciales = (datos.get('nombre', 'M')[0] + datos.get('apellido', 'V')[0]).upper()
            avatar = ctk.CTkFrame(card, fg_color="#2C3E50" if sexo == "Masculino" else "#4A2E80", width=45, height=45, corner_radius=22)
            avatar.place(x=20, y=20)
            avatar.pack_propagate(False)
            
            lbl_av = ctk.CTkLabel(avatar, text=iniciales, font=("Segoe UI", 14, "bold"), text_color="white")
            lbl_av.pack(expand=True)
            
            # Nombre y Especialidad
            lbl_nom = ctk.CTkLabel(card, text=nombre_completo, font=("Segoe UI", 14, "bold"), text_color="white")
            lbl_nom.place(x=80, y=18)
            lbl_esp = ctk.CTkLabel(card, text=especialidad, font=("Segoe UI", 12), text_color="#45A29E")
            lbl_esp.place(x=80, y=38)
            
            # Datos de contacto en columnas/etiquetas chicas
            lbl_tit_nit = ctk.CTkLabel(card, text="NIT", font=("Segoe UI", 10), text_color="gray")
            lbl_tit_nit.place(x=20, y=80)
            lbl_val_nit = ctk.CTkLabel(card, text=nit, font=("Segoe UI", 11, "bold"), text_color="white")
            lbl_val_nit.place(x=20, y=98)
            
            lbl_tit_tel = ctk.CTkLabel(card, text="TELÉFONO", font=("Segoe UI", 10), text_color="gray")
            lbl_tit_tel.place(x=150, y=80)
            lbl_val_tel = ctk.CTkLabel(card, text=telefono, font=("Segoe UI", 11), text_color="white")
            lbl_val_tel.place(x=150, y=98)
            
            # Badge de Citas Asignadas
            color_badge = "#2C3E50" if num_citas > 0 else "#242429"
            badge_citas = ctk.CTkFrame(card, fg_color=color_badge, height=30, corner_radius=15)
            badge_citas.place(x=20, y=140)
            
            lbl_badge = ctk.CTkLabel(badge_citas, text=f"  {num_citas} citas asignadas  ", font=("Segoe UI", 11, "bold"), text_color="white")
            lbl_badge.pack(expand=True, padx=5)
            
            # Botones de Acción (Editar y Borrar)
            btn_edit = ctk.CTkButton(card, text="📝 Editar", font=("Segoe UI", 11, "bold"), fg_color="#242429", hover_color="#2F2F35", width=75, height=30, corner_radius=6)
            btn_edit.place(x=185, y=140)
            
            btn_del = ctk.CTkButton(card, text="🗑", font=("Segoe UI", 12), fg_color="#242429", hover_color="#8B2525", width=35, height=30, corner_radius=6)
            btn_del.place(x=268, y=140)

            # Control de matriz (2 columnas por fila)
            columna += 1
            if columna > 1:
                columna = 0
                fila += 1

    def crear_item_cita_lateral(self, paciente, tipo, raza, fecha, hora, estado, color_estado):
        """Genera una fila estilizada de cita en el panel derecho."""
        item = ctk.CTkFrame(self.scroll_citas, fg_color="#1A1A1E", height=85, corner_radius=8)
        item.pack(fill="x", pady=6)
        
        # Nombre de mascota y datos
        lbl_pac = ctk.CTkLabel(item, text=paciente, font=("Segoe UI", 13, "bold"), text_color="white")
        lbl_pac.place(x=15, y=10)
        
        lbl_det = ctk.CTkLabel(item, text=f"{tipo} · {raza}", font=("Segoe UI", 11), text_color="gray")
        lbl_det.place(x=15, y=28)
        
        lbl_time = ctk.CTkLabel(item, text=f"📅 {fecha}  🕒 {hora}", font=("Segoe UI", 10), text_color="#45A29E")
        lbl_time.place(x=15, y=52)
        
        # Badge de estado (Pendiente, En curso, Cancelado)
        badge = ctk.CTkFrame(item, fg_color=color_estado, height=20, corner_radius=4)
        badge.place(x=210, y=10)
        
        lbl_b = ctk.CTkLabel(badge, text=estado, font=("Segoe UI", 9, "bold"), text_color="white")
        lbl_b.pack(padx=6)
        
        return item