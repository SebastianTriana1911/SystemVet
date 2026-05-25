import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from tkinter import messagebox, filedialog

# ── Paleta SystemVet ──────────────────────────────────────────────────────────
FONDO      = "#1A1A1E"
FONDO_EJES = "#242429"
TEAL       = "#45A29E"
PURP       = "#CE93D8"
AMBER      = "#FFB300"
VERDE      = "#66BB6A"
ROJO       = "#EF5350"
AZUL_GR    = "#8BA5BE"
TEXTO      = "#E8E8EC"
GRID_C     = "#2A2A30"

# Color por estado y por animal
COLOR_ESTADO = {
    "Pendiente":  VERDE,
    "En curso":   TEAL,
    "Completada": AZUL_GR,
    "Cancelada":  ROJO,
}
COLOR_ANIMAL = {
    "Perro": TEAL,
    "Gato":  PURP,
}


def _estilo_dark(ax, fig):
    fig.patch.set_facecolor(FONDO)
    ax.set_facecolor(FONDO_EJES)
    ax.tick_params(colors=TEXTO, labelsize=10)
    ax.xaxis.label.set_color(TEXTO)
    ax.yaxis.label.set_color(TEXTO)
    ax.title.set_color(TEXTO)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_C)
    ax.grid(True, color=GRID_C, linestyle="--", linewidth=0.6, alpha=0.8)
    ax.set_axisbelow(True)


