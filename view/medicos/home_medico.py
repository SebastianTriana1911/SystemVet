import customtkinter as ctk
import tkinter as tk
class HomeMedico():
    def _guardar_notas(self):
        """Guarda las notas en un archivo JSON"""
        import json, os
        ruta = os.path.join(os.path.dirname(__file__), "notas_guardadas.json")
        with open(ruta, "w", encoding="utf-8") as f:
                json.dump(self.notas_lista, f, ensure_ascii=False, indent=2)
    def agregar_nota(self):
        """Agrega una nota rápida a la lista"""
        nota_texto = self.entry_nota.get()
        if nota_texto.strip():
            from datetime import datetime
            hora_actual = datetime.now().strftime("%H:%M")
            self.notas_lista.append({"texto": nota_texto, "hora": hora_actual})
            self.entry_nota.delete(0, "end")
            self.mostrar_notas()
            self._guardar_notas()
    
    def mostrar_notas(self):
        """Muestra todas las notas en la lista"""
        # Limpiar notas anteriores
        for widget in self.notas_scrollable.winfo_children():
            widget.destroy()
        
        # Renderizar cada nota
        for i, nota in enumerate(self.notas_lista):
            nota_frame = ctk.CTkFrame(self.notas_scrollable,
                                      fg_color="#313131",
                                      corner_radius=15)
            nota_frame.pack(side="top", fill="x", pady=(5, 0), padx=0)
            
            # Contenido de la nota
            contenido_frame = ctk.CTkFrame(nota_frame,
                                          fg_color="#313131",
                                          corner_radius=15)
            contenido_frame.pack(side="left", fill="x", expand=True, padx=12, pady=8)
            
            # Frame para el texto
            texto_frame = ctk.CTkFrame(contenido_frame,
                                      fg_color="#313131",
                                      corner_radius=0)
            texto_frame.pack(side="left", fill="both", expand=True, anchor="w")
            
            # Texto de la nota
            tk.Label(texto_frame,
                    text=nota["texto"],
                    bg="#313131",
                    fg="white",
                    font=("Segoe UI", 10),
                    wraplength=180,
                    justify="left").pack(side="left", anchor="w", fill="x", expand=True)
            
            # Frame para la hora (tamaño fijo)
            hora_frame = ctk.CTkFrame(contenido_frame,
                                     fg_color="#313131",
                                     corner_radius=0)
            hora_frame.pack(side="right", padx=(10, 0), anchor="e")
            
            # Hora de la nota
            tk.Label(hora_frame,
                    text=nota["hora"],
                    bg="#313131",
                    fg="#8888a0",
                    font=("Segoe UI", 9)).pack(side="right", anchor="e")
    
    def limpiar_notas(self):
        """Limpia todas las notas"""
        self.notas_lista.clear()
        self.entry_nota.delete(0, "end")
        self.mostrar_notas()
    def resetear_tareas(self):
        """Resetea todas las tareas completadas"""
        for var in self.tareas_completadas.values():
            var.set(False)
        self.actualizar_progreso()
    def actualizar_progreso(self):
        """Actualiza la barra de progreso según las tareas completadas"""
        tareas_hechas = sum(1 for var in self.tareas_completadas.values() if var.get())
        total_tareas = len(self.tareas)
        
        porcentaje = (tareas_hechas / total_tareas * 100) if total_tareas > 0 else 0
        valor_barra = tareas_hechas / total_tareas if total_tareas > 0 else 0
        
        self.progress_bar.set(valor_barra)
        self.label_porcentaje.configure(text=f"{int(porcentaje)}%")
    def __init__(self, datos_usuario):
        self.datos_usuario = datos_usuario
    


        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DE LA VENTANA ─────────────────────────────────────────────────────
        # ========================================================================================================
        self.ventana = ctk.CTk()
        ctk.set_appearance_mode("dark")
        self.ventana.iconbitmap("image/huella_icono.ico") # Se muesta en ventana un icono
        self.ventana.title("SystemVet / Gestión de Administradores")
        self.ventana.configure(bg="black", bd=10)


        self.ventana.after(0, lambda: self.ventana.state('zoomed'))
        # ----------------------------------------------------



        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DEL ENCABEZADO ────────────────────────────────────────────────────
        # ========================================================================================================
        self.header = tk.Frame(self.ventana,
                                bg="#45A29E",)
        self.header.pack(side="top",
                          fill="x") # Mantiene el 100% del ancho en la pantalla
        
        self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2) # Acceder a la imagen
        image_logo = self.image_logo
        image_logo = tk.Label(self.header,
                                  bg="#45A29E",
                                  width=70,
                                  height=70,
                                    image=self.image_logo)
        image_logo.image = self.image_logo
        image_logo.pack(side="left", padx=20, pady=10)

        tk.Label(self.header,
                  text="Home Medico",
                    fg="white", 
                     bg="#45A29E", 
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
                                 bg="#45A29E", 
                                  image=self.image_avatar,)
        image_avatar.image = self.image_avatar
        image_avatar.pack(side="right", padx=(0,20))

        # Este contenedor permitira acomodar dos Label arriba y abajo
        self.container_usuario = tk.Frame(self.header,
                                           bg="#45A29E")
        self.container_usuario.pack(side="right", padx=20)
        
        # Etiqueta "Administrador" parte superior
        if datos_usuario["sexo"] == "Masculino":
            tk.Label(self.container_usuario,
                     text="Medico",
                      bg="#45A29E",
                      fg="white",
                       font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")
        else:
            tk.Label(self.container_usuario,
                     text="Administradora",
                      bg="#45A29E",
                      fg="white",
                       font=("Segoe UI", 13, "bold")).pack(side="top", anchor="e")
        
        # Contenedor que organiza el nombre del usuario y el boton de manera horizontal
        self.fila_nombre = tk.Frame(self.container_usuario,
                                     bg="#45A29E")
        self.fila_nombre.pack(side="top", anchor="e")
        
        # Nombre del usuario en la parte izquierda
        tk.Label(self.fila_nombre,
                   text=f"{datos_usuario['nombre']} {datos_usuario["apellido"]}    | ",
                    bg="#45A29E",
                     fg="white", 
                      font=("Segoe UI", 13)).pack(side="left", padx=(0, 5))
        
        # Botón Cerrar Sesión (Al lado del nombre)
        self.btn_cerrar_sesion = tk.Button(self.fila_nombre, 
                                            text="Cerrar sesión", 
                                             bg="#45A29E", 
                                                fg="white",
                                                 font=("Segoe UI", 12, "bold"),                                                  
                                                  borderwidth=0,
                                                   cursor="hand2",
                                                   # command= lamb1150184811
                                                   # da:GestionAdminController.cerrar_sesion(self.ventana) # Cambia el cursor al pasar por encima
                                           )
        self.btn_cerrar_sesion.pack(side="left")

        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DE LA BIENVENIDA ─────────────────────────────────────────────────────
        # ========================================================================================================

        # Contenedor principal con fondo
        self.welcome_container = tk.Frame(self.ventana, bg="#242424")
        self.welcome_container.pack(side="top", fill="x", padx=20, pady=(20, 0))
        
        # Frame con esquinas redondeadas usando CTkFrame
        self.welcome_section = ctk.CTkFrame(self.welcome_container,
                                            fg_color="#242424",
                                            corner_radius=15)
        self.welcome_section.pack(fill="x", padx=0, pady=0)
        
        # Título de bienvenida
        titulo_genero = "Dr" if datos_usuario["sexo"] == "Masculino" else "Dra"
        ctk.CTkLabel(self.welcome_section,
                     text=f"Bienvenido, {titulo_genero} {datos_usuario['nombre']}.",
                     text_color="white",
                     font=("Segoe UI", 24, "bold")).pack(side="top", anchor="w", pady=(15, 5), padx=20)
        
        # Subtítulo/Descripción
        ctk.CTkLabel(self.welcome_section,
                     text="Gestione sus consultas diarias y revise el historial de sus pacientes con facilidad",
                     text_color="#b0b0b0",
                     font=("Segoe UI", 12)).pack(side="top", anchor="w", pady=(0, 5), padx=20)
        
        # ========================================================================================================
        # ────────────────────── ""Estado de hoy"" ────────────────────────────────────────────────────
        # ========================================================================================================
        
        self.estado_section = ctk.CTkFrame(self.ventana,
                                        fg_color="#2a2a2a",
                                        corner_radius=15,)
        self.estado_section.pack(side="top", fill="x", padx=20, pady=(20, 0))
        
        # Contenedor interno con padding
        self.estado_container = tk.Frame(self.estado_section,
                                          bg="#2a2a2a")
        self.estado_container.pack(fill="both", padx=20, pady=15)
        
        # Título "Estado de hoy"
        tk.Label(self.estado_container,
                 text="Estado de hoy:",
                 bg="#2a2a2a",
                 fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=(0, 30))
        
        # Citas Pendientes (Naranja)
        self.frame_citas = ctk.CTkFrame(self.estado_container,
                                           fg_color="#313131",
                                           corner_radius=12)
        self.frame_citas.pack(side="left", padx=(0, 30))

        tk.Label(self.frame_citas,
                text="Citas pendientes: ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 11)).pack(side="left", padx=(10, 5), pady=8)
        tk.Label(self.frame_citas,
                text="8",
                bg="#313131",
                fg="#FF9500",
                font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 10), pady=8)

        # Citas Completadas (Verde)
        self.frame_citas = ctk.CTkFrame(self.estado_container,
                                           fg_color="#313131",
                                           corner_radius=12)
        self.frame_citas.pack(side="left", padx=(0, 30))

        tk.Label(self.frame_citas,
                text="Citas Completadas: ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 11)).pack(side="left", padx=(10, 5), pady=8)
        tk.Label(self.frame_citas,
                text="3",
                bg="#313131",
                fg="#2EA100",
                font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 10), pady=8)
        
        # Citas Canceladas (rojo)
        self.frame_citas = ctk.CTkFrame(self.estado_container,
                                           fg_color="#313131",
                                           corner_radius=12)
        self.frame_citas.pack(side="left", padx=(0, 30))

        tk.Label(self.frame_citas,
                text="Citas Canceladas: ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 11)).pack(side="left", padx=(10, 5), pady=8)
        tk.Label(self.frame_citas,
                text="1",
                bg="#313131",
                fg="#f70000",
                font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 10), pady=8)
        
        # Citas Confirmadas (Azul)
        self.frame_citas = ctk.CTkFrame(self.estado_container,
                                           fg_color="#313131",
                                           corner_radius=12)
        self.frame_citas.pack(side="left", padx=(0, 30))

        tk.Label(self.frame_citas,
                text="Citas confirmadas: ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 11)).pack(side="left", padx=(10, 5), pady=8)
        tk.Label(self.frame_citas,
                text="2",
                bg="#313131",
                fg="#006bf7",
                font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 10), pady=8)

        
        # ========================================================================================================
        # ────────────────────── ""Acciones rapidas"" ────────────────────────────────────────────────────
        # ========================================================================================================

        self.estado_section = ctk.CTkFrame(self.ventana,
                                        fg_color="#242424",
                                        corner_radius=15,)
        self.estado_section.pack(side="top", fill="x", padx=20, pady=(20, 0))

        #titulo "acciones rapidas"
        tk.Label(self.estado_section,
                 text="Acciones rapidas",
                 bg="#242424",
                 fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=(20, 5))
        
       
        self.estado_section = ctk.CTkFrame(self.ventana,
                                                fg_color="#2a2a2a",
                                                corner_radius=15,)
        self.estado_section.pack(side="top", fill="both", expand=False, padx=20, pady=(20, 0))
        
        # Contenedor interno para distribuir los recuadros
        self.acciones_container = ctk.CTkFrame(self.estado_section,
                                               fg_color="#2a2a2a",
                                               corner_radius=0)
        self.acciones_container.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        
        #primer recuadro de acciones
        self.frame_citas_1 = ctk.CTkFrame(self.acciones_container,
                                           fg_color="#313131",
                                           corner_radius=12)
        self.frame_citas_1.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(self.frame_citas_1,
                text="➕",
                bg="#313131",
                fg="#7a69b8",
                font=("Segoe UI", 30, "bold")).pack(side="top", anchor="w", padx=(20, 20), pady=(15, 0))
        tk.Label(self.frame_citas_1,
                text="Crear Cita: ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 11, "bold")).pack(side="top", anchor="w", padx=(20, 20), pady=(5, 15))
        tk.Label(self.frame_citas_1,
                text="Agende una consulta medica para un paciente. ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 8)).pack(side="top", anchor="w", padx=(20, 20), pady=(5, 15))
        self.btn_ingresar_1 = ctk.CTkButton(self.frame_citas_1,
                                  text="INGRESAR →",
                                  font=("Segoe UI", 11, "bold"),
                                  fg_color="#7a69b8",       
                                  hover_color="#5f5195",    
                                  text_color="white",
                                  corner_radius=8,          
                                  height=30,
                                  cursor="hand2")

        self.btn_ingresar_1.pack(side="top", fill="x", padx=(15, 15), pady=(0, 15))

        #segundo recuadro de acciones

        self.frame_citas_2 = ctk.CTkFrame(self.acciones_container,
                                           fg_color="#313131",
                                           corner_radius=12)
        self.frame_citas_2.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(self.frame_citas_2,
                text="📋",
                bg="#313131",
                fg="#db925d",
                font=("Segoe UI", 30, "bold")).pack(side="top", anchor="w", padx=(20, 20), pady=(15, 0))
        tk.Label(self.frame_citas_2,
                text="Consutar citas: ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 11, "bold")).pack(side="top", anchor="w", padx=(20, 20), pady=(5, 15))
        tk.Label(self.frame_citas_2,
                text="Revise su agenda para el dia de hoy y proximos turnos. ",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 8)).pack(side="top", anchor="w", padx=(20, 20), pady=(5, 15))
        self.btn_ingresar_2 = ctk.CTkButton(self.frame_citas_2,
                                  text="INGRESAR →",
                                  font=("Segoe UI", 11, "bold"),
                                  fg_color="#4a9ee8",       
                                  hover_color="#336fa3",    
                                  text_color="white",
                                  corner_radius=8,          
                                  height=30,
                                  cursor="hand2")

        self.btn_ingresar_2.pack(side="top", fill="x", padx=(15, 15), pady=(0, 15))




# ========================================================================================================
# ────────────────────── ""check list"" ────────────────────────────────────────────────────
# ======================================================================================================== (side="top", fill="x", padx=20, pady=(20, 0))
        # Lista de tareas fijas
        self.tareas = [
            "Abrir sistema",
            "Revisar agenda",
            "Revisar expedientes",
            "Preparar consultorios"
        ]
        
        # Variables para tracking de tareas completadas
        self.tareas_completadas = {}
        for i, tarea in enumerate(self.tareas):
            self.tareas_completadas[i] = tk.BooleanVar(value=False)
        
        
        # Frame principal
        self.frame_meta = ctk.CTkScrollableFrame(self.ventana,
                                       fg_color="#2a2a2a",
                                       corner_radius=15)
        self.frame_meta.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=(20, 0))
        
        # Encabezado
        header_frame = ctk.CTkFrame(self.frame_meta,
                                    fg_color="#2a2a2a",
                                    corner_radius=0)
        header_frame.pack(side="top", fill="x", padx=20, pady=(15, 10))
        
        tk.Label(header_frame,
                text="Meta del día",
                bg="#2a2a2a",
                fg="white",
                font=("Segoe UI", 18, "bold")).pack(side="left", anchor="w", padx=(0, 5))
        
        ctk.CTkButton(header_frame,
                     text="🔁 Reiniciar",
                     fg_color="#313131",
                     hover_color="#242424",
                     text_color="white",
                     font=("Segoe UI", 17, "bold"),
                     height=40,
                     cursor="hand2",
                     command=self.resetear_tareas).pack(side="right")
        
        # Descripción
        tk.Label(self.frame_meta,
                text="Barra de progreso hacia la meta diaria de citas, con checklist de objetivos.",
                bg="#2a2a2a",
                fg="white",
                font=("Segoe UI", 10),
                wraplength=400,
                justify="left").pack(side="top", fill="x", padx=20, pady=(0, 15))
        
        # Frame del progreso
        progress_frame = ctk.CTkFrame(self.frame_meta,
                                      fg_color="#313131",
                                      corner_radius=12)
        progress_frame.pack(side="top", fill="both", padx=20, pady=(0, 15))
        
        # Título progreso
        tk.Label(progress_frame,
                text="Progreso del día",
                bg="#313131",
                fg="white",
                font=("Segoe UI", 12, "bold")).pack(side="left", anchor="w", padx=20, pady=(15, 10))
        
        # Etiqueta de porcentaje
        self.label_porcentaje = tk.Label(progress_frame,
                                         text="0%",
                                         bg="#313131",
                                         fg="#56d18b",
                                         font=("Segoe UI", 18, "bold"))
        self.label_porcentaje.pack(side="right", anchor="e", padx=20, pady=(15, 10))
        
        # Barra de progreso
        progress_container = ctk.CTkFrame(progress_frame,
                                          fg_color="#313131",
                                          corner_radius=0)
        progress_container.pack(side="top", fill="x", padx=20, pady=(27, 15))
        
        self.progress_bar = ctk.CTkProgressBar(progress_container,
                                               fg_color="#2a2a2a",
                                               progress_color="#56d18b",
                                               height=15)
        self.progress_bar.pack(side="top", fill="x", pady=(0, 10))
        self.progress_bar.set(0.0)
        
        
        # Frame de tareas y botones
        acciones_frame = ctk.CTkFrame(self.frame_meta,
                                      fg_color="#313131",
                                      corner_radius=15)
        acciones_frame.pack(side="top", fill="both", padx=20, pady=(0, 20))
        
        # Frame para tareas  
        tareas_frame = ctk.CTkFrame(acciones_frame,
                                    fg_color="#2a2a2a",
                                    corner_radius=15)
        tareas_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 10))     

        
        # Crear los checkboxes para cada tarea
        self.checkbox_frames = []
        for i, tarea in enumerate(self.tareas):
            task_frame = ctk.CTkFrame(tareas_frame,
                                      fg_color="#2a2a2a",
                                      corner_radius=8)
            task_frame.pack(side="top", fill="x", padx=10, pady=(5, 0))           
            
            ctk.CTkCheckBox(task_frame,
                           text=tarea,
                           variable=self.tareas_completadas[i],
                           font=("Segoe UI", 11),
                           checkbox_height=18,
                           checkbox_width=18,
                           fg_color="#56d18b",
                           hover_color="#44a96f",
                           command=self.actualizar_progreso).pack(side="left", padx=15, pady=12)
            
            self.checkbox_frames.append(task_frame)
        


