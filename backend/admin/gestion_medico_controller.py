# import json # Módulo nativa para la lectura y escritura de estructuras JSON
# import pandas as pd # Librería de análisis de datos para la manipulación óptima de matrices y tablas CSV
# from datetime import date # Componente para capturar la fecha del sistema en tiempo real
# from tkinter import messagebox # Cuadros de diálogo emergentes estándar
# import customtkinter as ctk # Interfaz optimizada con widgets modernos en modo oscuro
# import tkinter as tk # Contenedor base de herramientas gráficas


# # =============================================================================
# # UTILIDAD: leer CSV siempre limpio (sin espacios iniciales en valores/columnas)
# # =============================================================================
# def _leer_csv(ruta):
#     """
#     FUNCIÓN DE SANITIZACIÓN: Carga un archivo CSV aplicando filtros de limpieza.
#     Remueve espacios en blanco huérfanos para evitar fallos de coincidencia de cadenas (strings).
#     """
#     # Separa por punto y coma (;), omite espacios iniciales y preserva los IDs como texto (no numéricos)
#     df = pd.read_csv(ruta, sep=";", skipinitialspace=True, dtype={"id_medico": str, "id_cita": str})
    
#     # Limpia los espacios en blanco (.strip()) que puedan existir en los nombres de las columnas
#     df.columns = df.columns.str.strip()
    
#     # Aplica de manera interna una función lambda para limpiar los textos de cada celda individual
#     df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
#     return df # Retorna el DataFrame de Pandas completamente purgado


# class GestionMedicosController:
#     def __init__(self, vista):
#         """
#         MÉTODO CONSTRUCTOR: Enlaza la vista con la lógica de negocio y
#         establece las rutas físicas de los archivos de almacenamiento de datos.
#         """
#         self.vista = vista
#         self.archivo_usuarios = "data/usuarios.json" # Archivo origen de perfiles
#         self.archivo_citas    = "data/citas_registradas.csv" # Archivo origen de la agenda

#         # VARIABLES DE CACHÉ / ESTADO INTERNO: Almacenan temporalmente al médico seleccionado en la UI
#         self._nit_medico_activo    = None
#         self._nombre_medico_activo = None
#         self._esp_medico_activo    = None
#         self._sexo_medico_activo   = None

#     # ==========================================================================
#     # CARGA Y DIBUJA LAS CARDS DE MÉDICOS
#     # ==========================================================================
#     def cargar_cards(self):
#         """
#         Lee el archivo de usuarios y citas, filtra el personal médico activo,
#         calcula las estadísticas globales por género y genera las tarjetas en la interfaz.
#         """
#         # LIMPIEZA VISUAL: Destruye todas las tarjetas previas del contenedor antes de redibujar
#         for w in self.vista.area_cards.winfo_children():
#             w.destroy()

#         # Reinicia los contadores gráficos de la pantalla a cero
#         self.vista.contador_total.set(0)
#         self.vista.contador_masculino.set(0)
#         self.vista.contador_femenino.set(0)

#         try:
#             # LECTURA JSON: Carga los usuarios registrados en el sistema
#             with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
#                 usuarios = json.load(f)

#             # LECTURA CSV VINCULADA: Intenta cargar las citas del archivo plano con Pandas
#             try:
#                 df_citas = _leer_csv(self.archivo_citas)
#                 # Si el archivo está vacío o corrupto, inicializa una estructura de respaldo segura
#                 if df_citas.empty or "id_medico" not in df_citas.columns:
#                     df_citas = pd.DataFrame(columns=["id_medico", "estado"])
#             except (FileNotFoundError, pd.errors.EmptyDataError):
#                 # Si el archivo CSV no existe aún, crea un DataFrame vacío con las columnas necesarias
#                 df_citas = pd.DataFrame(columns=["id_medico", "estado"])

#             # Variables de control para posicionar los elementos en una rejilla (Grid) de 2 columnas
#             fila, col = 0, 0

#             # Bucle principal para procesar a cada usuario del diccionario
#             for nit, datos in usuarios.items():
#                 # CLAÚSULA DE FILTRADO 1: Si el usuario no ostenta el rol de 'medico', lo ignora
#                 if datos.get("rol", "").lower() != "medico":
#                     continue
#                 # CLAÚSULA DE FILTRADO 2: Si el médico está inactivo o suspendido, no lo renderiza en el panel
#                 if datos.get("estado", "Activo") != "Activo":
#                     continue

#                 # Extrae los datos descriptivos del médico actual
#                 sexo         = datos.get("sexo", "")
#                 especialidad = datos.get("especialidad", "")
                
#                 # CÁLCULO DE CITAS ACTIVAS: Utiliza condicionales vectoriales de Pandas para contar cuántas 
#                 # citas vigentes ("Pendiente" o "En curso") posee el médico actual mediante su NIT
#                 num_citas    = len(df_citas[
#                     (df_citas["id_medico"].astype(str) == str(nit)) &
#                     (df_citas["estado"].isin(["Pendiente", "En curso"]))
#                 ]) if not df_citas.empty else 0

