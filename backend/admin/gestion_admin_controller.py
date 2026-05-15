import json
from tkinter import messagebox

class GestionAdminController:
    def __init__(self, vista):
        self.vista = vista
        self.archivo_path = "data/usuarios.json" # Ruta a tu base de datos

    # ==========================================================================
    # ESTE METODO ANALIZA EL JSON Y VALIDA LA FILA PARA IDENTIFICAR EL COLOR Y INSERTA EL DATO
    # ==========================================================================
    def cargar_datos_tabla(self):
        try:
            with open(self.archivo_path, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
            
            # Limpiar la tabla
            for i in self.vista.tabla.get_children():
                self.vista.tabla.delete(i)

            # Creamos un contador para saber qué fila es par y cuál impar con el fin de saber que color mostrar
            index = 0

            # Iterar sobre el diccionario (nit es la llave primaria)
            for nit, datos in usuarios.items():
                # Validación de seguridad: verificamos que el rol exista y sea administrador
                rol = datos.get("rol", "").lower()
                
                if rol == "administrador":
                    tag_fila = 'par' if index % 2 == 0 else 'impar'

                    # Valorres correspondientes a la clase Usuario
                    self.vista.tabla.insert("", "end", values=(
                        nit,                         # 1. Nit
                        datos.get("nombre", ""),     # 2. Nombre
                        datos.get("apellido", ""),   # 3. Apellido
                        datos.get("sexo", ""),       # 4. Sexo
                        datos.get("telefono", ""),   # 5. Telefono
                        "********",                  # 6. Password
                        "  ✎ Editar | 🗑 Borrar"      # 7. Acciones
                    ), tags=(tag_fila,))

                    index += 1
                    
        except FileNotFoundError:
            print("El archivo JSON no existe todavía.")
        except Exception as e:
            print(f"Error al cargar los datos en la tabla: {e}")
    # ==========================================================================


    # ==========================================================================
    # ESTE METODO PERMITE QUE AL HACER CLIK AL LOGO ME MANDE AL HOME
    # ==========================================================================
    def regresar_ventana(ventana_gestion_admin, datos_usuario):
        ventana = ventana_gestion_admin
        datos_usuario_home = datos_usuario

        try:
            # Importar aquí para evitar errores de importación circular
            from view.admin.home_view import HomeVentana 

            # Primero destruimos la actual para liberar la memoria de Tkinter
            ventana.destroy()

            # Creamos la nueva instancia
            app = HomeVentana(datos_usuario)

            # Forzamos el inicio del loop si no se inicia solo
            if hasattr(app, 'ventana'):
                app.ventana.mainloop()
            else:
                app.mainloop()
            
        except Exception as e:
            print(f"Error al intentar regresar: {e}")
    # ==========================================================================


    # ==========================================================================
    # METODO PARA CERRAR LA SESION
    # ==========================================================================
    def cerrar_sesion(ventana_gestion_admin):

        # Se pregunta al usuario si realmente desea cerrar la sesion
        respuesta = messagebox.askyesno("Cierre de sesion", "Esta seguro de cerrar la sesión")
        
        # Se identifica la respuesta, si esta es afirmativa se cierra la ventana
        if respuesta == True:
            ventana = ventana_gestion_admin        
            ventana.destroy()

            # Se vueve a ejecutar el metodo iniciar_app encontrado en el archivo main
            from main import iniciar_app
            iniciar_app()
    # ==========================================================================


