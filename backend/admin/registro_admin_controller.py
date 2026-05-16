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




    def cargar_datos_para_editar(self, nit):
        try:
            # Nos aseguramos de quitar cualquier espacio invisible que venga de la tabla
            nit_limpio = str(nit).strip()

            with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
            
            # Verificamos si el NIT realmente existe en el diccionario
            if nit_limpio in usuarios:
                info = usuarios[nit_limpio]
                
                # 1. Insertar el NIT y bloquearlo para que no lo editen (es la llave primaria)
                self.vista.txt_nit.configure(state="normal") # Nos aseguramos que deje escribir primero
                self.vista.txt_nit.delete(0, "end")
                self.vista.txt_nit.insert(0, nit_limpio)
                self.vista.txt_nit.configure(state="disabled", border_color="#555555")
                
                # 2. Insertar el resto de la información en las cajas de texto
                self.vista.txt_nombre.insert(0, info.get("nombre", ""))
                self.vista.txt_apellido.insert(0, info.get("apellido", ""))
                
                # Configurar el combobox del sexo de forma segura
                sexo_guardado = info.get("sexo", "Seleccione...")
                self.vista.cb_sexo.set(sexo_guardado)
                
                self.vista.txt_telefono.insert(0, info.get("telefono", ""))
                self.vista.txt_password.insert(0, info.get("password", ""))
            else:
                # Si no lo encuentra, le avisamos al usuario y cerramos la ventana rota
                messagebox.showerror(
                    "Error de lectura", 
                    f"No se pudo encontrar el NIT '{nit_limpio}' en la base de datos de usuarios.\n\n"
                    "Verifica que el archivo JSON no haya sido modificado manualmente."
                )
                self.vista.al_cerrar()
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos del usuario para edición: {e}")

    def actualizar_usuario(self, nit_original):
        # Capturamos lo que el usuario modificó
        nombre = self.vista.txt_nombre.get().strip()
        apellido = self.vista.txt_apellido.get().strip()
        sexo = self.vista.cb_sexo.get()
        telefono = self.vista.txt_telefono.get().strip()
        password = self.vista.txt_password.get().strip()

        if not nombre or not apellido or not telefono or not password or sexo == "Seleccione...":
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        try:
            with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            # Actualizamos el nodo correspondiente de la llave (NIT)
            if nit_original in usuarios:
                usuarios[nit_original] = {
                    "nombre": nombre,
                    "apellido": apellido,
                    "sexo": sexo,
                    "telefono": telefono,
                    "rol": "administrador",
                    "password": password
                }

                # Guardamos los cambios de vuelta en el JSON
                with open(self.data_usuarios, 'w', encoding='utf-8') as f:
                    json.dump(usuarios, f, ensure_ascii=False, indent=4)

                messagebox.showinfo("Éxito", "Los datos del administrador han sido actualizados.")
                
                # Refrescamos la tabla de gestión
                if self.vista.controlador_gestion:
                    self.vista.controlador_gestion.cargar_datos_tabla()
                
                # Cerramos la ventana emergente
                self.vista.al_cerrar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron salvar los cambios: {e}")    
    # def ejecutar_registro(self):
    #     RegistroAdminController.registrar_usuario()

    