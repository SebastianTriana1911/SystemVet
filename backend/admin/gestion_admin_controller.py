import json
from tkinter import messagebox

class GestionAdminController:
    def __init__(self, vista):
        self.vista = vista
        self.archivo_path = "data/usuarios.json" # Ruta a tu base de datos

        # 🌟 VINCULAR EL CLIC DE LA TABLA A NUESTRO MANEJADOR
        self.vista.tabla.bind("<ButtonRelease-1>", self.detectar_clic_acciones)
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
                    self.vista.tabla.insert("", "end", iid=nit, values=(
                        nit,                         # 1. Nit
                        datos.get("nombre", ""),     # 2. Nombre
                        datos.get("apellido", ""),   # 3. Apellido
                        datos.get("sexo", ""),       # 4. Sexo
                        datos.get("telefono", ""),   # 5. Telefono
                        "********",                  # 6. Password
                        " ✎ Editar  |  🗑 Borrar"      # 7. Acciones
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


    # ==========================================================================
    # METODO ABRIR FORMULARIO (VENTANA EMERGENTE)
    # ==========================================================================
    # Este método se ejecutaría al hacer clic en "+ Registrar Admin"
    # Se pasa como parametro la ventana de gestion admin para aplicarle ciertas propiedades que permitan el bloqueo de la misma
    # Ademas se le pasa el controlador admin que es el metodo que accede al archivo Json y muestra el registro de los campos en la tabla
    def abrir_formulario_registro(ventana_gestion_admin, controlador_admin):

        ventana_gestion_adm = ventana_gestion_admin
        controlador = controlador_admin

        # Importamos la vista y la abrimos pasándole la ventana actual
        from view.admin.registro_admin_view import RegistroAdminView
        ventana_registro = RegistroAdminView(ventana_gestion_adm, controlador)
    # ==========================================================================


    # ==========================================================================
    # METODO PARA CAPTURAR LOS EVENTOS DEL MOMENTO EN EL QUE EL USUARIO HACE CLICK EN ALGUNA OPCION DE LA FILA
    # ==========================================================================
    def detectar_clic_acciones(self, event):
        # 1. Identificar qué fila se seleccionó
        # item_id = self.vista.tabla.identify_row(event.y)
        # 2. Identificar qué columna se seleccionó
        # columna_id = self.vista.tabla.identify_column(event.x)
        
        # Si el usuario hizo clic en el espacio vacío fuera de las celdas, no hacemos nada
        # if not item_id:
        #     return
            
        # En tu Treeview, la columna "Acciones" es la #7
        # if columna_id == "#7" or columna_id == "Acciones":
        #     🌟 ¡CLAVE! El nit_seleccionado es directamente el item_id limpio
        #     nit_seleccionado = str(item_id).strip()
            
        #     Buscamos los valores solo para sacar el nombre para el mensaje de confirmación
        #     valores = self.vista.tabla.item(item_id, "values")
        #     nombre_seleccionado = valores[1] if len(valores) > 1 else ""
            
        #     bbox = self.vista.tabla.bbox(item_id, columna_id)
        #     if bbox:
        #         🌟 CLAVE: Traducimos la posición X del mouse al plano cartesiano de la TABLA
        #         Restamos el origen X de la tabla para sincronizarlo con el bbox
        #         x_relativo_tabla = event.x - self.vista.tabla.winfo_x()
                
        #         Calculamos el punto medio exacto de la celda de acciones
        #         punto_medio_celda = bbox[0] + (bbox[2] / 2)
                
        #         Comparamos usando la coordenada corregida
        #         if x_relativo_tabla < punto_medio_celda:
        #             CLIC A LA IZQUIERDA = EDITAR
        #             self.abrir_formulario_edicion(nit_seleccionado)
        #         else:
        #             CLIC A LA DERECHA = BORRAR
        #             self.eliminar_administrador(nit_seleccionado, nombre_seleccionado)
        # 1. Identificar qué fila se seleccionó
        item_id = self.vista.tabla.identify_row(event.y)
        columna_id = self.vista.tabla.identify_column(event.x)
        
        if not item_id:
            return
            
        if columna_id == "#7":
            # 2. OBTENER LOS VALORES DE LA FILA SELECCIONADA
            valores = self.vista.tabla.item(item_id, "values")
            
            if not valores:
                print("Error: No se pudieron recuperar los valores de la fila.")
                return

            # 🌟 ESTRATEGIA DE RESCATE DEL NIT 🌟
            # Intentamos sacarlo del item_id (gracias al iid=nit), 
            # y si Tkinter le inventó un ID interno (como 'I001'), lo sacamos de la columna 1 (valores[0])
            nit_seleccionado = str(item_id).strip()
            
            if nit_seleccionado.startswith("I") and len(nit_seleccionado) > 1:
                # Si Tkinter generó un iid automático (ej: I001, I002), sacamos el NIT real del value[0]
                nit_seleccionado = str(valores[0]).strip()
            
            nombre_seleccionado = valores[1] if len(valores) > 1 else ""
            
            # --- IMPRESIÓN DE CONTROL EN CONSOLA ---
            # Esto te dirá exactamente en la terminal qué está capturando el programa
            print(f"--- DEBUG CLIN DE ACCIONES ---")
            print(f"ID de la fila (item_id): {item_id}")
            print(f"NIT detectado final: {nit_seleccionado}")
            print(f"Valores de la fila: {valores}")
            print(f"------------------------------")

            bbox = self.vista.tabla.bbox(item_id, columna_id)
            if bbox:
                x_relativo_tabla = event.x - self.vista.tabla.winfo_x()
                punto_medio_celda = bbox[0] + (bbox[2] / 2)
                
                if x_relativo_tabla < punto_medio_celda:
                    # LE PASAMOS EL NIT ASEGURADO AL FORMULARIO
                    self.abrir_formulario_edicion(nit_seleccionado)
                else:
                    self.eliminar_administrador(nit_seleccionado, nombre_seleccionado)



    def eliminar_administrador(self, nit, nombre):
        # Confirmación de seguridad en pantalla
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar al administrador {nombre} con NIT {nit}?"
        )
        
        if confirmar:
            try:
                # 1. Leer JSON actual
                with open(self.archivo_path, 'r', encoding='utf-8') as f:
                    usuarios = json.load(f)
                
                # 2. Remover la llave del diccionario
                if nit in usuarios:
                    del usuarios[nit]
                    
                    # 3. Guardar los cambios de vuelta en el archivo
                    with open(self.archivo_path, 'w', encoding='utf-8') as f:
                        json.dump(usuarios, f, ensure_ascii=False, indent=4)
                    
                    messagebox.showinfo("Eliminado", "Administrador eliminado correctamente.")
                    
                    # 4. Refrescar la tabla automáticamente
                    self.cargar_datos_tabla()
                else:
                    messagebox.showerror("Error", "El usuario no se encontró en la base de datos.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")

    def abrir_formulario_edicion(self, nit):
        from view.admin.registro_admin_view import RegistroAdminView
        # Verifica que estés pasando el parámetro con el nombre exacto: nit_editar=nit
        ventana_edicion = RegistroAdminView(self.vista.ventana, self, nit_editar=nit)