#                 # Incrementa las estadísticas globales reflejadas en las tarjetas KPI superiores
#                 self.vista.contador_total.set(self.vista.contador_total.get() + 1)
#                 if sexo == "Masculino":
#                     self.vista.contador_masculino.set(self.vista.contador_masculino.get() + 1)
#                 else:
#                     self.vista.contador_femenino.set(self.vista.contador_femenino.get() + 1)

#                 # CONSTRUCCIÓN COMPONENTE: Invoca el método de la vista para instanciar la tarjeta física
#                 self.vista.agregar_card(
#                     nit=nit,
#                     nombre=datos.get("nombre", ""),
#                     apellido=datos.get("apellido", ""),
#                     sexo=sexo,
#                     telefono=datos.get("telefono", ""),
#                     especialidad=especialidad,
#                     num_citas=num_citas,
#                     fila=fila,
#                     columna=col
#                 )

#                 # CÁLCULO LOGÍSTICO DE LA REJILLA: Controla que solo se ubiquen 2 tarjetas por fila (Columna 0 y Columna 1)
#                 col += 1
#                 if col > 1:
#                     col = 0
#                     fila += 1 # Salto de fila en el Grid visual

#         except FileNotFoundError:
#             print("❌ El archivo JSON no existe.")
#         except Exception as e:
#             # En caso de fallo grave, imprime el rastreo exacto de la línea de error (Traceback) sin detener la app
#             print(f"❌ Error al cargar médicos: {e}")
#             import traceback
#             traceback.print_exc()

#     # ==========================================================================
#     # CARGA EL CONTADOR DE CITAS DE HOY
#     # ==========================================================================
#     def cargar_citas_hoy(self):
#         """
#         Filtra mediante Pandas las filas cuya fecha coincida exactamente con la 
#         fecha actual del servidor e inyecta el número resultante en la interfaz.
#         """
#         try:
#             df  = _leer_csv(self.archivo_citas)
#             hoy = str(date.today()) # Convierte la fecha del sistema a formato de texto (AAAA-MM-DD)
            
#             # Cuenta el total de registros que cumplen con la condición de fecha
#             self.vista.contador_citas_hoy.set(len(df[df["fecha"] == hoy]))
#         except (FileNotFoundError, pd.errors.EmptyDataError):
#             self.vista.contador_citas_hoy.set(0) # Si no hay archivo o está vacío, el KPI es 0
#         except Exception as e:
#             print(f"Error al cargar citas de hoy: {e}")

#     # ==========================================================================
#     # MUESTRA LAS CITAS DE UN MÉDICO EN EL PANEL LATERAL
#     # ==========================================================================
#     def mostrar_citas_panel(self, nit, nombre, especialidad, sexo):
#         """
#         Guarda los datos del médico seleccionado en el estado temporal y extrae todas 
#         sus citas agendadas para mostrarlas detalladamente en el panel de revisión lateral.
#         """
#         # Seteo de las propiedades del estado de la instancia activa
#         self._nit_medico_activo    = nit
#         self._nombre_medico_activo = nombre
#         self._esp_medico_activo    = especialidad
#         self._sexo_medico_activo   = sexo

#         try:
#             df           = _leer_csv(self.archivo_citas)
#             # Filtra todas las citas vinculadas a la llave primaria del médico seleccionado
#             citas_medico = df[df["id_medico"].astype(str) == str(nit)]
            
#             # Convierte las filas del DataFrame en una lista de diccionarios nativos de Python para fácil lectura de la vista
#             lista        = citas_medico.to_dict(orient="records")
#         except FileNotFoundError:
#             lista = []
#         except Exception as e:
#             print(f"Error al cargar citas del panel: {e}")
#             lista = []

#         # Ordena a la interfaz pintar el panel lateral con la lista estructurada de citas obtenidas
#         self.vista.mostrar_panel_citas(nombre, especialidad, sexo, lista)

#     # ==========================================================================
#     # HELPER: obtiene médicos disponibles excluyendo al médico activo
#     # ==========================================================================
#     def _obtener_medicos_disponibles(self):
#         """
#         MÉTODO DE SOPORTE INTERNO: Compila un mapa de médicos alternativos que estén aptos 
#         para recibir citas reasignadas, garantizando excluir al médico que se está procesando.
#         """
#         try:
#             with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
#                 usuarios = json.load(f)

#             try:
#                 df_citas = _leer_csv(self.archivo_citas)
#             except (FileNotFoundError, pd.errors.EmptyDataError):
#                 df_citas = pd.DataFrame(columns=["id_medico", "estado"])

#             medicos = []
#             for nit, datos in usuarios.items():
#                 # Descarta usuarios que no pertenezcan al cuerpo médico, inactivos o al médico de origen
#                 if datos.get("rol", "").lower() != "medico":
#                     continue
#                 if datos.get("estado", "Activo") != "Activo":
#                     continue
#                 if str(nit) == str(self._nit_medico_activo):
#                     continue

#                 # Calcula la carga laboral actual del médico destino potencial (Citas activas)
#                 citas_activas = len(df_citas[
#                     (df_citas["id_medico"].astype(str) == str(nit)) &
#                     (df_citas["estado"].isin(["Pendiente", "En curso"]))
#                 ]) if not df_citas.empty else 0

