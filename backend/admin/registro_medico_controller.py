import json
from tkinter import messagebox

class RegistroMedicoController:
    def __init__(self, vista_registro):
        self.vista         = vista_registro
        self.data_usuarios = "data/usuarios.json"

    # ==========================================================================
    # REGISTRAR NUEVO MÉDICO
    # ==========================================================================
    def registrar_medico(self):
        nit          = self.vista.txt_nit.get().strip()
        nombre       = self.vista.txt_nombre.get().strip()
        apellido     = self.vista.txt_apellido.get().strip()
        sexo         = self.vista.cb_sexo.get()
        telefono     = self.vista.txt_telefono.get().strip()
        especialidad = self.vista.cb_especialidad.get()
        password     = self.vista.txt_password.get().strip()

        # Validación de campos
        if not all([nit, nombre, apellido, telefono, password]) or \
           sexo == "Seleccione..." or especialidad == "Seleccione...":
            messagebox.showwarning("Campos vacíos",
                "Por favor, complete todos los campos del formulario.")
            return

        try:
            try:
                with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                    usuarios = json.load(f)
            except FileNotFoundError:
                usuarios = {}

            if nit in usuarios:
                messagebox.showerror("Duplicado",
                    f"El NIT '{nit}' ya está registrado en el sistema.")
                return

            # Guardar el nuevo médico
            usuarios[nit] = {
                "nombre":       nombre,
                "apellido":     apellido,
                "sexo":         sexo,
                "telefono":     telefono,
                "especialidad": especialidad,
                "rol":          "medico",
                "estado":       "Activo",
                "password":     password
            }

            with open(self.data_usuarios, 'w', encoding='utf-8') as f:
                json.dump(usuarios, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("Éxito",
                f"El médico {nombre} ha sido registrado correctamente.")

            # Refrescar las cards de la vista de médicos
            if hasattr(self.vista, 'controlador_gestion') and self.vista.controlador_gestion:
                self.vista.controlador_gestion.cargar_cards()

            self.vista.al_cerrar()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el registro: {e}")

    # ==========================================================================
    # CARGAR DATOS PARA EDITAR
    # ==========================================================================
    def cargar_datos_para_editar(self, nit):
        try:
            nit_limpio = str(nit).strip()

            with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            if nit_limpio in usuarios:
                info = usuarios[nit_limpio]

                # NIT bloqueado (es llave primaria)
                self.vista.txt_nit.configure(state="normal")
                self.vista.txt_nit.delete(0, "end")
                self.vista.txt_nit.insert(0, nit_limpio)
                self.vista.txt_nit.configure(state="disabled",
                                             border_color="#555555")

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
        nombre       = self.vista.txt_nombre.get().strip()
        apellido     = self.vista.txt_apellido.get().strip()
        sexo         = self.vista.cb_sexo.get()
        telefono     = self.vista.txt_telefono.get().strip()
        especialidad = self.vista.cb_especialidad.get()
        password     = self.vista.txt_password.get().strip()

        if not all([nombre, apellido, telefono, password]) or \
           sexo == "Seleccione..." or especialidad == "Seleccione...":
            messagebox.showwarning("Campos vacíos",
                "Por favor, complete todos los campos.")
            return

        try:
            with open(self.data_usuarios, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            if nit_original in usuarios:
                # Conservar el estado actual del médico al actualizar
                estado_actual = usuarios[nit_original].get("estado", "Activo")

                usuarios[nit_original] = {
                    "nombre":       nombre,
                    "apellido":     apellido,
                    "sexo":         sexo,
                    "telefono":     telefono,
                    "especialidad": especialidad,
                    "rol":          "medico",
                    "estado":       estado_actual,
                    "password":     password
                }

                with open(self.data_usuarios, 'w', encoding='utf-8') as f:
                    json.dump(usuarios, f, ensure_ascii=False, indent=4)

                messagebox.showinfo("Éxito",
                    "Los datos del médico han sido actualizados correctamente.")

                # Refrescar cards
                if self.vista.controlador_gestion:
                    self.vista.controlador_gestion.cargar_cards()

                self.vista.al_cerrar()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}")