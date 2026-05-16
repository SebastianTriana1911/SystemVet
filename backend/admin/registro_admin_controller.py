import json
from tkinter import messagebox

class RegistroAdminController():
    def __init__(self, vista_registro):
        self.vista = vista_registro

        # self.ventana_emergente = vista_registro
        # self.ventana_gestion = vista_registro.ventana_padre

        # Ruta del archivo JSON
        self.data_usuarios = "data/usuarios.json" 

    def registrar_usuario(self):
        # Se capturan los datos de los Entrys de la vista
        nit = self.vista.txt_nit.get().strip()
        nombre = self.vista.txt_nombre.get().strip()
        apellido = self.vista.txt_apellido.get().strip()
        sexo = self.vista.cb_sexo.get()
        telefono = self.vista.txt_telefono.get().strip()
        password = self.vista.txt_password.get().strip()

        # VALIDACIÓN: Verificar que no haya campos vacíos o por defecto
        if not nit or not nombre or not apellido or not telefono or not password or sexo == "Seleccione...":
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos del formulario.")
            return

        try:
            # Leer los datos existentes en el archivo json
            try:
                with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                    usuarios = json.load(f)
            except FileNotFoundError:
                # Si el archivo no existe todavía, inicializamos un diccionario vacío
                usuarios = {}

            # VALIDACIÓN: Verificar si el NIT ya existe
            if nit in usuarios:
                messagebox.showerror("Error de duplicado", f"El NIT/CC '{nit}' ya se encuentra registrado en el sistema.")
                return

            # CREAR EL NUEVO REGISTRO DE ADMINISTRADOR
            usuarios[nit] = {
                "nombre": nombre,
                "apellido": apellido,
                "sexo": sexo,
                "telefono": telefono,
                "rol": "administrador", # Forzado por defecto para este formulario
                "password": password
            }

            # 6. GUARDAR LOS DATOS ACTUALIZADOS EN EL JSON
            with open(self.data_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios, f, ensure_ascii=False, indent=4)

            # 7. ÉXITO: Notificar al usuario
            messagebox.showinfo("Registro exitoso", f"El administrador {nombre} ha sido creado correctamente.")
            
            # 8. REFRESCAR LA TABLA DE ATRÁS EN TIEMPO REAL
            # Usamos el controlador de la tabla de gestión que le pasamos a la vista
            if hasattr(self.vista, 'controlador_gestion') and self.vista.controlador_gestion:
                self.vista.controlador_gestion.cargar_datos_tabla()

            # 9. Cerrar el formulario emergente automáticamente
            self.vista.al_cerrar()

        except Exception as e:
            messagebox.showerror("Error de guardado", f"Ocurrió un error inesperado al guardar los datos: {e}")


    # def ejecutar_registro(self):
    #     RegistroAdminController.registrar_usuario()

    