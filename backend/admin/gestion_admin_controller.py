import json # Librería nativa para manipular archivos JSON (Base de Datos del sistema)
from tkinter import messagebox # Módulo gráfico para mostrar cuadros de diálogo de alerta o confirmación

class GestionAdminController:
    def __init__(self, vista):
        """
        MÉTODO CONSTRUCTOR: Se ejecuta al instanciar el controlador.
        Establece el puente de comunicación con la Vista y define la ruta de la base de datos.
        """
        self.vista = vista
        self.archivo_path = "data/usuarios.json" # Atributo que almacena la ruta de la base de datos local

    # ==========================================================================
    # CARGA Y DIBUJA LOS DATOS EN LA TABLA CUSTOM
    # ==========================================================================
    def cargar_datos_tabla(self):
        """
        Lee los registros del archivo JSON, calcula métricas estadísticas por género,
        filtra por rol de administrador y envía la información depurada a la interfaz visual.
        """
        try:
            # APERTURA EN MODO LECTURA ('r'): Abre el archivo JSON garantizando soporte para caracteres especiales (utf-8)
            with open(self.archivo_path, 'r', encoding='utf-8') as f:
                usuarios = json.load(f) # Convierte el texto estructurado del JSON en un diccionario de Python

            # LIMPIEZA PREVENTIVA DE LA INTERFAZ
            # Itera sobre todos los componentes hijos del contenedor de la tabla y los destruye para evitar duplicados
            for widget in self.vista.contenedor_tabla.winfo_children():
                widget.destroy()

            # RESETEO DE CONTADORES ESTADÍSTICOS
            # Establece en cero las variables de control de Tkinter enlazadas a las tarjetas KPI de la vista
            self.vista.contador_total.set(0)
            self.vista.contador_masculino.set(0)
            self.vista.contador_femenino.set(0)

            # PROCESAMIENTO FILA POR FILA
            # Recorre el diccionario de usuarios desestructurándolo en su Clave (nit) y su Valor (datos)
            for nit, datos in usuarios.items():
                rol  = datos.get("rol",  "").lower() # Obtiene el rol en minúsculas para evitar errores sintácticos
                sexo = datos.get("sexo", "")         # Obtiene el género del registro actual

                # FILTRO DE SEGURIDAD: Solo se listan y contabilizan los usuarios que tengan perfil de "administrador"
                if rol == "administrador":

                    # ACTUALIZACIÓN RECONSTRUCTIVA DE CONTADORES LOGÍSTICOS
                    # Incrementa el acumulador total de la vista en +1
                    self.vista.contador_total.set(self.vista.contador_total.get() + 1)
                    
                    # Evalúa la cadena de sexo para segmentar las estadísticas de género del panel superior
                    if sexo == "Masculino":
                        self.vista.contador_masculino.set(self.vista.contador_masculino.get() + 1)
                    else:
                        self.vista.contador_femenino.set(self.vista.contador_femenino.get() + 1)

                    # INYECCIÓN DE DATOS EN LA CAPA VISUAL
                    # Ejecuta el método encargado de construir físicamente los componentes visuales de la fila
                    self.vista.agregar_fila(
                        nit,                                # Llave primaria identificadora
                        datos.get("nombre",   ""),
                        datos.get("apellido", ""),
                        sexo,
                        datos.get("telefono", ""),
                    )

        except FileNotFoundError:
            # Control de excepciones por si el sistema se ejecuta por primera vez y no encuentra la BD
            print("El archivo JSON no existe todavía.")
        except Exception as e:
            # Captura cualquier otra anomalía imprevista (Ej: JSON corrupto o con errores de sintaxis)
            print(f"Error al cargar los datos en la tabla: {e}")
    # ==========================================================================


    # ==========================================================================
    # REGRESA A LA VENTANA HOME
    # ==========================================================================
    @staticmethod # Se puede interpretar como estático al no usar 'self' para interactuar con atributos de instancia
    def regresar_ventana(ventana_gestion_admin, datos_usuario):
        """
        Gestiona la navegación segura hacia atrás. Destruye el hilo del módulo de administración
        e instancia el panel principal correspondiente al usuario actual.
        """
        try:
            # IMPORTACIÓN LOCAL (Lazy Import): Se importa aquí dentro para prevenir errores de importación circular en Python
            from view.admin.home_view import HomeVentana
            
            ventana_gestion_admin.destroy()  # Destruye y libera los recursos de la ventana de gestión actual
            app = HomeVentana(datos_usuario) # Crea la nueva instancia de la ventana Home transfiriéndole la sesión activa
            
            # CONTROL DE COMPATIBILIDAD: Verifica si la clase heredó una ventana interna o si actúa como ventana raíz
            if hasattr(app, 'ventana'):
                app.ventana.mainloop() # Inicia el ciclo infinito de eventos de Tkinter sobre la propiedad interna
            else:
                app.mainloop()         # Inicia el ciclo directamente sobre el objeto instanciado
        except Exception as e:
            print(f"Error al intentar regresar: {e}")
    # ==========================================================================


    # ==========================================================================
    # CIERRA LA SESION
    # ==========================================================================
    @staticmethod
    def cerrar_sesion(ventana_gestion_admin):
        """
        Desencadena un protocolo de confirmación. Si el usuario acepta, se destruye la 
        interfaz administrativa y se reinicia el sistema redirigiéndolo al Login de acceso.
        """
        # Muestra una ventana emergente interactiva de tipo Sí/No
        respuesta = messagebox.askyesno("Cierre de sesión", "¿Está seguro de cerrar la sesión?")
        if respuesta: # Si el valor de la variable booleana es True (El usuario presionó "Sí")
            ventana_gestion_admin.destroy() # Cierra y destruye por completo el entorno actual
            from main import iniciar_app     # Importa el disparador principal de la raíz del proyecto
            iniciar_app()                    # Ejecuta el login restaurando el sistema desde cero
    # ==========================================================================


    # ==========================================================================
    # ABRE EL FORMULARIO DE REGISTRO
    # ==========================================================================
    @staticmethod
    def abrir_formulario_registro(ventana_gestion_admin, controlador_admin):
        """
        Método de enrutamiento que manda a llamar e inicializa la vista secundaria
        destinada a capturar los datos de un nuevo administrador.
        """
        from view.admin.registro_admin_view import RegistroAdminView
        # Crea la ventana modal pasándole la ventana padre y la referencia de este controlador
        RegistroAdminView(ventana_gestion_admin, controlador_admin)
    # ==========================================================================


    # ==========================================================================
    # ELIMINA UN ADMINISTRADOR
    # ==========================================================================
    def eliminar_administrador(self, nit, nombre):
        """
        Busca un registro mediante su clave única (NIT) en el diccionario JSON, lo remueve,
        guarda los cambios en el disco duro y refresca los datos reflejados en la interfaz gráfica.
        """
        # Cuadro de confirmación crítico para evitar eliminaciones accidentales en el sistema
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al administrador {nombre}?"
        )
        if confirmar:
            try:
                # OPERACIÓN DE LECTURA: Carga el estado actual de la Base de Datos en memoria RAM
                with open(self.archivo_path, 'r', encoding='utf-8') as f:
                    usuarios = json.load(f)

                # EVALUACIÓN DE EXISTENCIA: Revisa si la clave primaria NIT existe en las propiedades del diccionario
                if nit in usuarios:
                    del usuarios[nit] # Palabra clave 'del' elimina la llave y sus valores internos de forma permanente
                    
                    # OPERACIÓN DE ESCRITURA ('w'): Abre el archivo sobreescribiéndolo con las modificaciones del diccionario
                    with open(self.archivo_path, 'w', encoding='utf-8') as f:
                        # Convierte el diccionario a texto plano estructurado en JSON
                        # ensure_ascii=False conserva e imprime caracteres con tildes o eñes de manera correcta
                        # indent=4 le otorga un formato visual legible tabulado con 4 espacios
                        json.dump(usuarios, f, ensure_ascii=False, indent=4)
                    
                    # Notificaciones de éxito hacia el usuario operador
                    messagebox.showinfo("Eliminado", "Administrador eliminado correctamente.")
                    self.cargar_datos_tabla() # Llama al método local para refrescar la tabla visual al instante
                else:
                    messagebox.showerror("Error", "El usuario no se encontró en la base de datos.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")
    # ==========================================================================

    # ==========================================================================
    # ABRE EL FORMULARIO DE EDICION
    # ==========================================================================
    def abrir_formulario_edicion(self, nit):
        """
        Abre el mismo componente visual de registro pero en modo edición, inyectando
        el parámetro 'nit_editar' para que el formulario se precargue con la información existente.
        """
        from view.admin.registro_admin_view import RegistroAdminView
        # Instancia la vista compartida configurándola con los datos clave del administrador seleccionado
        RegistroAdminView(self.vista.ventana, self, nit_editar=nit)
    # ==========================================================================