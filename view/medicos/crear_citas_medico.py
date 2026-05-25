import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from backend.medicos.citas import BackendCitas
# pyrefly: ignore [missing-import]
from tkcalendar import DateEntry

# Configuración general del tema
# ctk.set_appearance_mode("dark") establece la paleta de colores del programa a modo oscuro por defecto.
ctk.set_appearance_mode("dark")

# =========================================================
# MOCKS (Datos simulados para la ejecución)
# =========================================================
datos_usuario = {"id_medico": "1", "sexo": "Masculino", "nombre": "Juan", "apellido": "Pérez"}

class GestionMedicoController:
    @staticmethod
    def cerrar_sesion(ventana):
        print("Cerrando sesión...")
        ventana.destroy()
# =========================================================

class VentanaCrearCita():
    def __init__(self, datos_usuario):
        self.datos_usuario = datos_usuario
        
        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DE LA VENTANA ─────────────────────────────────────────────────────
        # ========================================================================================================
        # Inicializa la ventana principal de CustomTkinter. ctk.CTk es el equivalente a tk.Tk() pero con soporte de temas modernos.
        self.ventana = ctk.CTk()
        ctk.set_appearance_mode("dark")
        
        # Icono y Título de la aplicación
        # iconbitmap vincula un archivo .ico como icono superior de la ventana.
        self.ventana.iconbitmap("image/huella_icono.ico") 
        self.ventana.title("SystemVet / Crear Cita")

        # after(0, lambda: ...) ejecuta el código inmediatamente después de que se inicie el bucle principal.
        # state('zoomed') maximiza la ventana en sistemas Windows.
        self.ventana.after(0, lambda: self.ventana.state('zoomed'))

        # ========================================================================================================
        # ────────────────────── CONFIGURACIÓN DEL ENCABEZADO ────────────────────────────────────────────────────
        # ========================================================================================================
        # tk.Frame es un contenedor estándar de Tkinter. Lo usamos aquí con un color de fondo verde menta (#45A29E).
        self.header = tk.Frame(self.ventana, bg="#45A29E")
        self.header.pack(side="top", fill="x") 
        
        # Intenta cargar el logotipo de la clínica veterinaria
        try:
            # subsample(2, 2) reduce la imagen original dividiendo su ancho y alto entre 2 (la escala).
            self.image_logo = tk.PhotoImage(file="image/logotipo.png").subsample(2, 2)
        except:
            self.image_logo = tk.PhotoImage()

        # Widget de imagen para el logotipo
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

        # Determina si muestra "Home Médico" o "Home Médica" según el sexo del usuario
        titulo_home = "Home Médico" if self.datos_usuario["sexo"] == "Masculino" else "Home Médica"
        tk.Label(
            self.header,
            text=titulo_home,
            fg="white",
            bg="#45A29E",
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")
        
        # Carga del avatar de usuario según corresponda del sexo
        avatar = "image/avatar_masculino.png" if self.datos_usuario["sexo"] == "Masculino" else "image/avatar_femenino.png"

        try:
            img_original = tk.PhotoImage(file=avatar) 
            self.image_avatar = img_original.subsample(2, 2)
        except:
            self.image_avatar = tk.PhotoImage()

        # Widget para el avatar del usuario
        image_avatar = tk.Label(
            self.header,
            bg="#45A29E",
            image=self.image_avatar
        )
        image_avatar.image = self.image_avatar
        image_avatar.pack(side="right", padx=(0, 20))

        # Contenedor para la información de sesión a la derecha del Header
        self.container_usuario = tk.Frame(self.header, bg="#45A29E")
        self.container_usuario.pack(side="right", padx=20)
        
        # Etiqueta de Rol (ej. "Médico" o "Médica")
        rol = "Médico" if self.datos_usuario["sexo"] == "Masculino" else "Médica"
        tk.Label(
            self.container_usuario,
            text=rol,
            bg="#45A29E",
            fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(side="top", anchor="e")
        
        # Contenedor para agrupar nombre del usuario y el botón de cerrar sesión
        self.fila_nombre = tk.Frame(self.container_usuario, bg="#45A29E")
        self.fila_nombre.pack(side="top", anchor="e")
        
        # Etiqueta del nombre de usuario (ej. "Juan Pérez")
        tk.Label(
            self.fila_nombre,
            text=f"{self.datos_usuario['nombre']} {self.datos_usuario['apellido']}    | ",
            bg="#45A29E",
            fg="white",
            font=("Segoe UI", 13)
        ).pack(side="left", padx=(0, 5))
        
        # Botón para cerrar sesión (destruye la ventana)
        # cursor="hand2" cambia el cursor a una mano con el dedo índice levantado al pasar por encima del botón.
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
        # Contenedor principal con fondo transparente para heredar el color dark nativo de la ventana principal
        cuerpo = ctk.CTkFrame(self.ventana, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True, pady=40)

        # ctk.CTkScrollableFrame crea un contenedor con una barra de scroll vertical nativa en el lado derecho.
        # Esto previene que el botón "Confirmar Cita" se oculte en pantallas de baja altura (e.g. 768px).
        # width=650 define un ancho de 650 píxeles para hacerlo un poco más ancho e ideal para los inputs.
        # expand=True y fill="y" lo centran de forma horizontal en la ventana principal.
        panel_izquierdo = ctk.CTkScrollableFrame(
            cuerpo,
            width=750,
            fg_color="transparent"
        )
        panel_izquierdo.pack(expand=True, fill="y")

        # ========================================================================================================
        # ────────────────────── PANEL DE CAPTURA: FORMULARIO ─────────────────────────────────────────────────────
        # ========================================================================================================
        # Cabecera del formulario (botón de retroceder y título)
        title_frame = ctk.CTkFrame(panel_izquierdo, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        # Botón de retroceso (simulado)
        btn_back = ctk.CTkButton(
            title_frame,
            text="←",
            width=30,
            height=30,
            font=("Segoe UI", 20, "bold"),
            fg_color="transparent",
            hover_color="#2b2b2b",
            anchor="w"
        )
        btn_back.pack(side="left")
        
        # Título de la acción
        lbl_title = ctk.CTkLabel(
            title_frame,
            text="Crear Cita",
            font=("Segoe UI", 26, "bold"),
            text_color="#45A29E"
        )
        lbl_title.pack(side="left", padx=10)

        # --- TARJETA 1: Detalles del Paciente ---
        # ctk.CTkFrame sirve como una "tarjeta" visual gracias a corner_radius y border_color.
        card1 = ctk.CTkFrame(
            panel_izquierdo,
            fg_color="#1a1a1f",
            corner_radius=10,       # Redondea las esquinas del contenedor a un radio de 10px.
            border_width=1,         # Grosor de la línea del borde.
            border_color="#333333"   # Color gris oscuro para el borde de la tarjeta.
        )
        card1.pack(fill="x", pady=(0, 15), ipady=15)

        # Título de la Tarjeta 1
        ctk.CTkLabel(
            card1,
            text="Detalles del Paciente",
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 15))

        # Campo: Nombre del Paciente
        ctk.CTkLabel(
            card1,
            text="Nombre del Paciente",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 5))
        
        self.entry_paciente = ctk.CTkEntry(
            card1,
            placeholder_text="Ingrese el nombre",
            height=35,
            fg_color="#121212",
            border_width=1,
            border_color="#333333"
        )
        # grid() coloca el elemento en coordenadas de filas y columnas.
        # sticky="ew" estira el entry a izquierda (East) y derecha (West) ocupando todo el ancho de su celda.
        self.entry_paciente.grid(row=2, column=0, sticky="ew", padx=(20, 10))

        # Campo: Nombre del Dueño
        ctk.CTkLabel(
            card1,
            text="Nombre del Dueño",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).grid(row=1, column=1, sticky="w", padx=10, pady=(0, 5))
        
        self.entry_dueno = ctk.CTkEntry(
            card1,
            placeholder_text="Ingrese el nombre",
            height=35,
            fg_color="#121212",
            border_width=1,
            border_color="#333333"
        )
        self.entry_dueno.grid(row=2, column=1, sticky="ew", padx=(10, 20))

        # Campo: Tipo de Animal (Perro, Gato, etc.)
        ctk.CTkLabel(
            card1,
            text="Tipo de Animal",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 5))
        
        # ctk.CTkComboBox es la lista desplegable de CustomTkinter.
        # state="readonly" previene que el usuario escriba texto libre en el combobox, forzándolo a elegir una opción.
        self.cmb_animal = ctk.CTkComboBox(
            card1,
            values=["Perro", "Gato"],
            height=35,
            fg_color="#ffffff",
            text_color="black",
            border_width=0,
            state="readonly"
        )
        self.cmb_animal.set("Seleccione tipo de animal")
        self.cmb_animal.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20)

        # grid_columnconfigure le da peso horizontal y un ancho uniforme a las dos columnas (0 y 1)
        # permitiendo que se repartan equitativamente al 50% de la tarjeta.
        card1.grid_columnconfigure(0, weight=1)
        card1.grid_columnconfigure(1, weight=1)

        # --- TARJETA 2: Fecha y Hora ---
        card2 = ctk.CTkFrame(
            panel_izquierdo,
            fg_color="#1a1a1f",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        card2.pack(fill="x", pady=15, ipady=15)

        # Título de la Tarjeta 2
        ctk.CTkLabel(
            card2,
            text="Fecha y Hora",
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 15))

        # Campo: Fecha
        ctk.CTkLabel(
            card2,
            text="Fecha",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 5))
        
        # DateEntry es un calendario gráfico importado de tkcalendar.
        # state="readonly" obliga a interactuar con el calendario y no a digitar fechas incorrectas.
        # date_pattern="dd/mm/yyyy" formatea la salida para estandarizar el día, mes y año.
        self.entry_fecha = DateEntry(
            card2,
            width=15,
            background='#1a1a1f',
            foreground='white',
            borderwidth=0,
            font=("Segoe UI", 11),
            headersbackground='#121212',
            headersforeground='white',
            normalbackground='#121212',
            normalforeground='white',
            weekendbackground='#121212',
            weekendforeground='white',
            date_pattern='dd/mm/yyyy',
            state="readonly"
        )
        self.entry_fecha.grid(row=2, column=0, sticky="ew", padx=(20, 10), ipady=6)

        # Campo: Hora de la cita
        ctk.CTkLabel(
            card2,
            text="Hora",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).grid(row=1, column=1, sticky="w", padx=10, pady=(0, 5))
        
        # CTkComboBox con state="readonly"
        self.cmb_hora = ctk.CTkComboBox(
            card2,
            values=["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM"],
            height=35,
            fg_color="#121212",
            border_width=1,
            border_color="#333333",
            state="readonly"
        )
        self.cmb_hora.set("--:-- -----")
        self.cmb_hora.grid(row=2, column=1, sticky="ew", padx=(10, 20))

        card2.grid_columnconfigure(0, weight=1)
        card2.grid_columnconfigure(1, weight=1)

        # --- TARJETA 3: Tipo de Servicio ---
        card3 = ctk.CTkFrame(
            panel_izquierdo,
            fg_color="#1a1a1f",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        card3.pack(fill="x", pady=15, ipady=15)

        # Título de la Tarjeta 3
        ctk.CTkLabel(
            card3,
            text="Tipo de Servicio",
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(15, 10))

        # Frame contenedor de los botones de radio
        frame_radios = ctk.CTkFrame(card3, fg_color="transparent")
        frame_radios.pack(fill="x", padx=20)
        frame_radios.grid_columnconfigure(0, weight=1)
        frame_radios.grid_columnconfigure(1, weight=1)

        # ctk.StringVar es una clase especial de Tkinter que rastrea y almacena un valor de tipo texto.
        # Asociar esta misma variable de control a un grupo de CTkRadioButton crea el enlace exclusivo:
        # cuando se selecciona uno, el valor de la variable cambia y los demás botones se desmarcan solos.
        self.var_servicio = ctk.StringVar(value="")
        color_act = "#ff85b3"

        # Creación dinámica de los RadioButtons
        # Usamos row=idx // 2 (división entera) y column=idx % 2 (residuo) para distribuirlos en 2 columnas
        servicios = ["Consulta General", "Vacunación", "Cirugía", "Peluquería"]
        for idx, serv in enumerate(servicios):
            rb = ctk.CTkRadioButton(
                frame_radios,
                text=serv,
                variable=self.var_servicio,
                value=serv,
                fg_color=color_act,
                hover_color=color_act
            )
            rb.grid(row=idx // 2, column=idx % 2, sticky="w", pady=10)

        # --- TARJETA 4: Motivo de consulta y Confirmación ---
        card4 = ctk.CTkFrame(
            panel_izquierdo,
            fg_color="#1a1a1f",
            corner_radius=10,
            border_width=1,
            border_color="#333333"
        )
        card4.pack(fill="x", pady=15, ipady=15)

        ctk.CTkLabel(
            card4,
            text="Motivo de consulta",
            font=("Segoe UI", 11, "bold"),
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        # ctk.CTkTextbox es un campo de entrada multilínea de CustomTkinter.
        placeholder_texto = "Describa brevemente el motivo de la visita..."
        self.txt_motivo = ctk.CTkTextbox(
            card4,
            height=80,
            fg_color="#ffffff",
            text_color="black",
            border_width=0,
            corner_radius=5
        )
        self.txt_motivo.pack(fill="x", padx=20, pady=(0, 20))
        self.txt_motivo.insert("0.0", placeholder_texto)

        # --- EVENTOS BIND PARA SIMULAR PLACEHOLDER EN CTKTEXTBOX ---
        # Dado que CTkTextbox no soporta la propiedad nativa 'placeholder_text' de forma directa,
        # asociamos funciones a los eventos <FocusIn> (hacer clic en la caja) y <FocusOut> (salir de la caja).
        def on_focus_in(event):
            # Si el texto actual es el placeholder inicial, lo limpiamos para que el usuario pueda escribir
            if self.txt_motivo.get("0.0", "end-1c") == placeholder_texto:
                self.txt_motivo.delete("0.0", "end")
                self.txt_motivo.configure(text_color="black") 

        def on_focus_out(event):
            # Si al salir, la caja está vacía, reinstauramos el texto del placeholder en color gris
            if not self.txt_motivo.get("0.0", "end-1c").strip(): 
                self.txt_motivo.insert("0.0", placeholder_texto)
                self.txt_motivo.configure(text_color="gray") 

        # bind vincula eventos específicos del widget con las funciones de simulación escritas arriba.
        self.txt_motivo.bind("<FocusIn>", on_focus_in)
        self.txt_motivo.bind("<FocusOut>", on_focus_out)

        # --- Botón de Confirmar Cita ---
        # command=self.guardar_cita asocia la función guardar_cita para ejecutarse inmediatamente al hacer clic.
        btn_confirmar = ctk.CTkButton(
            card4, 
            text="✓ Confirmar Cita", 
            font=("Segoe UI", 14, "bold"),
            fg_color="#45A29E",
            hover_color="#2C7A7B", 
            height=45,
            width=180,
            corner_radius=8,
            command=self.guardar_cita
        )
        btn_confirmar.pack(side="right", padx=20, pady=(10, 10))

        # mainloop() mantiene la ventana abierta y a la escucha de eventos (clicks, teclas, etc.)
        self.ventana.mainloop()

    def ir_a_home(self):
        """Cierra la ventana actual y regresa al home del médico."""
        self.ventana.destroy()
        from view.medicos.home_medico import HomeMedico
        HomeMedico(self.datos_usuario)

    def ir_a_consultar_citas(self):
        """Cierra la ventana actual y abre la ventana de consultar citas."""
        self.ventana.destroy()
        from view.medicos.consultar_citas_medico import VentanaConsultarCitas
        app_consultar = VentanaConsultarCitas(self.datos_usuario)

    def guardar_cita(self):
        """Valida que todos los campos requeridos estén llenos y guarda la cita en citas_registradas.csv."""
        # .get() lee el texto introducido en la caja de texto. .strip() elimina espacios sobrantes al inicio/final.
        paciente = self.entry_paciente.get().strip()
        dueno = self.entry_dueno.get().strip()
        animal = self.cmb_animal.get()
        fecha = self.entry_fecha.get().strip()
        hora = self.cmb_hora.get()
        servicio = self.var_servicio.get()
        
        # "0.0" y "end-1c" leen desde la primera línea y carácter cero hasta el final, omitiendo el salto de línea automático.
        motivo = self.txt_motivo.get("0.0", "end-1c").strip()

        placeholder_texto = "Describa brevemente el motivo de la visita..."
        if motivo == placeholder_texto:
            motivo = ""

        # Validación de campos obligatorios
        if not paciente or not dueno or animal == "Seleccione tipo de animal" or not fecha or hora == "--:-- -----" or not servicio:
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos obligatorios y seleccione un servicio.")
            return

        # Diccionario con los datos del paciente y de la cita en formato CSV
        nueva_cita = {
            "id_medico": self.datos_usuario.get("id_medico", "1"),
            "nombre_paciente": paciente,
            "nombre_propietario": dueno,
            "tipo_animal": animal,
            "fecha": fecha,
            "hora": hora,
            "tipo_servicio": servicio,
            "motivo": motivo,
            "estado": "Pendiente"
        }

        # Envía los datos del registro al controlador/backend
        exito, mensaje = BackendCitas.guardar_cita_csv(nueva_cita)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos() # Restablece el formulario a blanco tras el guardado del registro
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_campos(self):
        """Restablece los inputs y variables del formulario a sus valores de inicio."""
        # delete(0, "end") limpia todo el contenido escrito en la caja de entrada (de la posición 0 a la última).
        self.entry_paciente.delete(0, "end")
        self.entry_dueno.delete(0, "end")
        self.cmb_animal.set("Seleccione tipo de animal")
        self.entry_fecha.delete(0, "end")
        self.cmb_hora.set("--:-- -----")
        self.var_servicio.set("")
        
        # Restablece la caja del motivo con su placeholder inicial en color gris
        self.txt_motivo.delete("0.0", "end")
        self.txt_motivo.insert("0.0", "Describa brevemente el motivo de la visita...")
        self.txt_motivo.configure(text_color="gray")

# Punto de entrada para inicializar y ejecutar la aplicación cuando se arranca este script directamente.
if __name__ == "__main__":
    app = VentanaCrearCita(datos_usuario)