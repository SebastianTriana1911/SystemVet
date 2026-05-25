import json # Componente nativo para la manipulación, lectura y serialización de archivos JSON
from tkinter import messagebox # Módulo del framework UI para desplegar diálogos de alerta y confirmación nativos

class RegistroMedicoController:
    def __init__(self, vista_registro):
        """
        CONSTRUCTOR DEL CONTROLADOR: Inicializa la relación con la capa de presentación (Vista)
        y define la ruta física hacia el almacenamiento plano de persistencia de usuarios.
        """
        self.vista         = vista_registro
        self.data_usuarios = "data/usuarios.json" # Ruta relativa al JSON que actúa como base de datos

    # ==========================================================================
    # REGISTRAR NUEVO MÉDICO
    # ==========================================================================
    def registrar_medico(self):
        """
        MÉTODO TRANSACCIONAL: Extrae la información desde la interfaz de usuario, aplica
        validaciones de nulidad o estados por defecto, y realiza la persistencia física en disco.
        """
        # Extracción y sanitización (remoción de espacios huérfanos en los extremos de las cadenas)
        nit          = self.vista.txt_nit.get().strip()
        nombre       = self.vista.txt_nombre.get().strip()
        apellido     = self.vista.txt_apellido.get().strip()
        sexo         = self.vista.cb_sexo.get()
        telefono     = self.vista.txt_telefono.get().strip()
        especialidad = self.vista.cb_especialidad.get()
        password     = self.vista.txt_password.get().strip()

        # VALIDACIÓN DE CAMPOS: Verifica nulidad o valores por defecto del ComboBox
        if not all([nit, nombre, apellido, telefono, password]) or \
           sexo == "Seleccione..." or especialidad == "Seleccione...":
            messagebox.showwarning("Campos vacíos",
                "Por favor, complete todos los campos del formulario.")
            return # Rompe el hilo de ejecución para evitar operaciones inválidas

        try:
            # FLUJO DE CONTROL DE INGESTA: Intenta cargar la estructura NoSQL existente
            try:
                with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                    usuarios = json.load(f)
            except FileNotFoundError:
                # Tolerancia a fallos: Si el archivo físico no existe en la primera ejecución, inicializa el nodo raíz
                usuarios = {}

            # VALIDACIÓN DE CLAVE PRIMARIA: Evita la colisión de registros duplicados en tiempo de ejecución
            if nit in usuarios:
                messagebox.showerror("Duplicado",
                    f"El NIT '{nit}' ya está registrado en el sistema.")
                return

            # INYECCIÓN DEL NUEVO REGISTRO: Asignación estructural con metadatos por defecto para el rol médico
            usuarios[nit] = {
                "nombre":       nombre,
                "apellido":     apellido,
                "sexo":         sexo,
                "telefono":     telefono,
                "especialidad": especialidad,
                "rol":          "medico",   # Fuerza la jerarquía de permisos del usuario a nivel de backend
                "estado":       "Activo",   # Todo nuevo médico ingresa al ecosistema en estado operacional apto
                "password":     password    # Credencial de autenticación plana
            }

            # ESCRITURA FÍSICA EN DISCO: Vuelca la memoria caché al almacenamiento JSON persistente
            with open(self.data_usuarios, 'w', encoding='utf-8') as f:
                # indent=4 proporciona legibilidad humana; ensure_ascii=False respeta tildes y caracteres latinos (ñ)
                json.dump(usuarios, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("Éxito",
                f"El médico {nombre} ha sido registrado correctamente.")

            # SINCRONIZACIÓN DE LA UI: Comunicación entre controladores para actualizar las tarjetas gráficas en paralelo
            if hasattr(self.vista, 'controlador_gestion') and self.vista.controlador_gestion:
                self.vista.controlador_gestion.cargar_cards() # Invoca refresco dinámico de componentes en pantalla

            self.vista.al_cerrar() # Cierra de forma ordenada el modal o ventana de registro actual

        except Exception as e:
            # Captura de errores globales para mitigar caídas imprevistas del software (Crash)
            messagebox.showerror("Error", f"No se pudo guardar el registro: {e}")

    # ==========================================================================
    # CARGAR DATOS PARA EDITAR
    # ==========================================================================
    def cargar_datos_para_editar(self, nit):
        """
        MÉTODO DE CONSULTA: Recupera un registro específico desde el JSON y puebla
        los campos de entrada de la interfaz, bloqueando la edición de la clave primaria (NIT).
        """
        try:
            nit_limpio = str(nit).strip()

            # Apertura segura del archivo en modo solo lectura
            with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            # Búsqueda indexada $O(1)$ sobre el diccionario
            if nit_limpio in usuarios:
                info = usuarios[nit_limpio]

                # INMUTABILIDAD DE LA LLAVE PRIMARIA: Habilita temporalmente el widget, lo limpia,
                # escribe la llave consultada y lo inhabilita para prevenir alteraciones lógicas del ID.
                self.vista.txt_nit.configure(state="normal")
                self.vista.txt_nit.delete(0, "end")
                self.vista.txt_nit.insert(0, nit_limpio)
                self.vista.txt_nit.configure(state="disabled", border_color="#555555")

                # Poblado secuencial de los widgets de la interfaz con datos de contingencia en caso de llaves ausentes
                self.vista.txt_nombre.insert(0,   info.get("nombre",   ""))
                self.vista.txt_apellido.insert(0,  info.get("apellido",  ""))
                self.vista.cb_sexo.set(            info.get("sexo",      "Seleccione..."))
                self.vista.txt_telefono.insert(0,  info.get("telefono",  ""))
                self.vista.cb_especialidad.set(    info.get("especialidad", "Seleccione..."))
                self.vista.txt_password.insert(0,  info.get("password",  ""))
            else:
                messagebox.showerror("Error",
                    f"No se encontró el NIT '{nit_limpio}' en la base de datos.")
                self.vista.al_cerrar()

        except Exception as e:
            messagebox.showerror("Error",
                f"No se pudieron cargar los datos para edición: {e}")

    # ==========================================================================
    # ACTUALIZAR MÉDICO EXISTENTE
    # ==========================================================================
    def actualizar_medico(self, nit_original):
        """
        MÉTODO DE ACTUALIZACIÓN: Sobreescribe la información de un nodo existente en el JSON
        garantizando mantener invariables el Rol y el Estado administrativo previo del usuario.
        """
        # Extracción de valores actuales modificados por el administrador en la UI
        nombre       = self.vista.txt_nombre.get().strip()
        apellido     = self.vista.txt_apellido.get().strip()
        sexo         = self.vista.cb_sexo.get()
        telefono     = self.vista.txt_telefono.get().strip()
        especialidad = self.vista.cb_especialidad.get()
        password     = self.vista.txt_password.get().strip()

        # Validación estructural de los datos modificados
        if not all([nombre, apellido, telefono, password]) or \
           sexo == "Seleccione..." or especialidad == "Seleccione...":
            messagebox.showwarning("Campos vacíos",
                "Por favor, complete todos los campos.")
            return

        try:
            with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            if nit_original in usuarios:
                # INTEGRIDAD DE ESTADO: Recupera y encapsula el estado previo del médico ('Activo'/'Inactivo').
                # Evita que una actualización ordinaria altere una suspensión impuesta de forma previa.
                estado_actual = usuarios[nit_original].get("estado", "Activo")

                # Mutación del nodo del diccionario bajo el mismo NIT original
                usuarios[nit_original] = {
                    "nombre":       nombre,
                    "apellido":     apellido,
                    "sexo":         sexo,
                    "telefono":     telefono,
                    "especialidad": especialidad,
                    "rol":          "medico", # Mantiene consistencia de rol institucional
                    "estado":       estado_actual, # Inyecta el estado administrativo recuperado de forma segura
                    "password":     password
                }

                # Persistencia atómica de la mutación sobre el archivo JSON
                with open(self.data_usuarios, 'w', encoding='utf-8') as f:
                    json.dump(usuarios, f, ensure_ascii=False, indent=4)

                messagebox.showinfo("Éxito",
                    "Los datos del médico han sido actualizados correctamente.")

                # Refresco asíncrono/reactivo de la pantalla principal de gestión hospitalaria
                if self.vista.controlador_gestion:
                    self.vista.controlador_gestion.cargar_cards()

                self.vista.al_cerrar() # Conclusión segura del caso de uso de edición

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}")