class ReportesController:
    def __init__(self, vista):
        self.vista            = vista
        self.archivo_citas    = "data/citas.csv"
        self.archivo_usuarios = "data/usuarios.json"
        self._fig_actual      = None

    # ==========================================================================
    # PUNTO DE ENTRADA
    # ==========================================================================
    def generar_grafico(self, filtros):
        tipo_grafico = filtros["tipo_grafico"]
        animales     = filtros["animales"]
        estados      = filtros["estados"]
        fecha_ini    = filtros["fecha_ini"]
        fecha_fin    = filtros["fecha_fin"]

        # Validaciones básicas
        if not animales:
            self.vista.mostrar_error("⚠ Selecciona al menos un tipo de animal.")
            return
        if not estados:
            self.vista.mostrar_error("⚠ Selecciona al menos un estado de cita.")
            return
        if not fecha_ini or not fecha_fin:
            self.vista.mostrar_error("⚠ Ingresa ambas fechas para generar el gráfico.")
            return
        try:
            dt_ini = datetime.strptime(fecha_ini, "%Y-%m-%d")
            dt_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            if dt_ini > dt_fin:
                self.vista.mostrar_error(
                    "⚠ La fecha inicial no puede ser mayor que la fecha final.")
                return
        except ValueError:
            self.vista.mostrar_error(
                "⚠ Formato de fecha inválido.\nUsa el formato AAAA-MM-DD.")
            return

        # Cargar y filtrar CSV
        df = self._cargar_csv()
        if df is None:
            return

        df = df[
            df["tipo_animal"].str.lower().isin([a.lower() for a in animales]) &
            df["estado"].isin(estados) &
            (df["fecha"] >= fecha_ini) &
            (df["fecha"] <= fecha_fin)
        ].copy()

        if df.empty:
            self.vista.mostrar_error(
                "⚠ No hay citas con los filtros seleccionados\n"
                f"en el período {fecha_ini} → {fecha_fin}.")
            return

        # Métricas globales
        conteo_dia = df.groupby("fecha").size()
        metricas = {
            "total":    int(len(df)),
            "animales": "/".join(animales),
            "pico":     int(conteo_dia.max()) if not conteo_dia.empty else 0,
        }

        # Despacho al gráfico
        dispatch = {
            "Histograma por Estado": self._histograma_por_estado,
            "Línea de Tendencia":    self._linea_tendencia,
            "Barras por Médico":     self._barras_medico,
            "Dona por Estado":       self._dona_estado,
        }
        metodo = dispatch.get(tipo_grafico)
        if metodo is None:
            self.vista.mostrar_error("Tipo de gráfico no reconocido.")
            return

        resultado = metodo(df, animales, estados, fecha_ini, fecha_fin)
        if resultado is None:
            return
        fig, titulo = resultado

        self._fig_actual = fig
        self.vista.mostrar_canvas(fig, titulo, metricas)

    # ==========================================================================
    # CARGA DEL CSV
    # ==========================================================================
    def _cargar_csv(self):
        try:
            df = pd.read_csv(self.archivo_citas, skipinitialspace=True)
            df.columns = df.columns.str.strip()
            df = df.apply(
                lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x)
            )
        except FileNotFoundError:
            self.vista.mostrar_error("⚠ No se encontró el archivo de citas.")
            return None
        except pd.errors.EmptyDataError:
            self.vista.mostrar_error("⚠ El archivo de citas está vacío.")
            return None
        except Exception as e:
            self.vista.mostrar_error(f"⚠ Error al leer el archivo:\n{e}")
            return None

        for col in ("estado", "tipo_animal", "fecha"):
            if col not in df.columns:
                self.vista.mostrar_error(f"⚠ El CSV no tiene la columna '{col}'.")
                return None

        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df = df.dropna(subset=["fecha"])
        return df

    # ==========================================================================
    # GRÁFICO 1 — HISTOGRAMA AGRUPADO POR ESTADO (y opcionalmente por animal)
    # ==========================================================================
    def _histograma_por_estado(self, df, animales, estados, fecha_ini, fecha_fin):
        """
        Barras agrupadas: cada grupo es un estado, dentro del grupo una barra
        por tipo de animal.  Si hay un solo animal, una barra por estado.
        """
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        _estilo_dark(ax, fig)
        ax.grid(axis="x", color=GRID_C, linestyle="--", linewidth=0.6, alpha=0)
        ax.grid(axis="y", color=GRID_C, linestyle="--", linewidth=0.6, alpha=0.8)

        n_animales = len(animales)
        ancho      = 0.35 if n_animales > 1 else 0.5
        x          = np.arange(len(estados))

        for i, animal in enumerate(animales):
            conteos = []
            for estado in estados:
                n = len(df[(df["tipo_animal"].str.lower() == animal.lower()) &
                           (df["estado"] == estado)])
                conteos.append(n)

            offset = (i - (n_animales - 1) / 2) * ancho
            bars   = ax.bar(x + offset, conteos, ancho,
                            color=COLOR_ANIMAL[animal],
                            alpha=0.9, label=animal,
                            edgecolor=FONDO_EJES, linewidth=0.5)

            for bar, val in zip(bars, conteos):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 0.15,
                            str(val),
                            ha="center", va="bottom",
                            color=TEXTO, fontsize=9, fontweight="bold")

        ax.set_xticks(x)
        ax.set_xticklabels(estados, color=TEXTO, fontsize=10)
        ax.set_xlabel("Estado de la Cita", fontsize=11, labelpad=8)
        ax.set_ylabel("Cantidad de Citas", fontsize=11, labelpad=8)
        ax.yaxis.get_major_locator().set_params(integer=True)

        if n_animales > 1:
            legend = ax.legend(facecolor=FONDO_EJES, edgecolor=GRID_C,
                               labelcolor=TEXTO, fontsize=10)

        fig.tight_layout()
        animales_txt = " y ".join(animales)
        titulo = (f"Citas por Estado — {animales_txt}   "
                  f"({fecha_ini} → {fecha_fin})")
        return fig, titulo

    # ==========================================================================
    # GRÁFICO 2 — LÍNEA DE TENDENCIA (por animal y/o estado)
    # ==========================================================================
    def _linea_tendencia(self, df, animales, estados, fecha_ini, fecha_fin):
        """
        Una línea por cada combinación animal + estado.
        Si hay un animal y varios estados → línea por estado.
        Si hay varios animales y un estado → línea por animal.
        Si hay varios de ambos → línea por cada combinación.
        """
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        _estilo_dark(ax, fig)

        series_dibujadas = 0

        # Decidir granularidad de las series
        if len(animales) == 1 and len(estados) == 1:
            # Una sola línea
            sub = df.copy()
            conteo = sub.groupby("fecha").size().reset_index(name="n")
            if not conteo.empty:
                ax.plot(conteo["fecha"], conteo["n"],
                        color=COLOR_ANIMAL[animales[0]],
                        linewidth=2.2, marker="o", markersize=5,
                        markerfacecolor=AMBER,
                        markeredgecolor=FONDO, markeredgewidth=1,
                        label=f"{animales[0]} / {estados[0]}")
                ax.fill_between(conteo["fecha"], conteo["n"],
                                color=COLOR_ANIMAL[animales[0]], alpha=0.10)
                series_dibujadas += 1

        elif len(animales) > 1 and len(estados) == 1:
            for animal in animales:
                sub    = df[df["tipo_animal"].str.lower() == animal.lower()]
                conteo = sub.groupby("fecha").size().reset_index(name="n")
                if not conteo.empty:
                    ax.plot(conteo["fecha"], conteo["n"],
                            color=COLOR_ANIMAL[animal],
                            linewidth=2.2, marker="o", markersize=5,
                            markerfacecolor=AMBER,
                            markeredgecolor=FONDO, markeredgewidth=1,
                            label=animal)
                    ax.fill_between(conteo["fecha"], conteo["n"],
                                    color=COLOR_ANIMAL[animal], alpha=0.08)
                    series_dibujadas += 1

        elif len(animales) == 1 and len(estados) > 1:
            for estado in estados:
                sub    = df[df["estado"] == estado]
                conteo = sub.groupby("fecha").size().reset_index(name="n")
                if not conteo.empty:
                    ax.plot(conteo["fecha"], conteo["n"],
                            color=COLOR_ESTADO[estado],
                            linewidth=2.2, marker="o", markersize=5,
                            markerfacecolor=AMBER,
                            markeredgecolor=FONDO, markeredgewidth=1,
                            label=estado)
                    series_dibujadas += 1

        else:
            # Varias combinaciones: una línea por animal-estado
            colores_ciclo = [TEAL, PURP, AMBER, VERDE, ROJO, AZUL_GR]
            idx = 0
            for animal in animales:
                for estado in estados:
                    sub = df[
                        (df["tipo_animal"].str.lower() == animal.lower()) &
                        (df["estado"] == estado)
                    ]
                    conteo = sub.groupby("fecha").size().reset_index(name="n")
                    if not conteo.empty:
                        color = colores_ciclo[idx % len(colores_ciclo)]
                        ax.plot(conteo["fecha"], conteo["n"],
                                color=color, linewidth=2,
                                marker="o", markersize=4,
                                markerfacecolor=color,
                                markeredgecolor=FONDO, markeredgewidth=1,
                                label=f"{animal} / {estado}")
                        series_dibujadas += 1
                        idx += 1

        if series_dibujadas == 0:
            self.vista.mostrar_error(
                "⚠ No hay datos suficientes para trazar la línea de tendencia.")
            plt.close(fig)
            return None

        ax.set_xlabel("Fecha", fontsize=11, labelpad=8)
        ax.set_ylabel("Cantidad de Citas", fontsize=11, labelpad=8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.yaxis.get_major_locator().set_params(integer=True)
        fig.autofmt_xdate(rotation=30)

        if series_dibujadas > 1:
            ax.legend(facecolor=FONDO_EJES, edgecolor=GRID_C,
                      labelcolor=TEXTO, fontsize=9)

        fig.tight_layout()
        animales_txt = " y ".join(animales)
        titulo = (f"Tendencia de Citas — {animales_txt}   "
                  f"({fecha_ini} → {fecha_fin})")
        return fig, titulo

    # ==========================================================================
    # GRÁFICO 3 — BARRAS POR MÉDICO
    # ==========================================================================
    def _barras_medico(self, df, animales, estados, fecha_ini, fecha_fin):
        if "id_medico" not in df.columns:
            self.vista.mostrar_error("⚠ El CSV no tiene la columna 'id_medico'.")
            return None

        nombres = self._nombres_medicos()
        conteo  = df.groupby("id_medico").size().reset_index(name="cantidad")
        conteo["id_medico"] = conteo["id_medico"].astype(str)
        conteo["medico"]    = conteo["id_medico"].map(
            lambda n: nombres.get(str(n), f"Médico {n}")
        )
        conteo = conteo.sort_values("cantidad", ascending=False)

        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        _estilo_dark(ax, fig)

        colores = [TEAL if i % 2 == 0 else PURP for i in range(len(conteo))]
        bars    = ax.bar(conteo["medico"], conteo["cantidad"],
                         color=colores, alpha=0.9,
                         edgecolor=FONDO_EJES, linewidth=0.5)

        for bar, val in zip(bars, conteo["cantidad"]):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.15,
                    str(int(val)),
                    ha="center", va="bottom",
                    color=TEXTO, fontsize=10, fontweight="bold")

        ax.set_xlabel("Médico", fontsize=11, labelpad=8)
        ax.set_ylabel("Cantidad de Citas", fontsize=11, labelpad=8)
        ax.yaxis.get_major_locator().set_params(integer=True)
        plt.xticks(rotation=20, ha="right")
        fig.tight_layout()

        animales_txt = " y ".join(animales)
        titulo = (f"Citas por Médico — {animales_txt}   "
                  f"({fecha_ini} → {fecha_fin})")
        return fig, titulo

    # ==========================================================================
    # GRÁFICO 4 — DONA POR ESTADO
    # ==========================================================================
    def _dona_estado(self, df, animales, estados, fecha_ini, fecha_fin):
        """
        Gráfico de dona: proporciones de cada estado seleccionado.
        Si hay dos animales genera dos donas lado a lado para comparar.
        """
        if len(animales) == 1:
            fig, axes = plt.subplots(1, 1, figsize=(6, 4.5))
            axes = [axes]
        else:
            fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))

        fig.patch.set_facecolor(FONDO)

        for ax, animal in zip(axes, animales):
            sub     = df[df["tipo_animal"].str.lower() == animal.lower()]
            conteos = [len(sub[sub["estado"] == e]) for e in estados]
            colores = [COLOR_ESTADO[e] for e in estados]

            # Filtrar estados con 0 citas para no distorsionar la dona
            pares = [(e, c, col) for e, c, col in zip(estados, conteos, colores) if c > 0]
            if not pares:
                ax.text(0.5, 0.5, f"Sin datos\npara {animal}",
                        ha="center", va="center", color=TEXTO,
                        fontsize=12, transform=ax.transAxes)
                ax.axis("off")
                continue

            etiq, vals, cols = zip(*pares)

            wedges, texts, autotexts = ax.pie(
                vals,
                labels=None,
                colors=cols,
                autopct="%1.1f%%",
                pctdistance=0.78,
                startangle=90,
                wedgeprops=dict(width=0.52, edgecolor=FONDO, linewidth=2),
            )
            for at in autotexts:
                at.set_color(TEXTO)
                at.set_fontsize(10)
                at.set_fontweight("bold")

            # Hueco central con total
            total = sum(vals)
            ax.text(0, 0, f"{total}\ncitas",
                    ha="center", va="center",
                    color=TEXTO, fontsize=13, fontweight="bold")

            ax.set_title(animal,
                         color=COLOR_ANIMAL.get(animal, TEAL),
                         fontsize=13, fontweight="bold", pad=8)

            ax.legend(wedges, etiq,
                      loc="lower center",
                      bbox_to_anchor=(0.5, -0.14),
                      ncol=len(etiq),
                      facecolor=FONDO_EJES, edgecolor=GRID_C,
                      labelcolor=TEXTO, fontsize=9)

        fig.tight_layout(pad=2)
        animales_txt = " y ".join(animales)
        titulo = (f"Distribución por Estado — {animales_txt}   "
                  f"({fecha_ini} → {fecha_fin})")
        return fig, titulo

    # ==========================================================================
    # HELPER: nombres de médicos
    # ==========================================================================
    def _nombres_medicos(self):
        try:
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
            return {
                str(nit): f"{d.get('nombre','').strip()} {d.get('apellido','').strip()}".strip()
                for nit, d in usuarios.items()
                if d.get("rol", "").lower() == "medico"
            }
        except Exception:
            return {}

    # ==========================================================================
    # EXPORTAR PNG
    # ==========================================================================
    def exportar_png(self):
        if self._fig_actual is None:
            messagebox.showwarning("Sin gráfico",
                                   "Genera un gráfico antes de exportar.")
            return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("Todos los archivos", "*.*")],
            title="Guardar gráfico como PNG",
            initialfile="reporte_systemvet.png",
        )
        if ruta:
            try:
                self._fig_actual.savefig(ruta, dpi=180,
                                          bbox_inches="tight",
                                          facecolor=FONDO)
                messagebox.showinfo("Exportado",
                                    f"Gráfico guardado:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")