# ========================================================================================================
# ────────────────────── ""notas rapidas"" ────────────────────────────────────────────────────
# ========================================================================================================

        # Frame contenedor principal (para tener meta del día y notas lado a lado)
        self.container_meta_notas = ctk.CTkFrame(self.ventana,
                                                 fg_color="transparent",
                                                 corner_radius=0)
        self.container_meta_notas.pack(side="top", fill="both", expand=True, padx=20, pady=(20, 0))
        
        # Frame de Notas Rápidas
        self.frame_notas = ctk.CTkFrame(self.container_meta_notas,
                                        fg_color="#2a2a2a",
                                        corner_radius=15)
        self.frame_notas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Encabezado de Notas
        header_notas = ctk.CTkFrame(self.frame_notas,
                                    fg_color="#2a2a2a",
                                    corner_radius=0)
        header_notas.pack(side="top", fill="x", padx=20, pady=(15, 10))
        
        tk.Label(header_notas,
                text="Notas rápidas",
                bg="#2a2a2a",
                fg="white",
                font=("Segoe UI", 18, "bold")).pack(side="left", anchor="w", padx=(0, 5))
        
        ctk.CTkButton(header_notas,
                     text="🗑️Limpiar",
                     fg_color="#313131",
                     hover_color="#242424",
                     text_color="white",
                     font=("Segoe UI", 13, "bold"),
                     height=30,
                     cursor="hand2",
                     command=self.limpiar_notas).pack(side="right", padx=20, )   
        
        # Descripción
        tk.Label(self.frame_notas,
                text="Un bloc de notas simple para que el médico anote recordatorios del día.",
                bg="#2a2a2a",
                fg="white",
                font=("Segoe UI", 10),
                wraplength=350,
                justify="left").pack(side="top", fill="x", padx=20, pady=(0, 15))
        
        # Frame de entrada de notas
        entrada_frame = ctk.CTkFrame(self.frame_notas,
                                     fg_color="#2a2a2a",
                                     corner_radius=0)
        entrada_frame.pack(side="top", fill="x", padx=20, pady=(0, 15))
        
        # Entry para escribir nota rápida
        self.entry_nota = ctk.CTkEntry(entrada_frame,
                                       placeholder_text="Escribir nota rápida...",
                                       fg_color="#242424",
                                       border_color="#313131",
                                       text_color="white",
                                       placeholder_text_color="#666666",
                                       font=("Segoe UI", 11),
                                       height=40,
                                       corner_radius=8)
        self.entry_nota.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Botón para agregar nota
        self.btn_agregar_nota = ctk.CTkButton(entrada_frame,
                                              text="+",
                                              fg_color="#313131",
                                              hover_color="#242424",
                                              text_color="white",
                                              font=("Segoe UI", 16, "bold"),
                                              width=40,
                                              height=40,
                                              corner_radius=8,
                                              cursor="hand2",
                                              command=self.agregar_nota)
        self.btn_agregar_nota.pack(side="left")
        
        # Frame para lista de notas
        notas_list_frame = ctk.CTkFrame(self.frame_notas,
                                        fg_color="#2a2a2a",
                                        corner_radius=0)
        notas_list_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollable frame para notas
        self.notas_scrollable = ctk.CTkScrollableFrame(notas_list_frame,
                                                       fg_color="#2a2a2a",
                                                       corner_radius=0)
        self.notas_scrollable.pack(side="top", fill="both", expand=True)
        
        # Lista de notas (ejemplo)
        import json, os
        ruta = os.path.join(os.path.dirname(__file__), "notas_guardadas.json")
        if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                        self.notas_lista = json.load(f)
        else:
                self.notas_lista = []
        
        # Renderizar notas existentes
        self.mostrar_notas()
                          


        



       
        







































        self.ventana.mainloop()