#                 # Agrega el registro depurado al listado final de candidatos
#                 medicos.append({
#                     "nit":          nit,
#                     "nombre":       f"{datos.get('nombre', '')} {datos.get('apellido', '')}",
#                     "especialidad": datos.get("especialidad", ""),
#                     "sexo":         datos.get("sexo", ""),
#                     "num_citas":    citas_activas,
#                 })
#             return medicos # Retorna la colección de médicos candidatos disponibles

#         except Exception as e:
#             print(f"Error cargando médicos disponibles: {e}")
#             return []

#     # ==========================================================================
#     # REASIGNACIÓN INDIVIDUAL
#     # ==========================================================================
#     def iniciar_reasignacion_individual(self, id_cita, info_cita):
#         """Dispara el flujo visual para trasladar una única cita específica hacia otro médico."""
#         self.vista.mostrar_panel_reasignacion(
#             id_cita=id_cita,
#             info_cita=info_cita,
#             medicos_disponibles=self._obtener_medicos_disponibles(),
#             es_masiva=False, # Flag que define comportamiento selectivo único
#         )

#     # ==========================================================================
#     # REASIGNACIÓN MASIVA
#     # ==========================================================================
#     def iniciar_reasignacion_masiva(self):
#         """Dispara el flujo visual para trasladar la agenda completa de citas vigentes de un médico."""
#         self.vista.mostrar_panel_reasignacion(
#             id_cita=None,
#             info_cita=None,
#             medicos_disponibles=self._obtener_medicos_disponibles(),
#             es_masiva=True, # Flag que define un comportamiento de lote (Batch process)
#         )

#     # ==========================================================================
#     # CONFIRMAR REASIGNACIÓN (individual o masiva)
#     # ==========================================================================
#     def confirmar_reasignacion(self, nit_destino, id_cita=None, es_masiva=False):
#         """
#         PROCESAMIENTO TRANSACCIONAL: Modifica físicamente el archivo CSV cambiando el 
#         propietario de las citas. Ejecuta trazas de depuración (DEBUG) en consola para control de auditoría.
#         """
#         try:
#             df = _leer_csv(self.archivo_citas)

#             # TRAZAS DE AUDITORÍA (Logs de depuración del desarrollador)
#             print(f"DEBUG → nit_destino: {nit_destino} | id_cita: {id_cita} | es_masiva: {es_masiva}")
#             print(f"DEBUG → nit_activo: {self._nit_medico_activo}")
#             print(f"DEBUG → columnas CSV: {df.columns.tolist()}")
#             print(f"DEBUG → primeras filas:\n{df.head()}")

#             # CASO A: OPERACIÓN EN LOTE (REASIGNACIÓN MASIVA)
#             if es_masiva:
#                 # Genera una máscara booleana: localiza citas del médico origen que estén Pendientes o En Curso
#                 mask = (
#                     (df["id_medico"].astype(str).str.strip() == str(self._nit_medico_activo).strip()) &
#                     (df["estado"].isin(["Pendiente", "En curso"]))
#                 )
#                 cantidad = mask.sum() # Cuenta cuántas filas aplican para la mutación de datos
#                 print(f"DEBUG masiva → filas que matchean: {cantidad}")

#                 # Aplica indexación lógica (.loc) para cambiar el id_medico por el NIT destino en las filas filtradas
#                 df.loc[mask, "id_medico"] = str(nit_destino).strip()
#                 # Guarda los cambios sobreescribiendo el archivo original estructurado por punto y coma (;)
#                 df.to_csv(self.archivo_citas, index=False, sep=";")
#                 messagebox.showinfo("Reasignación masiva",
#                     f"Se reasignaron {cantidad} cita(s) correctamente.")

#             # CASO B: OPERACIÓN ATÓMICA (REASIGNACIÓN DE UNA CITA INDIVIDUAL)
#             else:
#                 id_cita_limpio = str(id_cita).strip()
#                 # Genera una máscara estricta evaluando el ID de la cita y validando que pertenezca al médico activo
#                 mask = (
#                     (df["id_cita"].astype(str).str.strip() == id_cita_limpio) &
#                     (df["id_medico"].astype(str).str.strip() == str(self._nit_medico_activo).strip())
#                 )
#                 cantidad = mask.sum()
#                 print(f"DEBUG individual → buscando id_cita: '{id_cita_limpio}' | filas que matchean: {cantidad}")

#                 # Control de excepciones lógico: Si la búsqueda da 0, cancela la operación y lanza advertencia
#                 if cantidad == 0:
#                     messagebox.showwarning("Sin coincidencia",
#                         f"No se encontró la cita '{id_cita_limpio}' para este médico.")
#                     return

#                 # Modifica el identificador del médico asignado a esa única cita en específico
#                 df.loc[mask, "id_medico"] = str(nit_destino).strip()
#                 df.to_csv(self.archivo_citas, index=False, sep=";")
#                 messagebox.showinfo("Cita reasignada", "La cita fue reasignada correctamente.")

#             # FLUJO ACTUALIZACIÓN (REACTIVO): Refresca inmediatamente la vista para reflejar los cambios en tiempo real
#             self.mostrar_citas_panel(
#                 self._nit_medico_activo,
#                 self._nombre_medico_activo,
#                 self._esp_medico_activo,
#                 self._sexo_medico_activo,
#             )
#             self.cargar_cards() # Re-calcula y dibuja las tarjetas de los médicos con los nuevos totales de agenda

