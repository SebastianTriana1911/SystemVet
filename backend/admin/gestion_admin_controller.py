import json
from tkinter import messagebox


class GestionAdminController:
    def __init__(self, vista):
        self.vista = vista
        self.archivo_path = "data/usuarios.json" # Ruta a tu base de datos

    def cargar_datos_tabla(self):
        # Lee el JSON y filtra solo a los administradores para la tabla
        try:
            with open(self.archivo_path, 'r') as f:
                usuarios = json.load(f)
            
            # Limpiar la tabla antes de insertar (por si es una actualización)
            for i in self.vista.tabla.get_children():
                self.vista.tabla.delete(i)

            # Lógica de filtrado por ROL
            for nit, datos in usuarios.items():
                if datos["rol"].lower() == "administrador":
                    # Insertamos todos los campos definidos en tu clase Usuario
                    self.vista.tabla.insert("", "end", values=(
                        nit,
                        datos["nombre"],
                        datos["sexo"],
                        datos["telefono"],
                        "********" # La contraseña se mantiene oculta por seguridad
                    ))
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró la base de datos de usuarios.")

    def cerrar_sesion(ventana_gestion_admin):

        respuesta = messagebox.askyesno("Cierre de sesion", "Esta seguro de cerrar la sesión")
        
        if respuesta == True:
            ventana = ventana_gestion_admin        
            ventana.destroy()

            from main import iniciar_app
            iniciar_app()

