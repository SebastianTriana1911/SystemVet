import customtkinter as ctk
import tkinter as tk
from backend.admin.gestion_medico_controller import GestionMedicosController


class GestionMedicosVentana:
    def __init__(self, ventana, datos_usuario):
        # ==========================================================================
        # VARIABLES DE INSTANCIA
        # Se guardan la ventana principal y los datos del usuario logueado para
        # poder usarlos en cualquier método de la clase sin tener que pasarlos
        # como parámetro cada vez.
        # ==========================================================================
        self.ventana       = ventana
        self.datos_usuario = datos_usuario

        # ==========================================================================
        # CONTADORES REACTIVOS (tk.IntVar)
        # Estas variables especiales de tkinter están vinculadas directamente a los
        # labels de las stat cards del subheader. Cuando el controlador llama
        # .set(nuevo_valor) sobre cualquiera de ellas, el número en pantalla se
        # actualiza automáticamente sin necesidad de reescribir el label.
        # Se ven en pantalla como los cuatro chips numéricos: Total, Masculino,
        # Femenino y Citas hoy.
        # ==========================================================================
        self.contador_total     = tk.IntVar(value=0)
        self.contador_masculino = tk.IntVar(value=0)
        self.contador_femenino  = tk.IntVar(value=0)
        self.contador_citas_hoy = tk.IntVar(value=0)

        # ==========================================================================
        # CONFIGURACIÓN DE LA VENTANA PRINCIPAL
        # Se aplica el tema oscuro de customtkinter, el ícono de la app, el título
        # que aparece en la barra del sistema operativo y el color de fondo base.
        # ==========================================================================
        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico")
        self.ventana.title("SystemVet - Gestión de Médicos")
        self.ventana.configure(bg="#1A1A1E", bd=0)

        # ==========================================================================
        # CONSTRUCCIÓN DE LA INTERFAZ
        # Se llaman los métodos en orden de arriba hacia abajo en la pantalla.
        # Es crítico que el controlador se instancie AL FINAL, porque necesita
        # que todos los widgets ya existan (area_cards, panel_citas, contadores)
        # para poder manipularlos.
        # ==========================================================================
        self._construir_header(datos_usuario)   # Barra teal superior
        self._construir_subheader()             # Sección de título + stats + botón registrar
        self._construir_cuerpo()               # Grid de cards + panel lateral de citas

        # Controlador: lee el JSON y el CSV, dibuja las cards y actualiza contadores
        self.controlador = GestionMedicosController(self)
        self.controlador.cargar_cards()        # Dibuja una card por cada médico activo
        self.controlador.cargar_citas_hoy()    # Actualiza el contador "Citas hoy"


    # ==========================================================================
    # HEADER
    # Barra horizontal teal (#45A29E) en la parte superior de la ventana.
    # Contiene de izquierda a derecha:
    #   - Botón con el logo (al hacer clic regresa al home del administrador)
    #   - Subtítulo "System Vet" + título "GESTIÓN DE MÉDICOS"
    #   - Nombre del usuario logueado + rol + botón cerrar sesión
    #   - Avatar del usuario (imagen según sexo)
    # ==========================================================================
    def _construir_header(self, datos_usuario):
        self.header = tk.Frame(self.ventana, bg="#45A29E")
        self.header.pack(side="top", fill="x")

        # Botón logo: al presionarlo llama al método estático regresar_ventana
        # del controlador, que destruye esta ventana y abre HomeVentana
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
        self.btn_regresar.image = self.image_logo  # Evita que el GC elimine la imagen
        self.btn_regresar.pack(side="left", padx=20, pady=10)

        # Contenedor de los dos títulos apilados verticalmente a la derecha del logo
        contenedor_titulo = tk.Frame(self.header, bg="#45A29E")
        contenedor_titulo.pack(side="left")
        tk.Label(contenedor_titulo, text="System Vet",
                 fg="#d0edeb", bg="#45A29E",
                 font=("Segoe UI", 11, "bold")).pack(side="top", anchor="w")
        tk.Label(contenedor_titulo, text="GESTIÓN DE MÉDICOS",
                 fg="white", bg="#45A29E",
                 font=("Segoe UI", 15, "bold")).pack(side="top", anchor="w")

        # Avatar: imagen distinta según el sexo del administrador logueado
        avatar    = "image/avatar_masculino.png" if datos_usuario["sexo"] == "Masculino" else "image/avatar_femenino.png"
        rol_texto = "Administrador"              if datos_usuario["sexo"] == "Masculino" else "Administradora"

        img_original      = tk.PhotoImage(file=avatar)
        self.image_avatar = img_original.subsample(2, 2)
        lbl_avatar        = tk.Label(self.header, bg="#45A29E", image=self.image_avatar)
        lbl_avatar.image  = self.image_avatar   # Retener referencia
        lbl_avatar.pack(side="right", padx=(0, 20))

        # Contenedor derecho: nombre, rol y botón cerrar sesión apilados
        container_usuario = tk.Frame(self.header, bg="#45A29E")
        container_usuario.pack(side="right", padx=20)
        tk.Label(container_usuario,
                 text=f"{datos_usuario['nombre']} {datos_usuario['apellido']}",
                 bg="#45A29E", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")

        fila_nombre = tk.Frame(container_usuario, bg="#45A29E")
        fila_nombre.pack(side="top", anchor="e")
        tk.Label(fila_nombre, text=f"{rol_texto}    |",
                 bg="#45A29E", fg="#d0edeb",
                 font=("Segoe UI", 11)).pack(side="left")

        # Botón cerrar sesión: llama al método estático que pregunta confirmación,
        # destruye la ventana y relanza el login desde main.py
        tk.Button(fila_nombre, text=" Cerrar sesión",
                  bg="#45A29E", fg="white",
                  font=("Segoe UI", 11, "bold"),
                  borderwidth=0, cursor="hand2",
                  command=lambda: GestionMedicosController.cerrar_sesion(self.ventana)
                  ).pack(side="left")


    # ==========================================================================
    # SUBHEADER
    # Banda oscura (#242429) debajo del header. Contiene dos columnas:
    #
    # Columna izquierda:
    #   - Eyebrow "PANEL DE CONTROL" en teal
    #   - Título grande "Médicos registrados"
    #   - Subtítulo de instrucción
    #
    # Columna derecha:
    #   - Cuatro stat cards (Total, Masculino, Femenino, Citas hoy)
    #   - Botón "+ Registrar médico"
    #
    # Las stat cards usan textvariable= vinculado a los IntVar del __init__,
    # por eso se actualizan solas cuando el controlador llama .set().
    # ==========================================================================
    def _construir_subheader(self):
        subheader = tk.Frame(self.ventana, bg="#242429", padx=30, pady=14)
        subheader.pack(fill="x")

        # --- Columna izquierda: títulos ---
        col_izq = tk.Frame(subheader, bg="#242429")
        col_izq.pack(side="left")
        tk.Label(col_izq, text="PANEL DE CONTROL",
                 fg="#45A29E", bg="#242429",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(col_izq, text="Médicos registrados",
                 fg="#E8E8EC", bg="#242429",
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(col_izq,
                 text="Haz clic en una tarjeta para ver las citas asignadas",
                 fg="white", bg="#242429",
                 font=("Segoe UI", 11)).pack(anchor="w")

        # --- Columna derecha: stats + botón ---
        col_der = tk.Frame(subheader, bg="#242429")
        col_der.pack(side="right")

        fila_stats = tk.Frame(col_der, bg="#242429")
        fila_stats.pack(anchor="e", pady=(0, 8))

        # Función interna que fabrica cada stat card.
        # Recibe la variable IntVar y la vincula con textvariable= para que
        # el número sea reactivo. El color del número varía por card:
        # teal para total/masculino, lavanda para femenino, amarillo para citas.
        def crear_stat_card(parent, variable, etiqueta, color_num):
            card = ctk.CTkFrame(parent,
                                fg_color="#1A1A1E",
                                border_color="#45A29E",
                                border_width=1,
                                corner_radius=10)
            card.pack(side="left", padx=4)
            ctk.CTkLabel(card, textvariable=variable,
                         text_color=color_num, width=50,
                         font=("Segoe UI", 22, "bold")).pack(padx=18, pady=(10, 2))
            ctk.CTkLabel(card, text=etiqueta,
                         text_color="#E8E8EC",
                         font=("Segoe UI", 12, "bold")).pack(padx=18, pady=(0, 10))

        crear_stat_card(fila_stats, self.contador_total,     "Total",     "#45A29E")
        crear_stat_card(fila_stats, self.contador_masculino, "Masculino", "#45A29E")
        crear_stat_card(fila_stats, self.contador_femenino,  "Femenino",  "#CE93D8")
        crear_stat_card(fila_stats, self.contador_citas_hoy, "Citas hoy", "#FFB300")

        # Botón registrar: abre RegistroMedicoView como ventana emergente.
        # Pasa self.controlador para que al guardar pueda llamar cargar_cards()
        # y refrescar la vista sin reiniciar la aplicación.
        self.btn_registrar = ctk.CTkButton(
            col_der,
            text="+ Registrar médico",
            fg_color="#45A29E", hover_color="#3a8a87",
            text_color="#111114",
            font=("Segoe UI", 13, "bold"),
            height=40, corner_radius=8, cursor="hand2",
            command=lambda: GestionMedicosController.abrir_formulario_registro(
                self.ventana, self.controlador)
        )
        self.btn_registrar.pack(anchor="e")

        # Línea decorativa teal de 2px que separa el subheader del cuerpo
        tk.Frame(self.ventana, bg="#45A29E", height=2).pack(fill="x")


    # ==========================================================================
    # CUERPO
    # El cuerpo ocupa todo el espacio restante de la ventana y se divide en dos:
    #
    # IZQUIERDA (contenedor_izq, expansible):
    #   Puede mostrar dos cosas mutuamente excluyentes:
    #   - area_cards: CTkScrollableFrame con el grid 2x2 de tarjetas de médicos
    #   - frame_reasignacion: Frame que muestra el listado de médicos destino
    #     cuando el usuario quiere reasignar una cita. Se alterna entre ambos
    #     con _mostrar_area_cards() y _mostrar_frame_reasignacion().
    #
    # DERECHA (panel_citas, ancho fijo 300px):
    #   Panel lateral que muestra las citas del médico seleccionado.
    #   Al inicio está vacío (_construir_panel_vacio).
    #   Se actualiza cada vez que el usuario hace clic en una card.
    # ==========================================================================
    def _construir_cuerpo(self):
        self.cuerpo = tk.Frame(self.ventana, bg="#1A1A1E")
        self.cuerpo.pack(fill="both", expand=True)

        # Contenedor izquierdo: aloja area_cards O frame_reasignacion
        self.contenedor_izq = tk.Frame(self.cuerpo, bg="#1A1A1E")
        self.contenedor_izq.pack(side="left", fill="both", expand=True, pady=10)

        # Grid de cards scrollable — visible por defecto
        self.area_cards = ctk.CTkScrollableFrame(
            self.contenedor_izq,
            fg_color="#1A1A1E",
            scrollbar_button_color="#45A29E",
            scrollbar_button_hover_color="#3a8a87",
            corner_radius=0
        )
        self.area_cards.pack(fill="both", expand=True)
        # Dos columnas iguales para el grid 2x2 de cards
        self.area_cards.columnconfigure(0, weight=1)
        self.area_cards.columnconfigure(1, weight=1)

        # Frame de reasignación — oculto hasta que el usuario presiona
        # "Reasignar" o "Reasignación masiva". No tiene pack() aquí.
        self.frame_reasignacion = tk.Frame(self.contenedor_izq, bg="#1A1A1E")

        # Panel lateral de citas — ancho fijo, siempre visible a la derecha
        self.panel_citas = tk.Frame(self.cuerpo, bg="#111114", width=300)
        self.panel_citas.pack(side="right", fill="y")
        self.panel_citas.pack_propagate(False)  # Evita que se encoja con el contenido

        self._construir_panel_vacio()


    # ==========================================================================
    # PANEL LATERAL VACÍO
    # Estado inicial del panel_citas antes de que el usuario seleccione un médico.
    # Muestra solo el título "Citas del médico" y el mensaje de instrucción.
    # También se llama después de eliminar un médico para limpiar el panel.
    # El bucle for w.destroy() limpia cualquier contenido previo del panel.
    # ==========================================================================
    def _construir_panel_vacio(self):
        for w in self.panel_citas.winfo_children():
            w.destroy()

        header_panel = tk.Frame(self.panel_citas, bg="#111114")
        header_panel.pack(fill="x", padx=14, pady=(14, 10))
        tk.Label(header_panel, text="🗓  Citas del médico",
                 fg="#E8E8EC", bg="#111114",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Frame(self.panel_citas, bg="#2A2A30", height=1).pack(fill="x")
        tk.Label(self.panel_citas,
                 text="Selecciona algun medico\npara ver sus citas",
                 fg="#4A4A52", bg="#111114",
                 font=("Segoe UI", 12, "bold"),
                 justify="center").pack(expand=True)


    # ==========================================================================
    # ALTERNAR ENTRE CARDS Y REASIGNACIÓN
    # Estos dos métodos controlan qué se muestra en el contenedor_izq.
    # pack_forget() oculta el widget sin destruirlo (se puede volver a mostrar).
    # pack() lo vuelve a mostrar.
    # Se usan cuando el usuario presiona Reasignar (oculta cards, muestra lista)
    # y cuando cancela o confirma (oculta lista, muestra cards).
    # ==========================================================================
    def _mostrar_area_cards(self):
        self.frame_reasignacion.pack_forget()
        self.area_cards.pack(fill="both", expand=True)

    def _mostrar_frame_reasignacion(self):
        self.area_cards.pack_forget()
        self.frame_reasignacion.pack(fill="both", expand=True)


    # ==========================================================================
    # AGREGAR CARD DE MÉDICO
    # El controlador llama este método una vez por cada médico activo encontrado
    # en el JSON. Construye una tarjeta (CTkFrame) y la ubica en el grid con
    # card.grid(row=fila, column=columna).
    #
    # Cada card contiene de arriba a abajo:
    #   - Franja amarilla lateral (solo si tiene citas activas)
    #   - Avatar circular con iniciales + nombre + especialidad
    #   - Separador
    #   - Grid 2x2 de campos: NIT, Sexo (badge), Teléfono, Contraseña
    #   - Separador
    #   - Footer: círculo con número de citas + botones Editar y Borrar
    #
    # Colores dinámicos según sexo:
    #   Masculino → azul oscuro (#18314B) con texto teal (#45A29E)
    #   Femenino  → púrpura oscuro (#5B1E5F) con texto lavanda (#E19DED)
    #
    # Botón borrar tiene dos estados:
    #   - Con citas: bloqueado visualmente (color apagado), llama iniciar_flujo_baja
    #   - Sin citas: rojo activo, llama eliminar_medico directamente
    #
    # El bind("<Button-1>") en los sub-frames hace que al hacer clic en cualquier
    # parte de la card (excepto los botones) se carguen las citas en el panel lateral.
    # ==========================================================================
    def agregar_card(self, nit, nombre, apellido, sexo, telefono, especialidad,
                     num_citas, fila, columna):

        es_masculino      = sexo == "Masculino"
        color_avatar_bg   = "#18314B" if es_masculino else "#5B1E5F"
        color_avatar_text = "#45A29E" if es_masculino else "#E19DED"
        color_badge_bg    = "#18314B" if es_masculino else "#5B1E5F"
        color_badge_text  = "#45A29E" if es_masculino else "#E19DED"
        icono_sexo        = "♂ Masc." if es_masculino else "♀ Fem."
        tiene_citas       = num_citas > 0

        # Frame principal de la card ubicado en el grid del area_cards
        card = ctk.CTkFrame(self.area_cards,
                            fg_color="#242429",
                            border_color="#2A2A30",
                            border_width=1,
                            corner_radius=12)
        card.grid(row=fila, column=columna, padx=10, pady=8, sticky="nsew")

        # Franja amarilla de 3px en el borde izquierdo: indica que el médico
        # tiene citas activas y NO puede eliminarse directamente
        if tiene_citas:
            tk.Frame(card, bg="#FFB300", width=3).pack(side="left", fill="y")

        contenido = tk.Frame(card, bg="#242429")
        contenido.pack(fill="both", expand=True, padx=14, pady=12)

        # --- TOP: avatar + nombre + especialidad ---
        top = tk.Frame(contenido, bg="#242429")
        top.pack(fill="x", pady=(0, 10))

        iniciales = f"{nombre[0]}{apellido[0]}".upper()
        av = ctk.CTkFrame(top, fg_color=color_avatar_bg,
                          width=42, height=42, corner_radius=21)
        av.pack(side="left")
        av.pack_propagate(False)
        ctk.CTkLabel(av, text=iniciales, text_color=color_avatar_text,
                     font=("Segoe UI", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        info = tk.Frame(top, bg="#242429")
        info.pack(side="left", padx=(10, 0))
        tk.Label(info, text=f"{nombre} {apellido}",
                 fg="#E8E8EC", bg="#242429",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        tk.Label(info, text=f"⚕ {especialidad}",
                 fg="#45A29E", bg="#242429",
                 font=("Segoe UI", 11)).pack(anchor="w")

        tk.Frame(contenido, bg="#2A2A30", height=1).pack(fill="x", pady=(0, 8))

        # --- CAMPOS: NIT, Sexo, Teléfono, Contraseña en grid 2x2 ---
        grid_campos = tk.Frame(contenido, bg="#242429")
        grid_campos.pack(fill="x", pady=(0, 10))
        grid_campos.columnconfigure(0, weight=1)
        grid_campos.columnconfigure(1, weight=1)

        # Función interna para crear cada campo del grid.
        # es_badge=True crea el chip de color para el sexo en vez de texto plano.
        def campo(parent, etiqueta, valor, fila_g, col_g, es_badge=False):
            f = tk.Frame(parent, bg="#242429")
            f.grid(row=fila_g, column=col_g, sticky="w", pady=3, padx=(0, 8))
            tk.Label(f, text=etiqueta, fg="white", bg="#242429",
                     font=("Segoe UI", 10)).pack(anchor="w")
            if es_badge:
                badge = ctk.CTkFrame(f, fg_color=color_badge_bg,
                                     corner_radius=10, width=72, height=25)
                badge.pack(anchor="w")
                badge.pack_propagate(False)
                ctk.CTkLabel(badge, text=icono_sexo, text_color=color_badge_text,
                             font=("Segoe UI", 11, "bold")).place(relx=0.5, rely=0.5, anchor="center")
            else:
                tk.Label(f, text=valor, fg="#C8C8D0", bg="#242429",
                         font=("Consolas", 11, "bold")).pack(anchor="w")

        campo(grid_campos, "NIT",        nit,         0, 0)
        campo(grid_campos, "Sexo",       "",          0, 1, es_badge=True)
        campo(grid_campos, "Teléfono",   telefono,    1, 0)
        campo(grid_campos, "Contraseña", "● ● ● ● ●", 1, 1)

        tk.Frame(contenido, bg="#2A2A30", height=1).pack(fill="x", pady=(0, 8))

        # --- FOOTER: contador de citas + botones ---
        footer = tk.Frame(contenido, bg="#242429")
        footer.pack(fill="x")

        # Círculo de citas: amarillo si tiene citas, verde si no tiene
        color_circulo = "#392713" if tiene_citas else "#1A2E20"
        color_num     = "#FFB300" if tiene_citas else "#4ADE80"

        citas_frame = tk.Frame(footer, bg="#242429")
        citas_frame.pack(side="left")
        circulo = ctk.CTkFrame(citas_frame, fg_color=color_circulo,
                               width=28, height=28, corner_radius=14)
        circulo.pack(side="left")
        circulo.pack_propagate(False)
        ctk.CTkLabel(circulo, text=str(num_citas), text_color=color_num,
                     font=("Segoe UI", 12, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(citas_frame,
                 text=f"  {'Citas asignadas' if tiene_citas else 'Sin citas'}",
                 fg="#6A6A72", bg="#242429",
                 font=("Segoe UI", 10, "bold")).pack(side="left")

        botones = tk.Frame(footer, bg="#242429")
        botones.pack(side="right")

        # Botón Editar: naranja, siempre activo.
        # Abre RegistroMedicoView con nit_editar=nit para precargar los datos.
        ctk.CTkButton(botones, text="✎ Editar",
                      width=80, height=30,
                      fg_color="#EC8600", hover_color="#C77100",
                      text_color="#FFFFFF",
                      font=("Segoe UI", 11, "bold"),
                      corner_radius=6, cursor="hand2",
                      command=lambda n=nit: self.controlador.abrir_formulario_edicion(n)
                      ).pack(side="left", padx=(0, 6))

        if tiene_citas:
            # Botón borrar BLOQUEADO: color apagado, sin cursor hand2.
            # Al presionar abre iniciar_flujo_baja que obliga a reasignar
            # antes de desactivar al médico.
            ctk.CTkButton(botones, text="🗑",
                          width=34, height=30,
                          fg_color="#3A2010", hover_color="#3A2010",
                          text_color="#6A4030",
                          font=("Segoe UI", 13), corner_radius=6,
                          command=lambda n=nit, nm=f"{nombre} {apellido}":
                              self.controlador.iniciar_flujo_baja(n, nm)
                          ).pack(side="left")
        else:
            # Botón borrar ACTIVO: rojo, con cursor hand2.
            # Llama eliminar_medico que pide confirmación y borra del JSON.
            ctk.CTkButton(botones, text="🗑",
                          width=34, height=30,
                          fg_color="#DD3434", hover_color="#B02020",
                          text_color="#fff",
                          font=("Segoe UI", 13), corner_radius=6, cursor="hand2",
                          command=lambda n=nit, nm=f"{nombre} {apellido}":
                              self.controlador.eliminar_medico(n, nm)
                          ).pack(side="left")

        # Bind de clic en la card: cualquier clic en los sub-frames del contenido
        # (excepto los botones que tienen su propio command) llama mostrar_citas_panel
        # pasando el nit del médico para cargar sus citas en el panel lateral.
        for widget in [contenido, top, info, grid_campos, footer, citas_frame]:
            widget.bind("<Button-1>",
                        lambda e, n=nit, nom=f"{nombre} {apellido}",
                        esp=especialidad, sx=sexo:
                        self.controlador.mostrar_citas_panel(n, nom, esp, sx))


    # ==========================================================================
    # PANEL LATERAL CON CITAS
    # Se ejecuta cuando el usuario hace clic en una card de médico.
    # Limpia el panel_citas con destroy() y lo reconstruye con:
    #   - Chip del médico seleccionado (avatar, nombre, especialidad, total citas)
    #   - Lista scrolleable de todas sus citas (todas las del CSV, no solo activas)
    #   - Por cada cita: nombre paciente, badge de estado, especie+raza, fecha+hora
    #   - Si la cita es Pendiente o En curso: botón "Reasignar" individual
    #   - Si hay citas activas: aviso amarillo + botón "Reasignación masiva"
    #
    # Al inicio llama _mostrar_area_cards() para que si estábamos en modo
    # reasignación, volvamos al grid de cards antes de actualizar el panel.
    # ==========================================================================
    def mostrar_panel_citas(self, nombre_medico, especialidad, sexo, citas):
        self._mostrar_area_cards()

        for w in self.panel_citas.winfo_children():
            w.destroy()

        es_m        = sexo == "Masculino"
        color_av_bg = "#18314B" if es_m else "#3D1040"
        color_av_tx = "#45A29E" if es_m else "#CE93D8"
        iniciales   = "".join([p[0].upper() for p in nombre_medico.split()[:2]])

        # Cabecera del panel con chip del médico
        header_panel = tk.Frame(self.panel_citas, bg="#111114")
        header_panel.pack(fill="x", padx=14, pady=(14, 10))
        tk.Label(header_panel, text="🗓  Citas del médico",
                 fg="#E8E8EC", bg="#111114",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")

        chip = ctk.CTkFrame(header_panel, fg_color="#242429",
                            border_color="#2A2A30", border_width=1, corner_radius=8)
        chip.pack(fill="x", pady=(8, 0))
        chip_inner = tk.Frame(chip, bg="#242429")
        chip_inner.pack(fill="x", padx=8, pady=8)

        av = ctk.CTkFrame(chip_inner, fg_color=color_av_bg,
                          width=32, height=32, corner_radius=16)
        av.pack(side="left")
        av.pack_propagate(False)
        ctk.CTkLabel(av, text=iniciales, text_color=color_av_tx,
                     font=("Segoe UI", 11, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        info_chip = tk.Frame(chip_inner, bg="#242429")
        info_chip.pack(side="left", padx=(8, 0))
        tk.Label(info_chip, text=nombre_medico,
                 fg="#E8E8EC", bg="#242429",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(info_chip, text=f"{especialidad} · {len(citas)} citas",
                 fg="#45A29E", bg="#242429",
                 font=("Segoe UI", 10)).pack(anchor="w")

        tk.Frame(self.panel_citas, bg="#2A2A30", height=1).pack(fill="x")

        if not citas:
            tk.Label(self.panel_citas, text="Sin citas asignadas",
                     fg="#4A4A52", bg="#111114",
                     font=("Segoe UI", 12)).pack(expand=True)
            return

        # Lista scrolleable de citas
        scroll_citas = ctk.CTkScrollableFrame(
            self.panel_citas, fg_color="#111114",
            scrollbar_button_color="#45A29E",
            scrollbar_button_hover_color="#3a8a87",
            corner_radius=0
        )
        scroll_citas.pack(fill="both", expand=True)

        # Colores de badge por estado de la cita
        COLORES_ESTADO = {
            "Pendiente":  ("#1A2E1A", "#66BB6A"),   # verde oscuro / texto verde
            "En curso":   ("#1A2030", "#45A29E"),   # azul oscuro / texto teal
            "Completada": ("#1A2030", "#8BA5BE"),   # azul oscuro / texto gris azul
            "Cancelada":  ("#2E1A1A", "#EF5350"),   # rojo oscuro / texto rojo
        }

        for cita in citas:
            estado     = cita.get("estado", "Pendiente")
            bg_e, fg_e = COLORES_ESTADO.get(estado, ("#1A2E1A", "#66BB6A"))
            # Solo las citas Pendiente o En curso se pueden reasignar
            es_activa  = estado in ("Pendiente", "En curso")

            item = tk.Frame(scroll_citas, bg="#111114")
            item.pack(fill="x", padx=10, pady=(6, 0))

            fila_top = tk.Frame(item, bg="#111114")
            fila_top.pack(fill="x")
            tk.Label(fila_top, text=cita.get("nombre_paciente", ""),
                     fg="#E8E8EC", bg="#111114",
                     font=("Segoe UI", 11, "bold")).pack(side="left")

            # Badge de estado (Pendiente / En curso / Completada / Cancelada)
            badge_e = ctk.CTkFrame(fila_top, fg_color=bg_e,
                                   corner_radius=10, width=70, height=20)
            badge_e.pack(side="right")
            badge_e.pack_propagate(False)
            ctk.CTkLabel(badge_e, text=estado, text_color=fg_e,
                         font=("Segoe UI", 10, "bold")).place(relx=0.5, rely=0.5, anchor="center")

            tipo_animal = cita.get("tipo_animal", "")
            raza        = cita.get("raza", "")
            tk.Label(item, text=f"{tipo_animal} · {raza}" if raza else tipo_animal,
                     fg="#45A29E", bg="#111114",
                     font=("Segoe UI", 10)).pack(anchor="w")
            tk.Label(item, text=f"📅 {cita.get('fecha', '')}   🕐 {cita.get('hora', '')}",
                     fg="#6A6A72", bg="#111114",
                     font=("Segoe UI", 10)).pack(anchor="w")

            # Botón Reasignar individual: solo aparece en citas activas.
            # Captura el id_cita e info_cita en el momento de creación del botón
            # (lambda con argumentos por defecto) para evitar el problema de
            # cierre de variables en bucles de Python.
            if es_activa:
                id_cita   = cita.get("id_cita", None)
                info_cita = {
                    "nombre_paciente": cita.get("nombre_paciente", ""),
                    "tipo_animal":     tipo_animal,
                    "raza":            raza,
                    "fecha":           cita.get("fecha", ""),
                    "hora":            cita.get("hora", ""),
                }
                ctk.CTkButton(
                    item, text="⇄  Reasignar",
                    height=26,
                    fg_color="#1A2E1A", hover_color="#243D24",
                    text_color="#66BB6A",
                    font=("Segoe UI", 10, "bold"),
                    corner_radius=6, cursor="hand2",
                    command=lambda ic=id_cita, inf=info_cita:
                        self.controlador.iniciar_reasignacion_individual(ic, inf)
                ).pack(anchor="w", pady=(4, 2))

            tk.Frame(scroll_citas, bg="#2A2A30", height=1).pack(fill="x", padx=10, pady=(6, 0))

        # Si hay citas activas, mostrar aviso y botón de reasignación masiva.
        # La reasignación masiva reasigna TODAS las citas activas del médico
        # a un solo médico destino de una sola vez.
        citas_activas = [c for c in citas if c.get("estado") in ("Pendiente", "En curso")]
        if citas_activas:
            aviso = ctk.CTkFrame(self.panel_citas, fg_color="#2A1E00",
                                 border_color="#3A2A00", border_width=1, corner_radius=8)
            aviso.pack(fill="x", padx=12, pady=(6, 4))
            ctk.CTkLabel(aviso,
                         text="⚠ Reasigna las citas antes\nde desactivar al médico",
                         text_color="#FFB300", font=("Segoe UI", 10),
                         justify="left").pack(padx=10, pady=8, anchor="w")

            ctk.CTkButton(
                self.panel_citas, text="⇄  Reasignación masiva",
                height=36,
                fg_color="#1E2A1E", hover_color="#243D24",
                text_color="#66BB6A",
                border_color="#2A3D2A", border_width=1,
                font=("Segoe UI", 12, "bold"),
                corner_radius=8, cursor="hand2",
                command=self.controlador.iniciar_reasignacion_masiva
            ).pack(fill="x", padx=12, pady=(0, 10))


    # ==========================================================================
    # VISTA DE REASIGNACIÓN (reemplaza el grid de cards)
    # Se activa al presionar "Reasignar" (individual) o "Reasignación masiva".
    # Oculta el area_cards y muestra frame_reasignacion con:
    #   - Encabezado: título + subtítulo + chip de la cita (solo individual)
    #   - Lista scrolleable de médicos activos disponibles (excluye al actual)
    #   - Por cada médico: avatar, nombre, especialidad, conteo de citas, checkmark
    #   - Barra inferior: botón Cancelar + botón Confirmar reasignación
    #
    # La selección funciona así:
    #   Al hacer clic en una fila, seleccionar() cambia el fondo a verde oscuro
    #   (#1A3028), muestra el checkmark (✓) y guarda el nit en _nit_seleccionado.
    #   Al hacer clic en otra fila, primero revierte la anterior y luego
    #   resalta la nueva.
    #
    # Al confirmar, on_confirmar() lee _nit_seleccionado y llama
    # controlador.confirmar_reasignacion() que actualiza el CSV y refresca la vista.
    # ==========================================================================
    def mostrar_panel_reasignacion(self, id_cita, info_cita,
                                   medicos_disponibles, es_masiva=False):
        for w in self.frame_reasignacion.winfo_children():
            w.destroy()
        self._mostrar_frame_reasignacion()

        # Variables de estado de la selección actual
        self._nit_seleccionado = tk.StringVar(value="")
        self._frames_medicos   = {}   # nit → frame de la fila (para cambiar bg)
        self._checks_labels    = {}   # nit → label del checkmark

        # --- Encabezado ---
        header = tk.Frame(self.frame_reasignacion, bg="#1A1A1E")
        header.pack(fill="x", padx=30, pady=(24, 0))

        titulo_txt = "Reasignación masiva" if es_masiva else "Reasignar cita"
        tk.Label(header, text=f"⇄  {titulo_txt}",
                 fg="#E8E8EC", bg="#1A1A1E",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")

        subtitulo = ("Todas las citas activas del médico serán reasignadas al médico que selecciones."
                     if es_masiva else
                     "Selecciona el médico que atenderá esta cita.")
        tk.Label(header, text=subtitulo,
                 fg="#6A6A72", bg="#1A1A1E",
                 font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 0))

        # Chip informativo de la cita (solo en reasignación individual)
        if not es_masiva and info_cita:
            tipo       = info_cita.get("tipo_animal", "")
            raza       = info_cita.get("raza", "")
            animal_txt = f"{tipo} · {raza}" if raza else tipo
            chip_cita  = ctk.CTkFrame(header, fg_color="#2A1E00",
                                      border_color="#3A2A00", border_width=1, corner_radius=8)
            chip_cita.pack(anchor="w", pady=(10, 0))
            ctk.CTkLabel(chip_cita,
                         text=f"🐾  {animal_txt}   📅 {info_cita.get('fecha','')}   🕐 {info_cita.get('hora','')}",
                         text_color="#FFB300",
                         font=("Segoe UI", 11, "bold")).pack(padx=14, pady=8)

        tk.Frame(self.frame_reasignacion, bg="#2A2A30", height=1).pack(fill="x", pady=(16, 0))
        tk.Label(self.frame_reasignacion, text="MÉDICOS DISPONIBLES",
                 fg="#6A6A72", bg="#1A1A1E",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=30, pady=(12, 4))

        # --- Lista scrolleable de médicos ---
        scroll = ctk.CTkScrollableFrame(
            self.frame_reasignacion, fg_color="#1A1A1E",
            scrollbar_button_color="#45A29E",
            scrollbar_button_hover_color="#3a8a87",
            corner_radius=0
        )
        scroll.pack(fill="both", expand=True, padx=20)

        if not medicos_disponibles:
            tk.Label(scroll, text="No hay médicos disponibles",
                     fg="#4A4A52", bg="#1A1A1E",
                     font=("Segoe UI", 12)).pack(pady=30)
        else:
            for medico in medicos_disponibles:
                nit_m   = medico["nit"]
                nombre  = medico["nombre"]
                esp     = medico["especialidad"]
                sexo_m  = medico["sexo"]
                n_citas = medico["num_citas"]

                es_masc   = sexo_m == "Masculino"
                av_bg     = "#18314B" if es_masc else "#3D1040"
                av_tx     = "#45A29E" if es_masc else "#CE93D8"
                iniciales = "".join([p[0].upper() for p in nombre.split()[:2]])

                # Fila del médico: se registra en _frames_medicos para cambiar su bg al seleccionar
                fila_m = tk.Frame(scroll, bg="#1A1A1E", cursor="hand2")
                fila_m.pack(fill="x", pady=2)
                self._frames_medicos[str(nit_m)] = fila_m

                contenido_m = tk.Frame(fila_m, bg="#1A1A1E")
                contenido_m.pack(fill="x", padx=10, pady=10)

                av_f = ctk.CTkFrame(contenido_m, fg_color=av_bg,
                                    width=40, height=40, corner_radius=20)
                av_f.pack(side="left")
                av_f.pack_propagate(False)
                ctk.CTkLabel(av_f, text=iniciales, text_color=av_tx,
                             font=("Segoe UI", 13, "bold")).place(relx=0.5, rely=0.5, anchor="center")

                info_m = tk.Frame(contenido_m, bg="#1A1A1E")
                info_m.pack(side="left", padx=(12, 0), fill="x", expand=True)
                tk.Label(info_m, text=nombre,
                         fg="#E8E8EC", bg="#1A1A1E",
                         font=("Segoe UI", 13, "bold")).pack(anchor="w")
                tk.Label(info_m, text=esp, fg=av_tx, bg="#1A1A1E",
                         font=("Segoe UI", 11)).pack(anchor="w")

                der_m = tk.Frame(contenido_m, bg="#1A1A1E")
                der_m.pack(side="right")
                tk.Label(der_m, text=f"{n_citas} {'cita' if n_citas == 1 else 'citas'}",
                         fg="#6A6A72", bg="#1A1A1E",
                         font=("Segoe UI", 11)).pack(side="left", padx=(0, 6))

                # Checkmark oculto por defecto; se muestra al seleccionar esta fila
                lbl_check = tk.Label(der_m, text="✓",
                                     fg="#45A29E", bg="#1A1A1E",
                                     font=("Segoe UI", 14, "bold"))
                self._checks_labels[str(nit_m)] = lbl_check

                tk.Frame(scroll, bg="#242429", height=1).pack(fill="x")

                # Función de selección: cambia el fondo de la fila seleccionada
                # a verde oscuro y revierte la anterior a negro.
                def seleccionar(event=None, n=nit_m, lc=lbl_check):
                    prev = self._nit_seleccionado.get()
                    if prev and prev in self._frames_medicos:
                        self._frames_medicos[prev].configure(bg="#1A1A1E")
                        for ch in self._iter_widgets(self._frames_medicos[prev]):
                            try: ch.configure(bg="#1A1A1E")
                            except Exception: pass
                    for chk in self._checks_labels.values():
                        chk.pack_forget()
                    self._nit_seleccionado.set(str(n))
                    self._frames_medicos[str(n)].configure(bg="#1A3028")
                    for ch in self._iter_widgets(self._frames_medicos[str(n)]):
                        try: ch.configure(bg="#1A3028")
                        except Exception: pass
                    lc.pack(side="left")

                for w in [fila_m, contenido_m, info_m, der_m]:
                    w.bind("<Button-1>", seleccionar)

        # --- Barra de botones ---
        tk.Frame(self.frame_reasignacion, bg="#2A2A30", height=1).pack(fill="x")
        barra = tk.Frame(self.frame_reasignacion, bg="#1A1A1E")
        barra.pack(fill="x", padx=30, pady=14)
        barra.columnconfigure(0, weight=1)
        barra.columnconfigure(1, weight=2)

        # Cancelar: vuelve al panel de citas del médico activo sin hacer cambios
        def cancelar():
            self.controlador.mostrar_citas_panel(
                self.controlador._nit_medico_activo,
                self.controlador._nombre_medico_activo,
                self.controlador._esp_medico_activo,
                self.controlador._sexo_medico_activo,
            )

        ctk.CTkButton(barra, text="Cancelar",
                      fg_color="#242429", hover_color="#2A2A30",
                      text_color="#8BA5BE", font=("Segoe UI", 13),
                      height=40, corner_radius=8,
                      command=cancelar
                      ).grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # Confirmar: lee el nit seleccionado y delega al controlador.
        # Si no hay selección muestra advertencia sin cerrar la vista.
        def on_confirmar():
            nit_dest = self._nit_seleccionado.get()
            if not nit_dest:
                from tkinter import messagebox
                messagebox.showwarning("Sin selección", "Selecciona un médico de la lista.")
                return
            self.controlador.confirmar_reasignacion(
                nit_destino=nit_dest,
                id_cita=id_cita,
                es_masiva=es_masiva,
            )

        ctk.CTkButton(barra, text="Confirmar reasignación",
                      fg_color="#45A29E", hover_color="#3a8a87",
                      text_color="#111114", font=("Segoe UI", 13, "bold"),
                      height=40, corner_radius=8,
                      command=on_confirmar
                      ).grid(row=0, column=1, sticky="ew")


    # ==========================================================================
    # UTILITARIO: _iter_widgets
    # Generador recursivo que recorre un widget y TODOS sus hijos en profundidad.
    # Se usa en la función seleccionar() para cambiar el color de fondo de todos
    # los sub-widgets de una fila de médico al mismo tiempo, porque en tkinter
    # configure(bg=...) solo afecta al widget en sí, no a sus hijos.
    # ==========================================================================
    def _iter_widgets(self, widget):
        yield widget
        for child in widget.winfo_children():
            yield from self._iter_widgets(child)