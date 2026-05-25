import tkinter as tk
import customtkinter as ctk
from backend.admin.gestion_reporte_controller import ReportesController
from backend.admin.gestion_medico_controller import GestionMedicosController


class ReportesVentana:
    def __init__(self, ventana, datos_usuario):
        self.ventana       = ventana
        self.datos_usuario = datos_usuario
        self._fig_actual   = None

        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico")
        self.ventana.title("SystemVet - Panel de Reportes Estadísticos")
        self.ventana.configure(bg="#1A1A1E", bd=0)

        self._construir_header(datos_usuario)
        self._construir_cuerpo()

        self.controlador = ReportesController(self)

    # ==========================================================================
    # HEADER — mismo patrón que el resto de vistas del sistema
    # ==========================================================================
    def _construir_header(self, datos_usuario):
        self.header = tk.Frame(self.ventana, bg="#45A29E")
        self.header.pack(side="top", fill="x", ipady=2)

        self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2)
        self.btn_regresar = tk.Button(
            self.header,
            image=self.image_logo,
            bg="#45A29E", activebackground="#45A29E",
            bd=0, cursor="hand2",
            width=70, height=70,
            command=lambda: GestionMedicosController.regresar_ventana(
                self.ventana, datos_usuario)
        )
        self.btn_regresar.image = self.image_logo
        self.btn_regresar.pack(side="left", padx=20, pady=10)

        contenedor_titulo = tk.Frame(self.header, bg="#45A29E")
        contenedor_titulo.pack(side="left")

        tk.Label(contenedor_titulo, text="System Vet",
                 fg="white", bg="#45A29E",
                 font=("Segoe UI", 11, "bold")).pack(side="top", anchor="w")
        tk.Label(contenedor_titulo, text="GESTIÓN DE REPORTES ESTADÍSTICOS",
                 fg="white", bg="#45A29E",
                 font=("Segoe UI", 15, "bold")).pack(side="top", anchor="w")

        avatar = ("image/avatar_masculino.png"
                  if datos_usuario["sexo"] == "Masculino"
                  else "image/avatar_femenino.png")
        img_original      = tk.PhotoImage(file=avatar)
        self.image_avatar = img_original.subsample(2, 2)
        lbl_avatar = tk.Label(self.header, bg="#45A29E", image=self.image_avatar)
        lbl_avatar.image = self.image_avatar
        lbl_avatar.pack(side="right", padx=(0, 20))

        container_usuario = tk.Frame(self.header, bg="#45A29E")
        container_usuario.pack(side="right", padx=20)

        tk.Label(container_usuario,
                 text=f"{datos_usuario['nombre']} {datos_usuario['apellido']}",
                 bg="#45A29E", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")

        fila_nombre = tk.Frame(container_usuario, bg="#45A29E")
        fila_nombre.pack(side="top", anchor="e")

        rol = "Administrador" if datos_usuario["sexo"] == "Masculino" else "Administradora"
        tk.Label(fila_nombre, text=rol,
                 bg="#45A29E", fg="white",
                 font=("Segoe UI", 13)).pack(side="left", padx=(0, 5))

        tk.Button(fila_nombre, text="|  Cerrar sesión",
                  bg="#45A29E", fg="white",
                  font=("Segoe UI", 12, "bold"),
                  borderwidth=0, cursor="hand2",
                  command=lambda: GestionMedicosController.cerrar_sesion(
                      self.ventana)
                  ).pack(side="left")

    # ==========================================================================
    # CUERPO
    # ==========================================================================
    def _construir_cuerpo(self):
        cuerpo = tk.Frame(self.ventana, bg="#1A1A1E")
        cuerpo.pack(fill="both", expand=True)
        self._construir_sidebar(cuerpo)
        self._construir_area_grafico(cuerpo)

    # ==========================================================================
    # SIDEBAR DE FILTROS
    # ==========================================================================
    def _construir_sidebar(self, parent):
        # Frame con scroll por si los filtros no caben
        sb = tk.Frame(parent, bg="#1E1E24", width=240)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # ── Título ─────────────────────────────────────────────────────────────
        tk.Label(sb, text="PANEL DE FILTROS",
                 fg="#45A29E", bg="#1E1E24",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(16, 2))

        fila_t = tk.Frame(sb, bg="#1E1E24")
        fila_t.pack(fill="x", padx=18, pady=(0, 10))
        tk.Label(fila_t, text="📊  FILTROS DE REPORTE",
                 fg="#E8E8EC", bg="#1E1E24",
                 font=("Segoe UI", 12, "bold")).pack(side="left")

        self._separador(sb)

        # ── Tipo de gráfico ────────────────────────────────────────────────────
        self._titulo_filtro(sb, "Tipo de Gráfico:")
        self.var_grafico = tk.StringVar(value="Histograma por Estado")
        ctk.CTkOptionMenu(
            sb,
            values=[
                "Histograma por Estado",
                "Línea de Tendencia",
                "Barras por Médico",
                "Dona por Estado",
            ],
            variable=self.var_grafico,
            fg_color="#242429",
            button_color="#45A29E",
            button_hover_color="#3a8a87",
            text_color="#E8E8EC",
            font=("Segoe UI", 11),
            width=204,
            dynamic_resizing=False,
        ).pack(padx=18, pady=(0, 14), anchor="w")

        self._separador(sb)

        # ── Checkboxes: Tipo de animal ─────────────────────────────────────────
        self._titulo_filtro(sb, "Tipo de Animal:")

        self.var_perro = tk.BooleanVar(value=True)
        self.var_gato  = tk.BooleanVar(value=False)

        fila_animales = tk.Frame(sb, bg="#1E1E24")
        fila_animales.pack(fill="x", padx=18, pady=(0, 14))

        self._checkbox(fila_animales, "🐕  Perro", self.var_perro, "#45A29E")
        self._checkbox(fila_animales, "🐈  Gato",  self.var_gato,  "#CE93D8")

        self._separador(sb)

        # ── Checkboxes: Estado de citas ────────────────────────────────────────
        self._titulo_filtro(sb, "Estado de Citas:")

        self.var_pendiente  = tk.BooleanVar(value=True)
        self.var_en_curso   = tk.BooleanVar(value=False)
        self.var_completada = tk.BooleanVar(value=True)
        self.var_cancelada  = tk.BooleanVar(value=False)

        estados_frame = tk.Frame(sb, bg="#1E1E24")
        estados_frame.pack(fill="x", padx=18, pady=(0, 14))

        self._checkbox(estados_frame, "⏳  Pendiente",  self.var_pendiente,  "#66BB6A")
        self._checkbox(estados_frame, "🔄  En curso",   self.var_en_curso,   "#45A29E")
        self._checkbox(estados_frame, "✅  Completada", self.var_completada, "#8BA5BE")
        self._checkbox(estados_frame, "❌  Cancelada",  self.var_cancelada,  "#EF5350")

        self._separador(sb)

        # ── Fechas ────────────────────────────────────────────────────────────
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

        # ── Botones ───────────────────────────────────────────────────────────
        ctk.CTkButton(
            sb,
            text="📊  Visualizar Gráfico",
            fg_color="#45A29E", hover_color="#3a8a87",
            text_color="#111114",
            font=("Segoe UI", 12, "bold"),
            height=42, corner_radius=10, cursor="hand2",
            command=self._solicitar_grafico,
        ).pack(fill="x", padx=18, pady=(12, 8))

        ctk.CTkButton(
            sb,
            text="💾  Exportar PNG",
            fg_color="transparent",
            hover_color="#242429",
            border_color="#3A3A40",
            border_width=1,
            text_color="#8BA5BE",
            font=("Segoe UI", 11),
            height=36, corner_radius=10, cursor="hand2",
            command=self._exportar_png,
        ).pack(fill="x", padx=18)

    # ==========================================================================
    # ÁREA DERECHA: métricas + título + canvas
    # ==========================================================================
    def _construir_area_grafico(self, parent):
        area = tk.Frame(parent, bg="#1A1A1E")
        area.pack(side="left", fill="both", expand=True)

        # Sub-header
        sub = tk.Frame(area, bg="#242429", pady=10)
        sub.pack(fill="x")
        tk.Label(sub, text="📊  Visualización del Reporte",
                 fg="#E8E8EC", bg="#242429",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20)
        tk.Frame(area, bg="#45A29E", height=2).pack(fill="x")

        # ── Fila de métricas ──────────────────────────────────────────────────
        frame_m = tk.Frame(area, bg="#1A1A1E")
        frame_m.pack(fill="x", padx=20, pady=(14, 0))

        self._metricas = {
            "total":    (tk.StringVar(value="—"), "Total citas",     "#45A29E"),
            "animales": (tk.StringVar(value="—"), "Tipos filtrados", "#CE93D8"),
            "pico":     (tk.StringVar(value="—"), "Pico diario",     "#FFB300"),
        }
        for var, lbl, color in self._metricas.values():
            card = tk.Frame(frame_m, bg="#242429",
                            padx=16, pady=8,
                            highlightbackground="#2A2A30",
                            highlightthickness=1)
            card.pack(side="left", padx=(0, 10))
            tk.Label(card, textvariable=var, fg=color, bg="#242429",
                     font=("Segoe UI", 20, "bold")).pack()
            tk.Label(card, text=lbl, fg="#6A6A72", bg="#242429",
                     font=("Segoe UI", 9)).pack()

        # Título dinámico
        self.lbl_titulo = tk.Label(area, text="",
                                   fg="#8BA5BE", bg="#1A1A1E",
                                   font=("Segoe UI", 11),
                                   wraplength=860, justify="center")
        self.lbl_titulo.pack(pady=(10, 2))

        # Frame del canvas matplotlib
        self.frame_grafico = tk.Frame(area, bg="#1A1A1E")
        self.frame_grafico.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        self._placeholder()

    # ==========================================================================
    # HELPERS DE CONSTRUCCIÓN
    # ==========================================================================
    def _separador(self, parent):
        tk.Frame(parent, bg="#2A2A30", height=1).pack(fill="x", padx=18, pady=(0, 12))

    def _titulo_filtro(self, parent, texto):
        tk.Label(parent, text=texto,
                 fg="#E8E8EC", bg="#1E1E24",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=18, pady=(0, 6))

    def _checkbox(self, parent, texto, variable, color_activo):
        """Checkbox personalizado con el tema oscuro del sistema."""
        fila = tk.Frame(parent, bg="#1E1E24")
        fila.pack(fill="x", pady=3)

        # Canvas cuadrado que actúa como checkbox
        size = 16
        cv = tk.Canvas(fila, width=size, height=size,
                       bg="#1E1E24", highlightthickness=0, cursor="hand2")
        cv.pack(side="left", padx=(0, 8))

        lbl = tk.Label(fila, text=texto,
                       bg="#1E1E24", fg="#C8C8D0",
                       font=("Segoe UI", 11), cursor="hand2")
        lbl.pack(side="left")

        def _dibujar():
            cv.delete("all")
            if variable.get():
                cv.create_rectangle(0, 0, size, size,
                                    fill=color_activo, outline=color_activo, width=0)
                cv.create_text(size // 2, size // 2, text="✓",
                               fill="#111114", font=("Segoe UI", 10, "bold"))
                lbl.configure(fg="#E8E8EC")
            else:
                cv.create_rectangle(0, 0, size, size,
                                    fill="#242429", outline="#3A3A40", width=1)
                lbl.configure(fg="#6A6A72")

        def _toggle(event=None):
            variable.set(not variable.get())
            _dibujar()

        cv.bind("<Button-1>", _toggle)
        lbl.bind("<Button-1>", _toggle)
        _dibujar()

    def _placeholder(self):
        for w in self.frame_grafico.winfo_children():
            w.destroy()
        tk.Label(
            self.frame_grafico,
            text="Selecciona los filtros y presiona\n'Visualizar Gráfico' para generar el reporte",
            fg="#3A3A44", bg="#1A1A1E",
            font=("Segoe UI", 13), justify="center",
        ).place(relx=0.5, rely=0.5, anchor="center")

    # ==========================================================================
    # API PÚBLICA PARA EL CONTROLADOR
    # ==========================================================================
    def mostrar_canvas(self, fig, titulo, metricas):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        for w in self.frame_grafico.winfo_children():
            w.destroy()

        self.lbl_titulo.configure(text=titulo)
        self._metricas["total"][0].set(str(metricas.get("total", "—")))
        self._metricas["animales"][0].set(str(metricas.get("animales", "—")))
        self._metricas["pico"][0].set(str(metricas.get("pico", "—")))

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._fig_actual = fig

    def mostrar_error(self, mensaje):
        for w in self.frame_grafico.winfo_children():
            w.destroy()
        self.lbl_titulo.configure(text="")
        for var, _, __ in self._metricas.values():
            var.set("—")
        tk.Label(self.frame_grafico, text=mensaje,
                 fg="#EF5350", bg="#1A1A1E",
                 font=("Segoe UI", 12), justify="center",
                 wraplength=600,
                 ).place(relx=0.5, rely=0.5, anchor="center")

    def obtener_filtros(self):
        """Devuelve un dict con todos los filtros seleccionados."""
        animales = []
        if self.var_perro.get():
            animales.append("Perro")
        if self.var_gato.get():
            animales.append("Gato")

        estados = []
        if self.var_pendiente.get():
            estados.append("Pendiente")
        if self.var_en_curso.get():
            estados.append("En curso")
        if self.var_completada.get():
            estados.append("Completada")
        if self.var_cancelada.get():
            estados.append("Cancelada")

        return {
            "tipo_grafico": self.var_grafico.get(),
            "animales":     animales,
            "estados":      estados,
            "fecha_ini":    self.entry_fecha_ini.get().strip(),
            "fecha_fin":    self.entry_fecha_fin.get().strip(),
        }

    # ==========================================================================
    # ACCIONES
    # ==========================================================================
    def _solicitar_grafico(self):
        self.controlador.generar_grafico(self.obtener_filtros())

    def _exportar_png(self):
        self.controlador.exportar_png()