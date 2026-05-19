import json
from tkinter import messagebox

class GestionAdminController:
    def __init__(self, vista):
        self.vista = vista
        self.archivo_path = "data/usuarios.json" # Lee el archivo bd

    # ==========================================================================
    # CARGA Y DIBUJA LOS DATOS EN LA TABLA CUSTOM
    # ==========================================================================
    def cargar_datos_tabla(self):
        try:
            with open(self.archivo_path, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)

            # Limpiar filas existentes
            for widget in self.vista.contenedor_tabla.winfo_children():
                widget.destroy()

            # Resetear contadores
            self.vista.contador_total.set(0)
            self.vista.contador_masculino.set(0)
            self.vista.contador_femenino.set(0)

            for nit, datos in usuarios.items():
                rol  = datos.get("rol",  "").lower()
                sexo = datos.get("sexo", "")

                if rol == "administrador":

                    # Contadores
                    self.vista.contador_total.set(self.vista.contador_total.get() + 1)
                    if sexo == "Masculino":
                        self.vista.contador_masculino.set(self.vista.contador_masculino.get() + 1)
                    else:
                        self.vista.contador_femenino.set(self.vista.contador_femenino.get() + 1)

                    # Dibujar fila en la vista
                    self.vista.agregar_fila(
                        nit,
                        datos.get("nombre",   ""),
                        datos.get("apellido", ""),
                        sexo,
                        datos.get("telefono", ""),
                    )

        except FileNotFoundError:
            print("El archivo JSON no existe todavía.")
        except Exception as e:
            print(f"Error al cargar los datos en la tabla: {e}")
    # ==========================================================================


    # ==========================================================================
    # REGRESA A LA VENTANA HOME
    # ==========================================================================
    def regresar_ventana(ventana_gestion_admin, datos_usuario):
        try:
            from view.admin.home_view import HomeVentana
            ventana_gestion_admin.destroy() # Destruye la ventana actual
            app = HomeVentana(datos_usuario) # Crea una nueva instancia de la ventana a acceder
            if hasattr(app, 'ventana'):
                app.ventana.mainloop()
            else:
                app.mainloop()
        except Exception as e:
            print(f"Error al intentar regresar: {e}")
    # ==========================================================================


    # ==========================================================================
    # CIERRA LA SESION
    # ==========================================================================
    def cerrar_sesion(ventana_gestion_admin):
        respuesta = messagebox.askyesno("Cierre de sesión", "¿Está seguro de cerrar la sesión?")
        if respuesta:
            ventana_gestion_admin.destroy()
            from main import iniciar_app
            iniciar_app()
    # ==========================================================================


    # ==========================================================================
    # ABRE EL FORMULARIO DE REGISTRO
    # ==========================================================================
    def abrir_formulario_registro(ventana_gestion_admin, controlador_admin):
        from view.admin.registro_admin_view import RegistroAdminView
        RegistroAdminView(ventana_gestion_admin, controlador_admin)
    # ==========================================================================


    # ==========================================================================
    # ELIMINA UN ADMINISTRADOR
    # ==========================================================================
    def eliminar_administrador(self, nit, nombre):
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al administrador {nombre}?"
        )
        if confirmar:
            try:
                with open(self.archivo_path, 'r', encoding='utf-8') as f: # Accede a la bd
                    usuarios = json.load(f)

                # Encuentra el registro con la llave primaria Nit
                if nit in usuarios:
                    del usuarios[nit] # Elimina usuario
                    with open(self.archivo_path, 'w', encoding='utf-8') as f:
                        json.dump(usuarios, f, ensure_ascii=False, indent=4)
                    messagebox.showinfo("Eliminado", "Administrador eliminado correctamente.")
                    self.cargar_datos_tabla()
                else:
                    messagebox.showerror("Error", "El usuario no se encontró en la base de datos.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")
    # ==========================================================================

    # ==========================================================================
    # ABRE EL FORMULARIO DE EDICION
    # ==========================================================================
    def abrir_formulario_edicion(self, nit):
        from view.admin.registro_admin_view import RegistroAdminView
        RegistroAdminView(self.vista.ventana, self, nit_editar=nit)
    # ==========================================================================