#         except Exception as e:
#             messagebox.showerror("Error", f"No se pudo completar la reasignación:\n{e}")
#             import traceback
#             traceback.print_exc()

#     # ==========================================================================
#     # FLUJO DE BAJA: médico con citas → modal de reasignación + desactivar
#     # ==========================================================================
#     def iniciar_flujo_baja(self, nit, nombre):
#         """
#         FLUJO DE NEGOCIO AVANZADO: Abre una ventana modal de alta prioridad (grab_set) para obligar 
#         a dar de baja a un médico de forma controlada reasignando sus citas vigentes primero.
#         """
#         # Crea e inicializa una ventana secundaria de tipo Toplevel vinculada a la principal
#         modal = ctk.CTkToplevel(self.vista.ventana)
#         modal.title("Reasignación de citas")
#         modal.geometry("420x380")
#         modal.resizable(False, False)
#         modal.configure(fg_color="#1A1A1E")
#         modal.grab_set() # Captura todos los eventos; bloquea la ventana padre hasta resolver el modal

#         # COMPONENTES DE TEXTO EXPLICATIVOS
#         ctk.CTkLabel(modal,
#                      text="Reasignación de citas",
#                      font=("Segoe UI", 17, "bold"),
#                      text_color="#E8E8EC").pack(pady=(22, 4))
#         ctk.CTkLabel(modal,
#                      text=f"El médico {nombre} tiene citas activas.\nSelecciona un médico activo para reasignarlas.",
#                      font=("Segoe UI", 12),
#                      text_color="#8BA5BE",
#                      justify="center").pack(pady=(0, 16))

#         try:
#             with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
#                 usuarios = json.load(f)
            
#             # COMPRENSIÓN DE DICCIONARIOS: Filtra y compila las opciones para el menú desplegable
#             # Almacena como Texto legible: "Nombre Apellido — Especialidad" y mapea internamente su Valor: "NIT"
#             opciones = {
#                 f"{d['nombre']} {d['apellido']} — {d.get('especialidad', '')}": k
#                 for k, d in usuarios.items()
#                 if d.get("rol", "").lower() == "medico"
#                 and d.get("estado", "Activo") == "Activo"
#                 and k != nit # Excluye al médico que va a ser suspendido
#             }
#         except Exception:
#             opciones = {}

#         # CONTROL DE CASO DE BORDE: Si no hay otros médicos disponibles en el sistema para recibir la agenda
#         if not opciones:
#             ctk.CTkLabel(modal,
#                          text="No hay otros médicos activos disponibles.",
#                          text_color="#EF5350",
#                          font=("Segoe UI", 12)).pack(pady=10)
#             ctk.CTkButton(modal, text="Cerrar",
#                           fg_color="#242429", hover_color="#2A2A30",
#                           text_color="#E8E8EC",
#                           command=modal.destroy).pack(pady=10)
#             return

#         ctk.CTkLabel(modal, text="Médico destino:",
#                      text_color="#8BA5BE",
#                      font=("Segoe UI", 12)).pack(anchor="w", padx=30)

#         # Inicializa el menú desplegable (OptionMenu) con los candidatos seleccionables
#         seleccion = ctk




import json # Módulo nativa para la lectura y escritura de estructuras JSON
import pandas as pd # Librería de análisis de datos para la manipulación óptima de matrices y tablas CSV
from datetime import date # Componente para capturar la fecha del sistema en tiempo real
from tkinter import messagebox # Cuadros de diálogo emergentes estándar
import customtkinter as ctk # Interfaz optimizada con widgets modernos en modo oscuro
import tkinter as tk # Contenedor base de herramientas gráficas


# =============================================================================
# UTILIDAD: leer CSV siempre limpio (sin espacios iniciales en valores/columnas)
# =============================================================================
def _leer_csv(ruta):
    """
    FUNCIÓN DE SANITIZACIÓN: Carga un archivo CSV aplicando filtros de limpieza.
    Remueve espacios en blanco huérfanos para evitar fallos de coincidencia de cadenas (strings).
    """
    # Separa por punto y coma (;), omite espacios iniciales y preserva los IDs como texto (no numéricos)
    df = pd.read_csv(ruta, sep=";", skipinitialspace=True, dtype={"id_medico": str, "id_cita": str})
    
    # Limpia los espacios en blanco (.strip()) que puedan existir en los nombres de las columnas
    df.columns = df.columns.str.strip()
    
    # Aplica de manera interna una función lambda para limpiar los textos de cada celda individual
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    return df # Retorna el DataFrame de Pandas completamente purgado


