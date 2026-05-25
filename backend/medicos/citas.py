import csv  # Librería que nos permite leer y escribir archivos en formato CSV (valores separados por comas/puntos y comas).
import os   # Librería del sistema operativo. La usamos para comprobar si los archivos existen y ver su tamaño.

class BackendCitas:
    # -------------------------------------------------------------------------
    # 1. VARIABLE DE CLASE
    # -------------------------------------------------------------------------
    # Definimos la ruta y el nombre del archivo donde se guardará todo.
    # Al estar aquí, todos los métodos pueden usar "BackendCitas.ARCHIVO_CSV".
    ARCHIVO_CSV = "data/citas_registradas.csv"


    # -------------------------------------------------------------------------
    # 2. MÉTODO: GUARDAR UNA NUEVA CITA 
    # -------------------------------------------------------------------------
    @staticmethod
    def guardar_cita_csv(datos_cita):
        """
        Recibe un diccionario (datos_cita) y lo guarda como una nueva fila en el CSV.
        """
        
        # Esta es la estructura de columnas que tendrá nuestro Excel/CSV. 
        # El orden aquí es importante porque dictará cómo se ven las columnas.
        campos = [
            "id_cita", "id_medico", "nombre_paciente", "nombre_propietario",
            "tipo_animal", "raza", "fecha", "hora", "tipo_servicio", 
            "motivo", "estado"
        ]
        
        siguiente_id = 1 # Empezamos asumiendo que el ID será el número 1.
        
        # Comprobamos en el disco duro si el archivo "citas_registradas.csv" ya existe.
        archivo_existe = os.path.exists(BackendCitas.ARCHIVO_CSV)
        
        # --- BLOQUE A: CALCULAR EL NUEVO ID (EJ: C001, C002) ---
        if archivo_existe:
            try:
                # Abrimos el archivo en modo lectura ("r" = read).
                with open(BackendCitas.ARCHIVO_CSV, "r", encoding="utf-8") as file:
                    # DictReader convierte cada fila del CSV en un diccionario.
                    reader = csv.DictReader(file, delimiter=";")
                    ids = [] # Lista temporal para guardar los números de ID que encontremos.
                    
                    for row in reader: # Recorremos fila por fila
                        try:
                            # Sacamos el ID de la fila actual y le quitamos espacios extra (strip).
                            id_str = row.get("id_cita", "").strip()
                            
                            # Si el ID empieza con la letra "C" (ej: "C005"):
                            if id_str.upper().startswith("C"):
                                num_str = id_str[1:]      # Le quitamos la "C" (queda "005")
                                ids.append(int(num_str))  # Lo convertimos a número entero y lo guardamos (5)
                            else:
                                ids.append(int(id_str))   # Por si acaso guardaron el ID solo como número.
                        except (ValueError, TypeError, KeyError):
                            # Si falla porque la celda está vacía o tiene un texto raro, simplemente lo ignoramos.
                            pass
                            
                    # Si encontramos IDs en el archivo, buscamos el más grande (max) y le sumamos 1.
                    if ids:
                        siguiente_id = max(ids) + 1
            except Exception:
                pass # Si hay algún error leyendo el archivo, ignoramos y nos quedamos con el ID 1.

        # Formateamos el ID. La f-string f"C{siguiente_id:03d}" hace que el número
        # siempre tenga 3 dígitos. Ej: si es 1, queda "C001". Si es 15, "C015".
        datos_cita["id_cita"] = f"C{siguiente_id:03d}"
        
        # Si no nos pasaron el "estado" de la cita, le ponemos "Pendiente" por defecto.
        if "estado" not in datos_cita:
            datos_cita["estado"] = "Pendiente"

        # --- BLOQUE B: ESCRIBIR LA CITA EN EL ARCHIVO ---
        try:
            # Abrimos el archivo en modo "a" (append = añadir). 
            # Esto escribe al final del archivo sin borrar lo que ya hay.
            with open(BackendCitas.ARCHIVO_CSV, "a", encoding="utf-8", newline="") as file:
                # Preparamos la herramienta para escribir el diccionario en el CSV.
                writer = csv.DictWriter(file, fieldnames=campos, delimiter=";")
                
                # Si el archivo es nuevo, o su tamaño es 0 bytes, necesitamos escribir
                # la primera fila (la cabecera con los nombres de las columnas).
                if not archivo_existe or os.path.getsize(BackendCitas.ARCHIVO_CSV) == 0:
                    writer.writeheader()
                    
                # Creamos un nuevo diccionario asegurándonos de que solo tenga los campos
                # permitidos. Si falta algún dato, le ponemos texto vacío ("").
                fila_escribir = {k: datos_cita.get(k, "") for k in campos}
                
                # Escribimos la fila finalmente en el archivo.
                writer.writerow(fila_escribir)
            
            # Devolvemos True porque fue un éxito, junto con un mensaje de confirmación.
            return True, f"La cita ha sido registrada correctamente con ID {siguiente_id}."
            
        except Exception as e:
            # Si da error (ej: si tienes el Excel abierto y no deja guardar), devolvemos False.
            return False, f"No se pudo guardar en el archivo CSV: {e}"


    # -------------------------------------------------------------------------
    # 3. MÉTODO: OBTENER TODAS LAS CITAS
    # -------------------------------------------------------------------------
    @staticmethod # <--- Agregamos este decorador para que todo tenga la misma estructura.
    def obtener_todas_citas():
        """
        Abre el archivo, lee todas las citas y las devuelve en una lista para mostrarlas.
        """
        # Si el archivo no existe, no hay citas. Devolvemos una lista vacía [].
        if not os.path.exists(BackendCitas.ARCHIVO_CSV):
            return []
        
        citas = []
        try:
            # Abrimos el archivo en modo lectura ("r").
            with open(BackendCitas.ARCHIVO_CSV, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")
                
                # Leemos fila por fila y convertimos cada fila en un diccionario.
                # Luego agregamos ese diccionario a nuestra lista "citas".
                for row in reader:
                    citas.append(dict(row))
        except Exception as e:
            # Si hay error (ej: permisos), lo imprimimos en consola.
            print(f"Error al leer citas: {e}")
            
        # Devolvemos la lista completa (estará llena si había citas, o vacía si dio error).
        return citas


    # -------------------------------------------------------------------------
    # 4. MÉTODO: ACTUALIZAR EL ESTADO DE UNA CITA
    # -------------------------------------------------------------------------
    @staticmethod
    def actualizar_estado_cita(id_cita, nuevo_estado):
        """
        Busca una cita por su ID y le cambia el estado (ej: de "Pendiente" a "Completado").
        Como no podemos editar una línea específica en un CSV directamente, 
        leemos todo, cambiamos lo que necesitamos, y volvemos a escribir todo el archivo.
        """
        # Si el archivo no existe, avisamos que falló (False).
        if not os.path.exists(BackendCitas.ARCHIVO_CSV):
            return False, "El archivo de citas no existe."

        campos = [
            "id_cita", "id_medico", "nombre_paciente", "nombre_propietario",
            "tipo_animal", "raza", "fecha", "hora", "tipo_servicio", 
            "motivo", "estado"
        ]

        citas_actualizadas = [] # Aquí guardaremos todas las citas (incluyendo la modificada).
        encontrado = False      # Nos sirve para saber si encontramos o no el ID.

        try:
            # --- PASO 1: Leer todas las citas a la memoria ---
            with open(BackendCitas.ARCHIVO_CSV, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    cita = dict(row)
                    # Comparamos el ID que estamos buscando con el ID de la fila actual.
                    # Convertimos ambos a texto (str) por si acaso hay diferencias de formato.
                    if str(cita.get("id_cita")) == str(id_cita):
                        cita["estado"] = nuevo_estado # Cambiamos el estado
                        encontrado = True             # Marcamos que sí lo encontramos
                        
                    # Agregamos la cita (modificada o no) a nuestra lista temporal.
                    citas_actualizadas.append(cita)

            # Si terminamos de leer todo y no encontramos el ID, devolvemos error.
            if not encontrado:
                return False, f"No se encontró la cita con ID {id_cita}."

            # --- PASO 2: Sobrescribir todo el archivo con la lista actualizada ---
            # Abrimos el archivo en modo "w" (write = escribir). 
            # ¡OJO! El modo "w" borra todo el contenido anterior del archivo.
            with open(BackendCitas.ARCHIVO_CSV, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=campos, delimiter=";")
                writer.writeheader() # Escribimos la cabecera
                
                # Recorremos nuestra lista de citas en memoria y las escribimos una a una.
                for cita in citas_actualizadas:
                    # Nos aseguramos de que cada cita tenga los campos correctos.
                    fila_escribir = {k: cita.get(k, "") for k in campos}
                    writer.writerow(fila_escribir)

            # Confirmamos que todo salió bien.
            return True, f"El estado de la cita #{id_cita} ha sido cambiado a '{nuevo_estado}'."

        except Exception as e:
            return False, f"Error al actualizar la cita: {e}"