import tkinter as tk
import customtkinter as ctk
# Importación de los Controladores (Backend) siguiendo el patrón MVC (Modelo-Vista-Controlador)
from backend.admin.gestion_reporte_controller import ReportesController
from backend.admin.gestion_medico_controller import GestionMedicosController


class ReportesVentana:
    def __init__(self, ventana, datos_usuario):
        """
        MÉTODO CONSTRUCTOR: Se ejecuta automáticamente al abrir la ventana.
        Configura el aspecto visual inicial y conecta la vista con el controlador.
        """
        self.ventana       = ventana        # Guarda la ventana principal recibida
        self.datos_usuario = datos_usuario  # Almacena los datos del usuario logueado (nombre, rol, sexo)
        self._fig_actual   = None           # Variable para guardar el gráfico actual de Matplotlib

        # Configuración estética de la ventana usando CustomTkinter y Tkinter estándar
        ctk.set_appearance_mode("dark")     # Forza el tema oscuro en la interfaz
        self.ventana.iconbitmap("image/huella_icono.ico")  # Cambia el icono de la ventana
        self.ventana.title("SystemVet - Panel de Reportes Estadísticos") # Título superior
        self.ventana.configure(bg="#1A1A1E", bd=0)          # Fondo gris oscuro sin bordes

        # LLAMADAS A LOS MÉTODOS DE CONSTRUCCIÓN VISUAL
        self._construir_header(datos_usuario)  # Dibuja la barra superior
        self._construir_cuerpo()              # Dibuja la zona de filtros y gráficos

        # INSTANCIA DEL CONTROLADOR: Aquí se vincula la Vista con la lógica del Backend
        self.controlador = ReportesController(self)

    # ==========================================================================
    # HEADER — Mismo patrón estético de identidad del sistema
    # ==========================================================================
    def _construir_header(self, datos_usuario):
        """
        Crea la barra superior de la pantalla. Contiene branding, datos del usuario
        y controles globales como cerrar sesión o regresar.
        """
        # Contenedor principal del Header (Color verde menta / turquesa)
        self.header = tk.Frame(self.ventana, bg="#45A29E")
        self.header.pack(side="top", fill="x", ipady=2) # Se posiciona arriba y se expande horizontalmente

        # BOTÓN LOGO (Actúa como botón para regresar al menú anterior)
        self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2) # Carga y escala el logo
        self.btn_regresar = tk.Button(
            self.header,
            image=self.image_logo,
            bg="#45A29E", activebackground="#45A29E",
            bd=0, cursor="hand2", # cursor="hand2" cambia el puntero a una mano interactiva
            width=70, height=70,
            # Evento: Al hacer clic, el controlador de médicos gestiona el regreso de ventana de forma segura
            command=lambda: GestionMedicosController.regresar_ventana(self.ventana, datos_usuario)
        )
        self.btn_regresar.image = self.image_logo # Evita que Python borre la imagen de la memoria ram
        self.btn_regresar.pack(side="left", padx=20, pady=10)

        # TEXTOS DE IDENTIFICACIÓN DE LA PANTALLA
        contenedor_titulo = tk.Frame(self.header, bg="#45A29E")
        contenedor_titulo.pack(side="left")

        tk.Label(contenedor_titulo, text="System Vet",
                 fg="white", bg="#45A29E",
                 font=("Segoe UI", 11, "bold")).pack(side="top", anchor="w")
        tk.Label(contenedor_titulo, text="GESTIÓN DE REPORTES ESTADÍSTICOS",
                 fg="white", bg="#45A29E",
                 font=("Segoe UI", 15, "bold")).pack(side="top", anchor="w")

        # SECCIÓN DE PERFIL (AVATAR DINÁMICO)
        # Condicional que evalúa el sexo del usuario para mostrar la foto correcta
        avatar = ("image/avatar_masculino.png"
                  if datos_usuario["sexo"] == "Masculino"
                  else "image/avatar_femenino.png")
        img_original      = tk.PhotoImage(file=avatar)
        self.image_avatar = img_original.subsample(2, 2)
        lbl_avatar = tk.Label(self.header, bg="#45A29E", image=self.image_avatar)
        lbl_avatar.image = self.image_avatar
        lbl_avatar.pack(side="right", padx=(0, 20)) # Se alinea a la extrema derecha

        # TEXTOS DE INFORMACIÓN DEL USUARIO Y BOTÓN DE CERRAR SESIÓN
        container_usuario = tk.Frame(self.header, bg="#45A29E")
        container_usuario.pack(side="right", padx=20)

        # Muestra Nombre y Apellido extraídos directamente del diccionario 'datos_usuario'
        tk.Label(container_usuario,
                 text=f"{datos_usuario['nombre']} {datos_usuario['apellido']}",
                 bg="#45A29E", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")

        fila_nombre = tk.Frame(container_usuario, bg="#45A29E")
        fila_nombre.pack(side="top", anchor="e")

        # Ajusta el texto del rol según el género gramatical
        rol = "Administrador" if datos_usuario["sexo"] == "Masculino" else "Administradora"
        tk.Label(fila_nombre, text=rol,
                 bg="#45A29E", fg="white",
                 font=("Segoe UI", 13)).pack(side="left", padx=(0, 5))

        # Botón con evento asignado al controlador para destruir la sesión actual y volver al Login
        tk.Button(fila_nombre, text="|   Cerrar sesión",
                  bg="#45A29E", fg="white",
                  font=("Segoe UI", 12, "bold"),
                  borderwidth=0, cursor="hand2",
                  command=lambda: GestionMedicosController.cerrar_sesion(self.ventana)
                  ).pack(side="left")

    # ==========================================================================
    # CUERPO PRINCIPAL
    # ==========================================================================
    def _construir_cuerpo(self):
        """
        Divide el espacio restante de la pantalla en dos columnas principales:
        Izquierda (Sidebar de filtros) y Derecha (Área de gráficos).
        """
        cuerpo = tk.Frame(self.ventana, bg="#1A1A1E")
        cuerpo.pack(fill="both", expand=True) # expand=True permite que ocupe todo el espacio libre
        
        self._construir_sidebar(cuerpo)       # Construye la barra de herramientas izquierda
        self._construir_area_grafico(cuerpo)  # Construye el lienzo visual derecho

    # ==========================================================================
    # SIDEBAR DE FILTROS (Panel Izquierdo)
    # ==========================================================================
    def _construir_sidebar(self, parent):
        """
        Crea los elementos de interacción: Menús desplegables, cuadros de texto de fechas,
        checkboxes personalizados y los botones de acción para generar reportes.
        """
        # Contenedor gris oscuro de ancho fijo (240px) alineado a la izquierda
        sb = tk.Frame(parent, bg="#1E1E24", width=240)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False) # Evita que el contenedor se encoja al tamaño de sus hijos

        # TÍTULOS DEL PANEL
        tk.Label(sb, text="PANEL DE FILTROS",
                 fg="#45A29E", bg="#1E1E24",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(16, 2))

        fila_t = tk.Frame(sb, bg="#1E1E24")
        fila_t.pack(fill="x", padx=18, pady=(0, 10))
        tk.Label(fila_t, text="📊   FILTROS DE REPORTE",
                 fg="#E8E8EC", bg="#1E1E24",
                 font=("Segoe UI", 12, "bold")).pack(side="left")

        self._separador(sb) # Dibuja una fina línea divisoria estética

        # FILTRO 1: SELECCIÓN DEL TIPO DE GRÁFICO (CustomTkinter OptionMenu)
        self._titulo_filtro(sb, "Tipo de Gráfico:")
        self.var_grafico = tk.StringVar(value="Histograma por Estado") # Variable de control de Tkinter
        ctk.CTkOptionMenu(
            sb,
            values=[
                "Histograma por Estado",
                "Línea de Tendencia",
                "Barras por Médico",
                "Dona por Estado",
            ],
            variable=self.var_grafico, # Vincula la selección a la variable var_grafico
            fg_color="#242429",
            button_color="#45A29E",
            button_hover_color="#3a8a87",
            text_color="#E8E8EC",
            font=("Segoe UI", 11),
            width=204,
            dynamic_resizing=False,
        ).pack(padx=18, pady=(0, 14), anchor="w")

        self._separador(sb)

        # FILTRO 2: CHECKBOXES PARA SELECCIÓN DE ANIMALES
        self._titulo_filtro(sb, "Tipo de Animal:")
        self.var_perro = tk.BooleanVar(value=True)  # Variable booleana (True/False)
        self.var_gato  = tk.BooleanVar(value=False)

        fila_animales = tk.Frame(sb, bg="#1E1E24")
        fila_animales.pack(fill="x", padx=18, pady=(0, 14))

        # Instancia los checkboxes renderizados manualmente mediante el método _checkbox
        self._checkbox(fila_animales, "🐕   Perro", self.var_perro, "#45A29E")
        self._checkbox(fila_animales, "🐈   Gato",  self.var_gato,  "#CE93D8")

        self._separador(sb)

        # FILTRO 3: CHECKBOXES PARA EL ESTADO DE LAS CITAS VETERINARIAS
        self._titulo_filtro(sb, "Estado de Citas:")
        self.var_pendiente  = tk.BooleanVar(value=True)
        self.var_en_curso   = tk.BooleanVar(value=False)
        self.var_completada = tk.BooleanVar(value=True)
        self.var_cancelada  = tk.BooleanVar(value=False)

        estados_frame = tk.Frame(sb, bg="#1E1E24")
        estados_frame.pack(fill="x", padx=18, pady=(0, 14))

        self._checkbox(estados_frame, "⏳   Pendiente",  self.var_pendiente,  "#66BB6A")
        self._checkbox(estados_frame, "🔄   En curso",   self.var_en_curso,   "#45A29E")
        self._checkbox(estados_frame, "✅   Completada", self.var_completada, "#8BA5BE")
        self._checkbox(estados_frame, "❌   Cancelada",  self.var_cancelada,  "#EF5350")

        self._separador(sb)

        # FILTRO 4: CUADROS DE ENTRADA PARA FILTRADO POR FECHAS
        self._titulo_filtro(sb, "Fecha Inicial (AAAA-MM-DD):")
        self.entry_fecha_ini = ctk.CTkEntry(
            sb,
            placeholder_text="2026-01-01",
            fg_color="#242429", border_color="#3A3A40",
            text_color="#E8E8EC", font=("Segoe UI", 12),
            width=204, height=36,
        )
        self.entry_fecha_ini.pack(padx=18, pady=(0, 12), anchor="w")

        self._titulo_filtro(sb, "Fecha Final (AAAA-MM-DD):")
        self.entry_fecha_fin = ctk.CTkEntry(
            sb,
            placeholder_text="2026-12-31",
            fg_color="#242429", border_color="#3A3A40",
            text_color="#E8E8EC", font=("Segoe UI", 12),
            width=204, height=36,
        )
        self.entry_fecha_fin.pack(padx=18, pady=(0, 16), anchor="w")

        self._separador(sb)

        # BOTONES PRINCIPALES DE ACCIÓN (Llaman a métodos de procesamiento interno)
        ctk.CTkButton(
            sb,
            text="📊   Visualizar Gráfico",
            fg_color="#45A29E", hover_color="#3a8a87",
            text_color="#111114",
            font=("Segoe UI", 12, "bold"),
            height=42, corner_radius=10, cursor="hand2",
            command=self._solicitar_grafico, # Ejecuta la lógica para pedir el gráfico
        ).pack(fill="x", padx=18, pady=(12, 8))

        ctk.CTkButton(
            sb,
            text="💾   Exportar PNG",
            fg_color="transparent",
            hover_color="#242429",
            border_color="#3A3A40",
            border_width=1,
            text_color="#8BA5BE",
            font=("Segoe UI", 11),
            height=36, corner_radius=10, cursor="hand2",
            command=self._exportar_png, # Ejecuta la lógica para guardar la imagen del gráfico
        ).pack(fill="x", padx=18)

    # ==========================================================================
    # ÁREA DERECHA: Métricas KPI + Contenedor de Gráficos Matplotlib
    # ==========================================================================
    def _construir_area_grafico(self, parent):
        """
        Crea la zona central-derecha de la interfaz donde se renderizan las tarjetas
        informativas rápidas (KPIs) y el gráfico dinámico procesado.
        """
        area = tk.Frame(parent, bg="#1A1A1E")
        area.pack(side="left", fill="both", expand=True)

        # Sub-header decorativo interno
        sub = tk.Frame(area, bg="#242429", pady=10)
        sub.pack(fill="x")
        tk.Label(sub, text="📊   Visualización del Reporte",
                 fg="#E8E8EC", bg="#242429",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20)
        tk.Frame(area, bg="#45A29E", height=2).pack(fill="x") # Línea divisoria turquesa

        # SECCIÓN DE MÁTRIX / TARJETAS KPI (Key Performance Indicators)
        frame_m = tk.Frame(area, bg="#1A1A1E")
        frame_m.pack(fill="x", padx=20, pady=(14, 0))

        # Estructura de datos (Diccionario) para gestionar los valores dinámicos de las tarjetas
        self._metricas = {
            "total":    (tk.StringVar(value="—"), "Total citas",     "#45A29E"),
            "animales": (tk.StringVar(value="—"), "Tipos filtrados", "#CE93D8"),
            "pico":     (tk.StringVar(value="—"), "Pico diario",     "#FFB300"),
        }
        # Bucle 'for' automático para dibujar las 3 cajitas informativas sin repetir código redundante
        for var, lbl, color in self._metricas.values():
            card = tk.Frame(frame_m, bg="#242429",
                            padx=16, pady=8,
                            highlightbackground="#2A2A30",
                            highlightthickness=1)
            card.pack(side="left", padx=(0, 10))
            # El Label numérico usa 'textvariable=var' para actualizarse automáticamente desde el controlador
            tk.Label(card, textvariable=var, fg=color, bg="#242429",
                     font=("Segoe UI", 20, "bold")).pack()
            tk.Label(card, text=lbl, fg="#6A6A72", bg="#242429",
                     font=("Segoe UI", 9)).pack()

        # TÍTULO DINÁMICO DEL REPORTE (Cambia según el gráfico seleccionado)
        self.lbl_titulo = tk.Label(area, text="",
                                   fg="#8BA5BE", bg="#1A1A1E",
                                   font=("Segoe UI", 11),
                                   wraplength=860, justify="center")
        self.lbl_titulo.pack(pady=(10, 2))

        # LIENZO DESTINADO AL CANVAS: Espacio en blanco donde encajará el gráfico final
        self.frame_grafico = tk.Frame(area, bg="#1A1A1E")
        self.frame_grafico.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        self._placeholder() # Invoca el estado inicial por defecto (Mensaje de ayuda)

    # ==========================================================================
    # HELPERS DE CONSTRUCCIÓN (Funciones de Soporte Estético)
    # ==========================================================================
    def _separador(self, parent):
        """Dibuja una sutil línea gris horizontal para separar secciones visuales."""
        tk.Frame(parent, bg="#2A2A30", height=1).pack(fill="x", padx=18, pady=(0, 12))

    def _titulo_filtro(self, parent, texto):
        """Genera los textos de cabecera estándar de los filtros con tipografía uniforme."""
        tk.Label(parent, text=texto,
                 fg="#E8E8EC", bg="#1E1E24",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=18, pady=(0, 6))

    def _checkbox(self, parent, texto, variable, color_activo):
        """
        MÉTODO AVANZADO: Dibuja un Checkbox personalizado píxel por píxel usando un objeto Canvas.
        Se creó para evitar las limitaciones estéticas del checkbox nativo de Tkinter en modo oscuro.
        """
        fila = tk.Frame(parent, bg="#1E1E24")
        fila.pack(fill="x", pady=3)

        size = 16
        # El Canvas actúa como el recuadro interactivo donde se pintará el check (✓)
        cv = tk.Canvas(fila, width=size, height=size,
                       bg="#1E1E24", highlightthickness=0, cursor="hand2")
        cv.pack(side="left", padx=(0, 8))

        lbl = tk.Label(fila, text=texto,
                       bg="#1E1E24", fg="#C8C8D0",
                       font=("Segoe UI", 11), cursor="hand2")
        lbl.pack(side="left")

        def _dibujar():
            """Actualiza el diseño gráfico del checkbox dependiendo de su estado interno (True/False)."""
            cv.delete("all") # Borra los dibujos anteriores en el Canvas
            if variable.get(): # Si está activo, pinta un cuadrado sólido con un check blanco
                cv.create_rectangle(0, 0, size, size,
                                    fill=color_activo, outline=color_activo, width=0)
                cv.create_text(size // 2, size // 2, text="✓",
                               fill="#111114", font=("Segoe UI", 10, "bold"))
                lbl.configure(fg="#E8E8EC") # Resalta el texto al seleccionarse
            else: # Si está inactivo, dibuja solo un borde vacío
                cv.create_rectangle(0, 0, size, size,
                                    fill="#242429", outline="#3A3A40", width=1)
                lbl.configure(fg="#6A6A72") # Opaca el texto

        def _toggle(event=None):
            """Invierte el estado de la variable lógica al hacer clic."""
            variable.set(not variable.get())
            _dibujar() # Redibuja el nuevo aspecto visual inmediatamente

        # Vincula el clic del ratón tanto al recuadro como al texto adjunto
        cv.bind("<Button-1>", _toggle)
        lbl.bind("<Button-1>", _toggle)
        _dibujar() # Ejecuta el dibujo inicial en pantalla

    def _placeholder(self):
        """Establece la pantalla de bienvenida inicial dentro del contenedor de gráficos."""
        for w in self.frame_grafico.winfo_children():
            w.destroy() # Asegura limpiar cualquier residuo visual previo
        tk.Label(
            self.frame_grafico,
            text="Selecciona los filtros y presiona\n'Visualizar Gráfico' para generar el reporte",
            fg="#3A3A44", bg="#1A1A1E",
            font=("Segoe UI", 13), justify="center",
        ).place(relx=0.5, rely=0.5, anchor="center") # Lo posiciona matemáticamente en el centro exacto

    # ==========================================================================
    # API PÚBLICA PARA INTERCONEXIÓN DEL CONTROLADOR (Capa del backend llama aquí)
    # ==========================================================================
    def mostrar_canvas(self, fig, titulo, metricas):
        """
        MÉTODO CRÍTICO: Recibe un objeto Figure (de Matplotlib) con el gráfico ya procesado
        por el controlador, lo incrusta de forma nativa en la UI y actualiza los indicadores KPI.
        """
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        # Limpia el área del gráfico (borra el placeholder o gráficos obsoletos anteriores)
        for w in self.frame_grafico.winfo_children():
            w.destroy()

        # Actualiza dinámicamente los títulos de los Labels de la interfaz
        self.lbl_titulo.configure(text=titulo)
        
        # Inserta los números procesados en las variables enlazadas a las tarjetas superiores
        self._metricas["total"][0].set(str(metricas.get("total", "—")))
        self._metricas["animales"][0].set(str(metricas.get("animales", "—")))
        self._metricas["pico"][0].set(str(metricas.get("pico", "—")))

        # PUENTE INTERMEDIO MATPLOTLIB-TKINTER
        # Transforma el gráfico científico de Matplotlib en un componente gráfico compatible con Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw() # Dibuja la representación gráfica
        canvas.get_tk_widget().pack(fill="both", expand=True) # Expande e integra el componente al contenedor
        self._fig_actual = fig # Guarda el puntero en caché por si se requiere exportar a imagen externa

    def mostrar_error(self, mensaje):
        """Muestra de forma segura un mensaje de error controlado en pantalla (Ej: Fechas inválidas)."""
        for w in self.frame_grafico.winfo_children():
            w.destroy()
        self.lbl_titulo.configure(text="")
        for var, _, __ in self._metricas.values():
            var.set("—") # Restablece los KPIs a guiones por seguridad de datos faltantes
        tk.Label(self.frame_grafico, text=mensaje,
                 fg="#EF5350", bg="#1A1A1E", # fg="#EF5350" es un tono de color rojo alerta suave
                 font=("Segoe UI", 12), justify="center",
                 wraplength=600,
                 ).place(relx=0.5, rely=0.5, anchor="center")

    def obtener_filtros(self):
        """
        MÉTODO DE EXTRACCIÓN: Examina minuciosamente cada elemento visual de la UI,
        recolecta los estados actuales y devuelve un Diccionario estructurado hacia el controlador.
        """
        animales = []
        if self.var_perro.get(): animales.append("Perro")
        if self.var_gato.get():  animales.append("Gato")

        estados = []
        if self.var_pendiente.get():  estados.append("Pendiente")
        if self.var_en_curso.get():   estados.append("En curso")
        if self.var_completada.get(): estados.append("Completada")
        if self.var_cancelada.get():  estados.append("Cancelada")

        # Retorna el paquete listo con la configuración elegida por el usuario administrador
        return {
            "tipo_grafico": self.var_grafico.get(),
            "animales":     animales,
            "estados":      estados,
            "fecha_ini":    self.entry_fecha_ini.get().strip(), # .strip() remueve espacios accidentales
            "fecha_fin":    self.entry_fecha_fin.get().strip(),
        }

    # ==========================================================================
    # DISPARADORES DE ACCIONES (Llaman funciones del controlador)
    # ==========================================================================
    def _solicitar_grafico(self):
        """Acción intermedia ejecutada por el botón de visualización."""
        # Delega la responsabilidad de generar datos al controlador pasándole los filtros actuales
        self.controlador.generar_grafico(self.obtener_filtros())

    def _exportar_png(self):
        """Acción intermedia ejecutada por el botón de guardar archivo."""
        # Ordena al controlador que guarde la imagen en el almacenamiento local
        self.controlador.exportar_png()