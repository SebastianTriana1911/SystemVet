import json
from tkinter import messagebox

class GestionAdminController:
    def __init__(self, vista):
        self.vista = vista
        self.archivo_path = "data/usuarios.json" # Ruta a tu base de datos

    def cargar_datos_tabla(self):
        try:
            with open(self.archivo_path, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
            
            # Limpiar la tabla
            for i in self.vista.tabla.get_children():
                self.vista.tabla.delete(i)

            # Iterar sobre el diccionario (nit es la llave primaria)
            for nit, datos in usuarios.items():
                # Validación de seguridad: verificamos que el rol exista y sea administrador
                rol = datos.get("rol", "").lower()
                
                if rol == "administrador":
                    # DEBEN SER 7 VALORES EXACTAMENTE:
                    self.vista.tabla.insert("", "end", values=(
                        nit,                         # 1. Nit
                        datos.get("nombre", ""),     # 2. Nombre
                        datos.get("apellido", ""),   # 3. Apellido (Faltaba este)
                        datos.get("sexo", ""),       # 4. Sexo
                        datos.get("telefono", ""),   # 5. Telefono
                        "********",                  # 6. Password
                        "  ✎ Editar | 🗑 Borrar"      # 7. Acciones (Faltaba este)
                    ))
                    
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo en: {self.archivo_path}")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON está mal formado o vacío.")
        except Exception as e:
            print(f"Error inesperado: {e}")


    def regresar_ventana(ventana_gestion_admin, datos_usuario):
        ventana = ventana_gestion_admin
        datos_usuario_home = datos_usuario

        # # 2. Creamos la nueva ventana ANTES o durante el proceso
        # # Nota: Asegúrate de importar HomeVentana al inicio del archivo
        # from view.admin.home_view import HomeVentana 

        # # 3. Abrimos la Home pasando los datos del usuario logueado
        # nueva_ventana_home = HomeVentana(datos_usuario_home)
        

        # ventana.destroy()

        try:
            # 1. Importar aquí para evitar errores de importación circular
            from view.admin.home_view import HomeVentana 

            # 2. Primero destruimos la actual para liberar la memoria de Tkinter
            ventana.destroy()

            # 3. Creamos la nueva instancia
            # Asegúrate de que esta clase realmente cree su propia ventana
            app = HomeVentana(datos_usuario)

            # 4. Forzamos el inicio del loop si no se inicia solo
            if hasattr(app, 'ventana'):
                app.ventana.mainloop()
            else:
                app.mainloop()
            
        except Exception as e:
            print(f"Error al intentar regresar: {e}")
    

    def cerrar_sesion(ventana_gestion_admin):

        respuesta = messagebox.askyesno("Cierre de sesion", "Esta seguro de cerrar la sesión")
        
        if respuesta == True:
            ventana = ventana_gestion_admin        
            ventana.destroy()

            from main import iniciar_app
            iniciar_app()