class GestionMedicosController:
    def __init__(self, vista):
        """
        MÉTODO CONSTRUCTOR: Enlaza la vista con la lógica de negocio y
        establece las rutas físicas de los archivos de almacenamiento de datos.
        """
        self.vista = vista
        self.archivo_usuarios = "data/usuarios.json" # Archivo origen de perfiles
        self.archivo_citas    = "data/citas_registradas.csv" # Archivo origen de la agenda

        # VARIABLES DE CACHÉ / ESTADO INTERNO: Almacenan temporalmente al médico seleccionado en la UI
        self._nit_medico_activo    = None
        self._nombre_medico_activo = None
        self._esp_medico_activo    = None
        self._sexo_medico_activo   = None

    # ==========================================================================
    # CARGA Y DIBUJA LAS CARDS DE MÉDICOS
    # ==========================================================================
    def cargar_cards(self):
        """
        Lee el archivo de usuarios y citas, filtra el personal médico activo,
        calcula las estadísticas globales por género y genera las tarjetas en la interfaz.
        """
        # LIMPIEZA VISUAL: Destruye todas las tarjetas previas del contenedor antes de redibujar
        for w in self.vista.area_cards.winfo_children():
            w.destroy()

        # Reinicia los contadores gráficos de la pantalla a cero
        self.vista.contador_total.set(0)
        self.vista.contador_masculino.set(0)
        self.vista.contador_femenino.set(0)

        try:
            # LECTURA JSON: Carga los usuarios registrados en el sistema
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

            # LECTURA CSV VINCULADA: Intenta cargar las citas del archivo plano con Pandas
            try:
                df_citas = _leer_csv(self.archivo_citas)
                # Si el archivo está vacío o corrupto, inicializa una estructura de respaldo segura
                if df_citas.empty or "id_medico" not in df_citas.columns:
                    df_citas = pd.DataFrame(columns=["id_medico", "estado"])
            except (FileNotFoundError, pd.errors.EmptyDataError):
                # Si el archivo CSV no existe aún, crea un DataFrame vacío con las columnas necesarias
                df_citas = pd.DataFrame(columns=["id_medico", "estado"])

            # Variables de control para posicionar los elementos en una rejilla (Grid) de 2 columnas
            fila, col = 0, 0

            # Bucle principal para procesar a cada usuario del diccionario
            for nit, datos in usuarios.items():
                # CLAÚSULA DE FILTRADO 1: Si el usuario no ostenta el rol de 'medico', lo ignora
                if datos.get("rol", "").lower() != "medico":
                    continue
                # CLAÚSULA DE FILTRADO 2: Si el médico está inactivo o suspendido, no lo renderiza en el panel
                if datos.get("estado", "Activo") != "Activo":
                    continue

                # Extrae los datos descriptivos del médico actual
                sexo         = datos.get("sexo", "")
                especialidad = datos.get("especialidad", "")
                
                # CÁLCULO DE CITAS ACTIVAS: Utiliza condicionales vectoriales de Pandas para contar cuántas 
                # citas vigentes ("Pendiente" o "En curso") posee el médico actual mediante su NIT
                num_citas    = len(df_citas[
                    (df_citas["id_medico"].astype(str) == str(nit)) &
                    (df_citas["estado"].isin(["Pendiente", "En curso"]))
                ]) if not df_citas.empty else 0

                # Incrementa las estadísticas globales reflejadas en las tarjetas KPI superiores
                self.vista.contador_total.set(self.vista.contador_total.get() + 1)
                if sexo == "Masculino":
                    self.vista.contador_masculino.set(self.vista.contador_masculino.get() + 1)
                else:
                    self.vista.contador_femenino.set(self.vista.contador_femenino.get() + 1)

                # CONSTRUCCIÓN COMPONENTE: Invoca el método de la vista para instanciar la tarjeta física
                self.vista.agregar_card(
                    nit=nit,
                    nombre=datos.get("nombre", ""),
                    apellido=datos.get("apellido", ""),
                    sexo=sexo,
                    telefono=datos.get("telefono", ""),
                    especialidad=especialidad,
                    num_citas=num_citas,
                    fila=fila,
                    columna=col
                )

                # CÁLCULO LOGÍSTICO DE LA REJILLA: Controla que solo se ubiquen 2 tarjetas por fila (Columna 0 y Columna 1)
                col += 1
                if col > 1:
                    col = 0
                    fila += 1 # Salto de fila en el Grid visual

        except FileNotFoundError:
            print("❌ El archivo JSON no existe.")
        except Exception as e:
            # En caso de fallo grave, imprime el rastreo exacto de la línea de error (Traceback) sin detener la app
            print(f"❌ Error al cargar médicos: {e}")
            import traceback
            traceback.print_exc()

    # ==========================================================================
    # CARGA EL CONTADOR DE CITAS DE HOY
    # ==========================================================================
    def cargar_citas_hoy(self):
        """
        Filtra mediante Pandas las filas cuya fecha coincida exactamente con la 
        fecha actual del servidor e inyecta el número resultante en la interfaz.
        """
        try:
            df  = _leer_csv(self.archivo_citas)
            hoy = str(date.today()) # Convierte la fecha del sistema a formato de texto (AAAA-MM-DD)
            
            # Cuenta el total de registros que cumplen con la condición de fecha
            self.vista.contador_citas_hoy.set(len(df[df["fecha"] == hoy]))
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.vista.contador_citas_hoy.set(0) # Si no hay archivo o está vacío, el KPI es 0
        except Exception as e:
            print(f"Error al cargar citas de hoy: {e}")

    # ==========================================================================
    # MUESTRA LAS CITAS DE UN MÉDICO EN EL PANEL LATERAL
    # ==========================================================================
    def mostrar_citas_panel(self, nit, nombre, especialidad, sexo):
        """
        Guarda los datos del médico seleccionado en el estado temporal y extrae todas 
        sus citas agendadas para mostrarlas detalladamente en el panel de revisión lateral.
        """
        # Seteo de las propiedades del estado de la instancia activa
        self._nit_medico_activo    = nit
        self._nombre_medico_activo = nombre
        self._esp_medico_activo    = especialidad
        self._sexo_medico_activo   = sexo

        try:
            df           = _leer_csv(self.archivo_citas)
            # Filtra todas las citas vinculadas a la llave primaria del médico seleccionado
            citas_medico = df[df["id_medico"].astype(str) == str(nit)]
            
            # Convierte las filas del DataFrame en una lista de diccionarios nativos de Python para fácil lectura de la vista
            lista        = citas_medico.to_dict(orient="records")
        except FileNotFoundError:
            lista = []
        except Exception as e:
            print(f"Error al cargar citas del panel: {e}")
            lista = []

        # Ordena a la interfaz pintar el panel lateral con la lista estructurada de citas obtenidas
        self.vista.mostrar_panel_citas(nombre, especialidad, sexo, lista)

    # ==========================================================================
    # HELPER: obtiene médicos disponibles excluyendo al médico activo
    # ==========================================================================
    def _obtener_medicos_disponibles(self):
        """
        MÉTODO DE SOPORTE INTERNO: Compila un mapa de médicos alternativos que estén aptos 
        para recibir citas reasignadas, garantizando excluir al médico que se está procesando.
        """
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

            try:
                df_citas = _leer_csv(self.archivo_citas)
            except (FileNotFoundError, pd.errors.EmptyDataError):
                df_citas = pd.DataFrame(columns=["id_medico", "estado"])

            medicos = []
            for nit, datos in usuarios.items():
                # Descarta usuarios que no pertenezcan al cuerpo médico, inactivos o al médico de origen
                if datos.get("rol", "").lower() != "medico":
                    continue
                if datos.get("estado", "Activo") != "Activo":
                    continue
                if str(nit) == str(self._nit_medico_activo):
                    continue

                # Calcula la carga laboral actual del médico destino potencial (Citas activas)
                citas_activas = len(df_citas[
                    (df_citas["id_medico"].astype(str) == str(nit)) &
                    (df_citas["estado"].isin(["Pendiente", "En curso"]))
                ]) if not df_citas.empty else 0

                # Agrega el registro depurado al listado final de candidatos
                medicos.append({
                    "nit":          nit,
                    "nombre":       f"{datos.get('nombre', '')} {datos.get('apellido', '')}",
                    "especialidad": datos.get("especialidad", ""),
                    "sexo":         datos.get("sexo", ""),
                    "num_citas":    citas_activas,
                })
            return medicos # Retorna la colección de médicos candidatos disponibles

        except Exception as e:
            print(f"Error cargando médicos disponibles: {e}")
            return []

    # ==========================================================================
    # REASIGNACIÓN INDIVIDUAL
    # ==========================================================================
    def iniciar_reasignacion_individual(self, id_cita, info_cita):
        """Dispara el flujo visual para trasladar una única cita específica hacia otro médico."""
        self.vista.mostrar_panel_reasignacion(
            id_cita=id_cita,
            info_cita=info_cita,
            medicos_disponibles=self._obtener_medicos_disponibles(),
            es_masiva=False, # Flag que define comportamiento selectivo único
        )

    # ==========================================================================
    # REASIGNACIÓN MASIVA
    # ==========================================================================
    def iniciar_reasignacion_masiva(self):
        """Dispara el flujo visual para trasladar la agenda completa de citas vigentes de un médico."""
        self.vista.mostrar_panel_reasignacion(
            id_cita=None,
            info_cita=None,
            medicos_disponibles=self._obtener_medicos_disponibles(),
            es_masiva=True, # Flag que define un comportamiento de lote (Batch process)
        )

    # ==========================================================================
    # CONFIRMAR REASIGNACIÓN (individual o masiva)
    # ==========================================================================
    def confirmar_reasignacion(self, nit_destino, id_cita=None, es_masiva=False):
        """
        PROCESAMIENTO TRANSACCIONAL: Modifica físicamente el archivo CSV cambiando el 
        propietario de las citas. Ejecuta trazas de depuración (DEBUG) en consola para control de auditoría.
        """
        try:
            df = _leer_csv(self.archivo_citas)

            # TRAZAS DE AUDITORÍA (Logs de depuración del desarrollador)
            print(f"DEBUG → nit_destino: {nit_destino} | id_cita: {id_cita} | es_masiva: {es_masiva}")
            print(f"DEBUG → nit_activo: {self._nit_medico_activo}")
            print(f"DEBUG → columnas CSV: {df.columns.tolist()}")
            print(f"DEBUG → primeras filas:\n{df.head()}")

            # CASO A: OPERACIÓN EN LOTE (REASIGNACIÓN MASIVA)
            if es_masiva:
                # Genera una máscara booleana: localiza citas del médico origen que estén Pendientes o En Curso
                mask = (
                    (df["id_medico"].astype(str).str.strip() == str(self._nit_medico_activo).strip()) &
                    (df["estado"].isin(["Pendiente", "En curso"]))
                )
                cantidad = mask.sum() # Cuenta cuántas filas aplican para la mutación de datos
                print(f"DEBUG masiva → filas que matchean: {cantidad}")

                # Aplica indexación lógica (.loc) para cambiar el id_medico por el NIT destino en las filas filtradas
                df.loc[mask, "id_medico"] = str(nit_destino).strip()
                # Guarda los cambios sobreescribiendo el archivo original estructurado por punto y coma (;)
                df.to_csv(self.archivo_citas, index=False, sep=";")
                messagebox.showinfo("Reasignación masiva",
                    f"Se reasignaron {cantidad} cita(s) correctamente.")

            # CASO B: OPERACIÓN ATÓMICA (REASIGNACIÓN DE UNA CITA INDIVIDUAL)
            else:
                id_cita_limpio = str(id_cita).strip()
                # Genera una máscara estricta evaluando el ID de la cita y validando que pertenezca al médico activo
                mask = (
                    (df["id_cita"].astype(str).str.strip() == id_cita_limpio) &
                    (df["id_medico"].astype(str).str.strip() == str(self._nit_medico_activo).strip())
                )
                cantidad = mask.sum()
                print(f"DEBUG individual → buscando id_cita: '{id_cita_limpio}' | filas que matchean: {cantidad}")

                # Control de excepciones lógico: Si la búsqueda da 0, cancela la operación y lanza advertencia
                if cantidad == 0:
                    messagebox.showwarning("Sin coincidencia",
                        f"No se encontró la cita '{id_cita_limpio}' para este médico.")
                    return

                # Modifica el identificador del médico asignado a esa única cita en específico
                df.loc[mask, "id_medico"] = str(nit_destino).strip()
                df.to_csv(self.archivo_citas, index=False, sep=";")
                messagebox.showinfo("Cita reasignada", "La cita fue reasignada correctamente.")

            # FLUJO ACTUALIZACIÓN (REACTIVO): Refresca inmediatamente la vista para reflejar los cambios en tiempo real
            self.mostrar_citas_panel(
                self._nit_medico_activo,
                self._nombre_medico_activo,
                self._esp_medico_activo,
                self._sexo_medico_activo,
            )
            self.cargar_cards() # Re-calcula y dibuja las tarjetas de los médicos con los nuevos totales de agenda

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la reasignación:\n{e}")
            import traceback
            traceback.print_exc()

    # ==========================================================================
    # FLUJO DE BAJA: médico con citas → modal de reasignación + desactivar
    # ==========================================================================
    def iniciar_flujo_baja(self, nit, nombre):
        """
        FLUJO DE NEGOCIO AVANZADO: Abre una ventana modal de alta prioridad (grab_set) para obligar 
        a dar de baja a un médico de forma controlada reasignando sus citas vigentes primero.
        """
        # Crea e inicializa una ventana secundaria de tipo Toplevel vinculada a la principal
        modal = ctk.CTkToplevel(self.vista.ventana)
        modal.title("Reasignación de citas")
        modal.geometry("420x380")
        modal.resizable(False, False)
        modal.configure(fg_color="#1A1A1E")
        modal.grab_set() # Captura todos los eventos; bloquea la ventana padre hasta resolver el modal

        # COMPONENTES DE TEXTO EXPLICATIVOS
        ctk.CTkLabel(modal,
                     text="Reasignación de citas",
                     font=("Segoe UI", 17, "bold"),
                     text_color="#E8E8EC").pack(pady=(22, 4))
        ctk.CTkLabel(modal,
                     text=f"El médico {nombre} tiene citas activas.\nSelecciona un médico activo para reasignarlas.",
                     font=("Segoe UI", 12),
                     text_color="#8BA5BE",
                     justify="center").pack(pady=(0, 16))

        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
            
            # COMPRENSIÓN DE DICCIONARIOS: Filtra y compila las opciones para el menú desplegable
            # Almacena como Texto legible: "Nombre Apellido — Especialidad" y mapea internamente su Valor: "NIT"
            opciones = {
                f"{d['nombre']} {d['apellido']} — {d.get('especialidad', '')}": k
                for k, d in usuarios.items()
                if d.get("rol", "").lower() == "medico"
                and d.get("estado", "Activo") == "Activo"
                and k != nit # Excluye al médico que va a ser suspendido
            }
        except Exception:
            opciones = {}

        # CONTROL DE CASO DE BORDE: Si no hay otros médicos disponibles en el sistema para recibir la agenda
        if not opciones:
            ctk.CTkLabel(modal,
                         text="No hay otros médicos activos disponibles.",
                         text_color="#EF5350",
                         font=("Segoe UI", 12)).pack(pady=10)
            ctk.CTkButton(modal, text="Cerrar",
                          fg_color="#242429", hover_color="#2A2A30",
                          text_color="#E8E8EC",
                          command=modal.destroy).pack(pady=10)
            return

        ctk.CTkLabel(modal, text="Médico destino:",
                     text_color="#8BA5BE",
                     font=("Segoe UI", 12)).pack(anchor="w", padx=30)

        # Inicializa el menú desplegable (OptionMenu) con los candidatos seleccionables
        seleccion = ctk.StringVar(value=list(opciones.keys())[0])
        ctk.CTkOptionMenu(modal,
                          values=list(opciones.keys()),
                          variable=seleccion,
                          fg_color="#242429",
                          button_color="#45A29E",
                          button_hover_color="#3a8a87",
                          text_color="#E8E8EC",
                          font=("Segoe UI", 12),
                          width=360).pack(padx=30, pady=(4, 20))

        def confirmar_baja():
            """Sub-función de confirmación encapsulada para ejecutar la reasignación y el cambio de estado."""
            nit_destino = opciones[seleccion.get()] # Resuelve el NIT real del médico destino
            try:
                # PASO 1: Reasigna masivamente toda la agenda vigente del médico saliente en el CSV
                df   = _leer_csv(self.archivo_citas)
                mask = (df["id_medico"].astype(str) == str(nit)) & \
                       (df["estado"].isin(["Pendiente", "En curso"]))
                df.loc[mask, "id_medico"] = nit_destino
                df.to_csv(self.archivo_citas, index=False, sep=";")

                # PASO 2: Modifica las propiedades del usuario en el JSON cambiando su estado a "Inactivo"
                with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                    usuarios = json.load(f)
                
                usuarios[nit]["estado"] = "Inactivo" # Baja lógica preventiva
                
                with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                    json.dump(usuarios, f, ensure_ascii=False, indent=4)

                # PASO 3: Notifica el éxito del proceso y destruye la interfaz del modal liberando los recursos
                messagebox.showinfo("Listo",
                    f"Citas reasignadas.\nEl médico {nombre} ha sido desactivado.")
                modal.destroy()
                
                # PASO 4: Refresca el entorno principal
                self.cargar_cards()
                self.vista._construir_panel_vacio() # Limpia el panel de visualización detallada por seguridad
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo completar la reasignación:\n{e}")

        # BOTONES DE CONTROL DE CIERRE Y CONFIRMACIÓN
        ctk.CTkButton(modal, text="Confirmar reasignación",
                      fg_color="#45A29E", hover_color="#3a8a87",
                      text_color="#111114",
                      font=("Segoe UI", 13, "bold"),
                      height=42, corner_radius=8,
                      command=confirmar_baja).pack(fill="x", padx=30, pady=(0, 8))
                      
        ctk.CTkButton(modal, text="Cancelar",
                      fg_color="transparent", hover_color="#242429",
                      text_color="#6A6A72",
                      font=("Segoe UI", 12), height=36,
                      command=modal.destroy).pack(fill="x", padx=30)

    # ==========================================================================
    # ELIMINAR MÉDICO (sin citas activas)
    # ==========================================================================
    def eliminar_medico(self, nit, nombre):
        """
        ELIMINACIÓN FÍSICA: Remueve de forma definitiva la clave del médico del 
        diccionario JSON siempre y cuando su historial esté libre de citas vigentes.
        """
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar al médico {nombre}?\nEsta acción no se puede deshacer."
        )
        if confirmar:
            try:
                with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                    usuarios = json.load(f)
                
                # Si el NIT existe en las propiedades mapeadas, remueve la llave del objeto diccionario
                if nit in usuarios:
                    del usuarios[nit]
                    
                    with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                        json.dump(usuarios, f, ensure_ascii=False, indent=4)
                    
                    messagebox.showinfo("Eliminado", "Médico eliminado correctamente.")
                    self.cargar_cards() # Regenera los componentes visuales de las tarjetas
                    self.vista._construir_panel_vacio() # Reestablece el panel derecho
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    # ==========================================================================
    # FORMULARIOS (Mapeo de vistas secundarias)
    # ==========================================================================
    @staticmethod
    def abrir_formulario_registro(ventana, controlador):
        """Inicializa e invoca la vista del formulario para la inserción de un nuevo médico."""
        from view.admin.registro_medico_view import RegistroMedicoView
        RegistroMedicoView(ventana, controlador)        

    def abrir_formulario_edicion(self, nit):
        """Abre la vista del formulario inyectando el NIT para realizar una actualización (Update)."""
        from view.admin.registro_medico_view import RegistroMedicoView
        RegistroMedicoView(self.vista.ventana, self, nit_editar=nit)

    # ==========================================================================
    # REGRESAR AL HOME
    # ==========================================================================
    @staticmethod
    def regresar_ventana(ventana, datos_usuario):
        """Navigación segura: Destruye el módulo de médicos y restaura la pantalla de menú Home."""
        try:
            from view.admin.home_view import HomeVentana
            ventana.destroy() # Libera memoria RAM
            app = HomeVentana(datos_usuario) # Traspasa los datos de la sesión activa
            if hasattr(app, "ventana"):
                app.ventana.mainloop()
            else:
                app.mainloop()
        except Exception as e:
            print(f"Error al regresar: {e}")

    # ==========================================================================
    # CERRAR SESIÓN
    # ==========================================================================
    @staticmethod
    def cerrar_sesion(ventana):
        """Protocolo de interrupción de sesión para redirigir al Login principal de la aplicación."""
        respuesta = messagebox.askyesno("Cierre de sesión", "¿Está seguro de cerrar la sesión?")
        if respuesta:
            ventana.destroy()
            from main import iniciar_app
            iniciar_app() # Reinicia la aplicación desde su raíz ejecutable




    
