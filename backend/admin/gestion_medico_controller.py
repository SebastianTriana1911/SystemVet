import json
import pandas as pd
from datetime import date
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk


# =============================================================================
# UTILIDAD: leer CSV siempre limpio (sin espacios iniciales en valores/columnas)
# =============================================================================
def _leer_csv(ruta):
    df = pd.read_csv(ruta, skipinitialspace=True, dtype={"id_medico": str, "id_cita": str})
    df.columns = df.columns.str.strip()
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    return df
    # df = pd.read_csv(ruta, skipinitialspace=True)
    # df.columns = df.columns.str.strip()
    # df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    # return df


class GestionMedicosController:
    def __init__(self, vista):
        self.vista = vista
        self.archivo_usuarios = "data/usuarios.json"
        self.archivo_citas    = "data/citas.csv"

        # Estado interno del médico activo en el panel lateral
        self._nit_medico_activo    = None
        self._nombre_medico_activo = None
        self._esp_medico_activo    = None
        self._sexo_medico_activo   = None

    # ==========================================================================
    # CARGA Y DIBUJA LAS CARDS DE MÉDICOS
    # ==========================================================================
    def cargar_cards(self):
        for w in self.vista.area_cards.winfo_children():
            w.destroy()

        self.vista.contador_total.set(0)
        self.vista.contador_masculino.set(0)
        self.vista.contador_femenino.set(0)

        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

            try:
                df_citas = _leer_csv(self.archivo_citas)
                if df_citas.empty or "id_medico" not in df_citas.columns:
                    df_citas = pd.DataFrame(columns=["id_medico", "estado"])
            except (FileNotFoundError, pd.errors.EmptyDataError):
                df_citas = pd.DataFrame(columns=["id_medico", "estado"])

            fila, col = 0, 0

            for nit, datos in usuarios.items():
                if datos.get("rol", "").lower() != "medico":
                    continue
                if datos.get("estado", "Activo") != "Activo":
                    continue

                sexo         = datos.get("sexo", "")
                especialidad = datos.get("especialidad", "")
                num_citas    = len(df_citas[
                    (df_citas["id_medico"].astype(str) == str(nit)) &
                    (df_citas["estado"].isin(["Pendiente", "En curso"]))
                ]) if not df_citas.empty else 0

                self.vista.contador_total.set(self.vista.contador_total.get() + 1)
                if sexo == "Masculino":
                    self.vista.contador_masculino.set(self.vista.contador_masculino.get() + 1)
                else:
                    self.vista.contador_femenino.set(self.vista.contador_femenino.get() + 1)

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

                col += 1
                if col > 1:
                    col = 0
                    fila += 1

        except FileNotFoundError:
            print("❌ El archivo JSON no existe.")
        except Exception as e:
            print(f"❌ Error al cargar médicos: {e}")
            import traceback
            traceback.print_exc()

    # ==========================================================================
    # CARGA EL CONTADOR DE CITAS DE HOY
    # ==========================================================================
    def cargar_citas_hoy(self):
        try:
            df  = _leer_csv(self.archivo_citas)
            hoy = str(date.today())
            self.vista.contador_citas_hoy.set(len(df[df["fecha"] == hoy]))
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.vista.contador_citas_hoy.set(0)
        except Exception as e:
            print(f"Error al cargar citas de hoy: {e}")

    # ==========================================================================
    # MUESTRA LAS CITAS DE UN MÉDICO EN EL PANEL LATERAL
    # ==========================================================================
    def mostrar_citas_panel(self, nit, nombre, especialidad, sexo):
        self._nit_medico_activo    = nit
        self._nombre_medico_activo = nombre
        self._esp_medico_activo    = especialidad
        self._sexo_medico_activo   = sexo

        try:
            df           = _leer_csv(self.archivo_citas)
            citas_medico = df[df["id_medico"].astype(str) == str(nit)]
            lista        = citas_medico.to_dict(orient="records")
        except FileNotFoundError:
            lista = []
        except Exception as e:
            print(f"Error al cargar citas del panel: {e}")
            lista = []

        self.vista.mostrar_panel_citas(nombre, especialidad, sexo, lista)

    # ==========================================================================
    # HELPER: obtiene médicos disponibles excluyendo al médico activo
    # ==========================================================================
    def _obtener_medicos_disponibles(self):
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

            try:
                df_citas = _leer_csv(self.archivo_citas)
            except (FileNotFoundError, pd.errors.EmptyDataError):
                df_citas = pd.DataFrame(columns=["id_medico", "estado"])

            medicos = []
            for nit, datos in usuarios.items():
                if datos.get("rol", "").lower() != "medico":
                    continue
                if datos.get("estado", "Activo") != "Activo":
                    continue
                if str(nit) == str(self._nit_medico_activo):
                    continue

                citas_activas = len(df_citas[
                    (df_citas["id_medico"].astype(str) == str(nit)) &
                    (df_citas["estado"].isin(["Pendiente", "En curso"]))
                ]) if not df_citas.empty else 0

                medicos.append({
                    "nit":          nit,
                    "nombre":       f"{datos.get('nombre', '')} {datos.get('apellido', '')}",
                    "especialidad": datos.get("especialidad", ""),
                    "sexo":         datos.get("sexo", ""),
                    "num_citas":    citas_activas,
                })
            return medicos

        except Exception as e:
            print(f"Error cargando médicos disponibles: {e}")
            return []

    # ==========================================================================
    # REASIGNACIÓN INDIVIDUAL
    # ==========================================================================
    def iniciar_reasignacion_individual(self, id_cita, info_cita):
        self.vista.mostrar_panel_reasignacion(
            id_cita=id_cita,
            info_cita=info_cita,
            medicos_disponibles=self._obtener_medicos_disponibles(),
            es_masiva=False,
        )

    # ==========================================================================
    # REASIGNACIÓN MASIVA
    # ==========================================================================
    def iniciar_reasignacion_masiva(self):
        self.vista.mostrar_panel_reasignacion(
            id_cita=None,
            info_cita=None,
            medicos_disponibles=self._obtener_medicos_disponibles(),
            es_masiva=True,
        )

    # ==========================================================================
    # CONFIRMAR REASIGNACIÓN (individual o masiva)
    # ==========================================================================
    # def confirmar_reasignacion(self, nit_destino, id_cita=None, es_masiva=False):
    #     try:
    #         df = _leer_csv(self.archivo_citas)

    #         if es_masiva:
    #             mask = (
    #                 (df["id_medico"].astype(str) == str(self._nit_medico_activo)) &
    #                 (df["estado"].isin(["Pendiente", "En curso"]))
    #             )
    #             cantidad = mask.sum()
    #             df.loc[mask, "id_medico"] = nit_destino
    #             df.to_csv(self.archivo_citas, index=False)
    #             messagebox.showinfo(
    #                 "Reasignación masiva",
    #                 f"Se reasignaron {cantidad} cita(s) correctamente."
    #             )
    #         else:
    #             if "id_cita" in df.columns:
    #                 mask = df["id_cita"].astype(str) == str(id_cita)
    #             else:
    #                 activas = (
    #                     (df["id_medico"].astype(str) == str(self._nit_medico_activo)) &
    #                     (df["estado"].isin(["Pendiente", "En curso"]))
    #                 )
    #                 mask = activas & (df.index == df[activas].index[0])

    #             df.loc[mask, "id_medico"] = nit_destino
    #             df.to_csv(self.archivo_citas, index=False)
    #             messagebox.showinfo("Cita reasignada", "La cita fue reasignada correctamente.")

    #         # Refrescar
    #         self.mostrar_citas_panel(
    #             self._nit_medico_activo,
    #             self._nombre_medico_activo,
    #             self._esp_medico_activo,
    #             self._sexo_medico_activo,
    #         )
    #         self.cargar_cards()

    #     except Exception as e:
    #         messagebox.showerror("Error", f"No se pudo completar la reasignación:\n{e}")
    def confirmar_reasignacion(self, nit_destino, id_cita=None, es_masiva=False):
        try:
            df = _leer_csv(self.archivo_citas)

            print(f"DEBUG → nit_destino: {nit_destino} | id_cita: {id_cita} | es_masiva: {es_masiva}")
            print(f"DEBUG → nit_activo: {self._nit_medico_activo}")
            print(f"DEBUG → columnas CSV: {df.columns.tolist()}")
            print(f"DEBUG → primeras filas:\n{df.head()}")

            if es_masiva:
                mask = (
                    (df["id_medico"].astype(str).str.strip() == str(self._nit_medico_activo).strip()) &
                    (df["estado"].isin(["Pendiente", "En curso"]))
                )
                cantidad = mask.sum()
                print(f"DEBUG masiva → filas que matchean: {cantidad}")

                df.loc[mask, "id_medico"] = str(nit_destino).strip()
                df.to_csv(self.archivo_citas, index=False)
                messagebox.showinfo("Reasignación masiva",
                    f"Se reasignaron {cantidad} cita(s) correctamente.")

            else:
                id_cita_limpio = str(id_cita).strip()
                mask = (
                    (df["id_cita"].astype(str).str.strip() == id_cita_limpio) &
                    (df["id_medico"].astype(str).str.strip() == str(self._nit_medico_activo).strip())
                )
                cantidad = mask.sum()
                print(f"DEBUG individual → buscando id_cita: '{id_cita_limpio}' | filas que matchean: {cantidad}")

                if cantidad == 0:
                    messagebox.showwarning("Sin coincidencia",
                        f"No se encontró la cita '{id_cita_limpio}' para este médico.")
                    return

                df.loc[mask, "id_medico"] = str(nit_destino).strip()
                df.to_csv(self.archivo_citas, index=False)
                messagebox.showinfo("Cita reasignada", "La cita fue reasignada correctamente.")

            # Refrescar panel y cards
            self.mostrar_citas_panel(
                self._nit_medico_activo,
                self._nombre_medico_activo,
                self._esp_medico_activo,
                self._sexo_medico_activo,
            )
            self.cargar_cards()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la reasignación:\n{e}")
            import traceback
            traceback.print_exc()



    # ==========================================================================
    # FLUJO DE BAJA: médico con citas → modal de reasignación + desactivar
    # ==========================================================================
    def iniciar_flujo_baja(self, nit, nombre):
        modal = ctk.CTkToplevel(self.vista.ventana)
        modal.title("Reasignación de citas")
        modal.geometry("420x380")
        modal.resizable(False, False)
        modal.configure(fg_color="#1A1A1E")
        modal.grab_set()

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
            opciones = {
                f"{d['nombre']} {d['apellido']} — {d.get('especialidad', '')}": k
                for k, d in usuarios.items()
                if d.get("rol", "").lower() == "medico"
                and d.get("estado", "Activo") == "Activo"
                and k != nit
            }
        except Exception:
            opciones = {}

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
            nit_destino = opciones[seleccion.get()]
            try:
                df   = _leer_csv(self.archivo_citas)
                mask = (df["id_medico"].astype(str) == str(nit)) & \
                       (df["estado"].isin(["Pendiente", "En curso"]))
                df.loc[mask, "id_medico"] = nit_destino
                df.to_csv(self.archivo_citas, index=False)

                with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                    usuarios = json.load(f)
                usuarios[nit]["estado"] = "Inactivo"
                with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                    json.dump(usuarios, f, ensure_ascii=False, indent=4)

                messagebox.showinfo("Listo",
                    f"Citas reasignadas.\nEl médico {nombre} ha sido desactivado.")
                modal.destroy()
                self.cargar_cards()
                self.vista._construir_panel_vacio()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo completar la reasignación:\n{e}")

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
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar al médico {nombre}?\nEsta acción no se puede deshacer."
        )
        if confirmar:
            try:
                with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                    usuarios = json.load(f)
                if nit in usuarios:
                    del usuarios[nit]
                    with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
                        json.dump(usuarios, f, ensure_ascii=False, indent=4)
                    messagebox.showinfo("Eliminado", "Médico eliminado correctamente.")
                    self.cargar_cards()
                    self.vista._construir_panel_vacio()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")




    # ==========================================================================
    # FORMULARIOS (stubs)
    # ==========================================================================
    def abrir_formulario_registro(ventana, controlador):
        from view.admin.registro_medico_view import RegistroMedicoView
        RegistroMedicoView(ventana, controlador)        


    def abrir_formulario_edicion(self, nit):
        from view.admin.registro_medico_view import RegistroMedicoView
        RegistroMedicoView(self.vista.ventana, self, nit_editar=nit)


    # ==========================================================================
    # REGRESAR AL HOME
    # ==========================================================================
    def regresar_ventana(ventana, datos_usuario):
        try:
            from view.admin.home_view import HomeVentana
            ventana.destroy()
            app = HomeVentana(datos_usuario)
            if hasattr(app, "ventana"):
                app.ventana.mainloop()
            else:
                app.mainloop()
        except Exception as e:
            print(f"Error al regresar: {e}")


    # ==========================================================================
    # CERRAR SESIÓN
    # ==========================================================================
    def cerrar_sesion(ventana):
        respuesta = messagebox.askyesno("Cierre de sesión", "¿Está seguro de cerrar la sesión?")
        if respuesta:
            ventana.destroy()
            from main import iniciar_app
            iniciar_app()