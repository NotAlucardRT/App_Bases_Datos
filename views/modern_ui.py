"""
Vista Principal - Capa de Presentacion (MVC)

Esta clase SOLO se encarga de construir y actualizar la interfaz grafica.
NO contiene logica de negocio ni accede directamente a modelos.
Toda operacion de datos, ML, IA o exportacion se delega a los controladores:
  - DataController   : carga de archivos, ML, backup de BD
  - AIController     : chat con IA, insights de negocio
  - ExportController : exportacion a CSV, Excel, JSON y PDF
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime
import sys
sys.path.append('..')

# Importar SOLO los controladores; nunca los modelos directamente
from controllers.data_controller import DataController
from controllers.ai_controller import AIController
from controllers.export_controller import ExportController


class ModernDataAnalyzer:
    """
    Vista principal de la aplicacion.
    MVC - Capa View: delega toda logica a los controladores.
    """

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Instanciar controladores (unico punto de contacto con la logica)
        self.data_ctrl = DataController()
        self.ai_ctrl = AIController(db_manager=self.data_ctrl.db)
        self.export_ctrl = ExportController(db_manager=self.data_ctrl.db)

        # Estado de la vista (solo datos que la UI necesita para renderizar)
        self.ml_results = None

        self.setup_ui()

    # ------------------------------------------------------------------
    # Construccion de la interfaz
    # ------------------------------------------------------------------

    def setup_ui(self):
        self.root = ctk.CTk()
        self.root.title("Advanced Data Analyzer Pro")
        self.root.geometry("1400x900")

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---- Encabezado ----
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header_frame,
            text="Advanced Data Analyzer Pro",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        quick_actions = ctk.CTkFrame(header_frame)
        quick_actions.pack(side="right", padx=20, pady=10)

        ctk.CTkButton(
            quick_actions, text="Backup BD",
            command=self._on_backup, width=110
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            quick_actions, text="Ver Estadisticas BD",
            command=self._show_db_stats, width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            quick_actions, text="Exportar",
            command=self._show_export_options, width=110
        ).pack(side="left", padx=5)

        # ---- Panel izquierdo ----
        left_panel = ctk.CTkFrame(main_frame, width=360)
        left_panel.pack(side="left", fill="y", padx=(10, 5), pady=10)
        left_panel.pack_propagate(False)

        self._build_data_section(left_panel)
        self._build_ml_section(left_panel)
        self._build_ai_section(left_panel)

        # ---- Panel derecho ----
        right_panel = ctk.CTkFrame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        self.notebook = ctk.CTkTabview(right_panel)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.notebook.add("Datos")
        self.notebook.add("Graficos")
        self.notebook.add("ML Results")

        self._build_tabs()

    def _build_data_section(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="Gestion de Datos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        ctk.CTkButton(
            frame, text="Cargar Archivo Excel",
            command=self._on_load_file
        ).pack(fill="x", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(frame, text="No hay datos cargados")
        self.status_label.pack(pady=5)

        self.progress = ctk.CTkProgressBar(frame)
        self.progress.pack(fill="x", padx=10, pady=5)
        self.progress.set(0)

    def _build_ml_section(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="Machine Learning",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        self.target_combo = ctk.CTkComboBox(
            frame, values=["Seleccionar columna target"]
        )
        self.target_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Analisis ML Completo",
            command=self._on_run_analysis
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Hacer Predicciones",
            command=self._on_make_predictions
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Guardar Modelo",
            command=self._on_save_model
        ).pack(fill="x", padx=10, pady=5)

    def _build_ai_section(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame,
            text=self.ai_ctrl.get_provider_info(),
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=8)

        self.ai_entry = ctk.CTkEntry(
            frame, placeholder_text="Pregunta sobre tus datos..."
        )
        self.ai_entry.pack(fill="x", padx=10, pady=5)
        self.ai_entry.bind("<Return>", self._on_ask_ai)

        btn_row = ctk.CTkFrame(frame)
        btn_row.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            btn_row, text="Preguntar",
            command=self._on_ask_ai, width=100
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_row, text="Insights",
            command=self._on_get_insights, width=100
        ).pack(side="left", padx=2)

        self.ai_chat = ctk.CTkTextbox(frame, height=200)
        self.ai_chat.pack(fill="both", expand=True, padx=10, pady=10)

    def _build_tabs(self):
        self.data_tree_frame = ctk.CTkFrame(self.notebook.tab("Datos"))
        self.data_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.charts_frame = ctk.CTkFrame(self.notebook.tab("Graficos"))
        self.charts_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.ml_results_frame = ctk.CTkScrollableFrame(self.notebook.tab("ML Results"))
        self.ml_results_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ------------------------------------------------------------------
    # Manejadores de eventos (on_*) — llaman a controladores
    # ------------------------------------------------------------------

    def _on_load_file(self):
        """El usuario solicita cargar un archivo; la Vista pide la ruta y
        delega la carga al DataController."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.status_label.configure(text="Cargando archivo...")

        self.data_ctrl.load_file(
            file_path,
            on_progress=self._update_progress,
            on_success=self._on_file_loaded,
            on_error=lambda e: self._show_error("Error cargando archivo", e)
        )

    def _on_file_loaded(self, df, dataset_id, columns):
        """Callback invocado por DataController cuando la carga termina con exito."""
        name = self.data_ctrl.current_dataset_name
        self.status_label.configure(
            text="{} - {} filas, {} columnas".format(name, df.shape[0], df.shape[1])
        )

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.target_combo.configure(
            values=numeric_cols if numeric_cols else ["No hay columnas numericas"]
        )

        self._show_data_preview(df)
        self._create_auto_charts(df)
        self._log("Dataset cargado: {} filas, {} columnas".format(df.shape[0], df.shape[1]))
        self.progress.set(0)

    def _on_run_analysis(self):
        """El usuario solicita ejecutar ML; la Vista valida la seleccion
        y delega al DataController."""
        if not self.data_ctrl.has_data:
            messagebox.showwarning("Advertencia", "Carga un dataset primero")
            return

        target_col = self.target_combo.get()
        if target_col in ("Seleccionar columna target", "No hay columnas numericas", ""):
            messagebox.showwarning("Advertencia", "Selecciona una columna target valida")
            return

        self._log("Iniciando analisis ML...")

        self.data_ctrl.run_analysis(
            target_col,
            on_progress=self._update_progress,
            on_success=self._on_analysis_done,
            on_error=lambda e: self._show_error("Error en analisis ML", e)
        )

    def _on_analysis_done(self, results, best_algorithm):
        """Callback del DataController cuando el analisis ML termina."""
        self.ml_results = results
        self._show_ml_results(results)
        self._log("Analisis completado. Mejor modelo: {}".format(best_algorithm))
        self.progress.set(0)

        # Pedir recomendaciones IA automaticamente
        self.ai_ctrl.get_ml_recommendations(
            self.data_ctrl.current_df,
            results,
            dataset_id=self.data_ctrl.current_dataset_id,
            on_success=lambda r: self._log("Recomendaciones IA:\n{}".format(r)),
            on_error=lambda e: self._log("No se pudieron generar recomendaciones: {}".format(e))
        )

    def _on_make_predictions(self):
        """El usuario solicita predicciones; la Vista muestra opciones."""
        if not self.data_ctrl.has_trained_model:
            messagebox.showwarning("Advertencia", "Entrena un modelo primero")
            return

        win = ctk.CTkToplevel(self.root)
        win.title("Opciones de Prediccion")
        win.geometry("400x200")

        ctk.CTkLabel(
            win, text="Tipo de prediccion:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)

        ctk.CTkButton(
            win, text="Predecir Dataset Actual",
            command=lambda: self._predict_current(win)
        ).pack(pady=10)

        ctk.CTkButton(
            win, text="Predecir Nuevo Archivo",
            command=lambda: self._predict_new_file(win)
        ).pack(pady=10)

    def _predict_current(self, window):
        window.destroy()
        self.data_ctrl.make_predictions(
            on_success=self._on_predictions_ready,
            on_error=lambda e: self._log("Error en predicciones: {}".format(e))
        )

    def _on_predictions_ready(self, predictions):
        self._log("Predicciones generadas: {} valores".format(len(predictions)))
        self._log(
            "Min: {:.2f} | Max: {:.2f} | Media: {:.2f}".format(
                predictions.min(), predictions.max(), predictions.mean()
            )
        )
        # Guardar via ExportController para que quede en export_log
        import pandas as pd
        df_pred = self.data_ctrl.current_df.copy()
        df_pred['Prediccion'] = predictions
        self.export_ctrl.export_excel(
            df_pred,
            dataset_id=self.data_ctrl.current_dataset_id,
            on_success=lambda p: self._log("Predicciones guardadas en: {}".format(p)),
            on_error=lambda e: self._log("Error guardando predicciones: {}".format(e))
        )

    def _predict_new_file(self, window):
        window.destroy()
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo para predicciones",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            import pandas as pd
            new_df = pd.read_csv(file_path) if file_path.endswith('.csv') \
                else pd.read_excel(file_path)
            target_col = self.target_combo.get()
            # Acceso via DataController (MVC)
            predictions = self.data_ctrl.ml_analyzer.predict(new_df, target_col)
            new_df['Prediccion'] = predictions
            out = file_path.replace('.xlsx', '_predicciones.xlsx').replace('.csv', '_predicciones.csv')
            if out.endswith('.csv'):
                new_df.to_csv(out, index=False)
            else:
                new_df.to_excel(out, index=False)
            self._log("Predicciones nuevo archivo guardadas en: {}".format(out))
        except Exception as e:
            self._log("Error procesando archivo: {}".format(str(e)))

    def _on_ask_ai(self, event=None):
        """El usuario envia una pregunta al chat IA."""
        question = self.ai_entry.get().strip()
        if not question:
            return
        if not self.data_ctrl.has_data:
            messagebox.showwarning("Advertencia", "Carga un dataset primero")
            return

        self.ai_entry.delete(0, 'end')
        self._log("Tu: {}".format(question))

        self.ai_ctrl.ask(
            question,
            self.data_ctrl.current_df,
            dataset_id=self.data_ctrl.current_dataset_id,
            on_success=lambda r: self._log("IA: {}".format(r)),
            on_error=lambda e: self._log("Error IA: {}".format(e))
        )

    def _on_get_insights(self):
        """El usuario solicita insights de negocio."""
        if not self.data_ctrl.has_data:
            messagebox.showwarning("Advertencia", "Carga un dataset primero")
            return

        self._log("Generando insights de negocio...")
        self.ai_ctrl.get_business_insights(
            self.data_ctrl.current_df,
            dataset_id=self.data_ctrl.current_dataset_id,
            on_success=lambda r: self._log("Insights:\n{}".format(r)),
            on_error=lambda e: self._log("Error generando insights: {}".format(e))
        )

    def _on_save_model(self):
        """El usuario guarda el modelo entrenado."""
        if not self.data_ctrl.has_trained_model:
            messagebox.showwarning("Advertencia", "No hay modelo entrenado para guardar")
            return

        path = "models/saved/modelo_{}.joblib".format(
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        self.data_ctrl.save_model(
            path,
            on_success=lambda p: (
                self._log("Modelo guardado: {}".format(p)),
                messagebox.showinfo("Exito", "Modelo guardado en: {}".format(p))
            ),
            on_error=lambda e: self._show_error("Error guardando modelo", e)
        )

    def _on_backup(self):
        """El usuario solicita un backup de la BD."""
        self.data_ctrl.backup_database(
            on_success=lambda p: (
                self._log("Backup creado: {}".format(p)),
                messagebox.showinfo("Exito", "Backup creado: {}".format(p))
            ),
            on_error=lambda e: self._show_error("Error en backup", e)
        )

    def _show_export_options(self):
        """Muestra ventana de opciones de exportacion."""
        if not self.data_ctrl.has_data:
            messagebox.showwarning("Advertencia", "Carga un dataset primero")
            return

        win = ctk.CTkToplevel(self.root)
        win.title("Opciones de Exportacion")
        win.geometry("420x380")

        ctk.CTkLabel(
            win, text="Exportar datos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=15)

        ctk.CTkButton(
            win, text="Exportar a CSV",
            command=lambda: self._do_export('csv', win)
        ).pack(pady=8)

        ctk.CTkButton(
            win, text="Exportar a Excel",
            command=lambda: self._do_export('excel', win)
        ).pack(pady=8)

        ctk.CTkButton(
            win, text="Exportar a JSON",
            command=lambda: self._do_export('json', win)
        ).pack(pady=8)

        ctk.CTkButton(
            win, text="Generar Reporte PDF",
            command=lambda: self._do_export('pdf', win)
        ).pack(pady=8)

        ctk.CTkButton(
            win, text="Cargar Modelo Guardado",
            command=lambda: self._load_model(win)
        ).pack(pady=8)

        ctk.CTkButton(
            win, text="Ver Historial de Exportaciones",
            command=self._show_export_history
        ).pack(pady=8)

    def _do_export(self, fmt, window):
        window.destroy()
        ds_id = self.data_ctrl.current_dataset_id
        df = self.data_ctrl.current_df

        def _ok(p):
            self._log("Exportado ({}) a: {}".format(fmt, p))
            messagebox.showinfo("Exito", "Archivo generado:\n{}".format(p))

        def _err(e):
            self._show_error("Error exportando", e)

        if fmt == 'csv':
            self.export_ctrl.export_csv(df, dataset_id=ds_id, on_success=_ok, on_error=_err)
        elif fmt == 'excel':
            self.export_ctrl.export_excel(df, dataset_id=ds_id, on_success=_ok, on_error=_err)
        elif fmt == 'json':
            self.export_ctrl.export_json(df, dataset_id=ds_id, on_success=_ok, on_error=_err)
        elif fmt == 'pdf':
            self.export_ctrl.generate_pdf_report(
                df, ml_results=self.ml_results,
                dataset_id=ds_id, on_success=_ok, on_error=_err
            )

    def _load_model(self, window):
        window.destroy()
        file_path = filedialog.askopenfilename(
            title="Seleccionar modelo guardado",
            filetypes=[("Joblib files", "*.joblib"), ("All files", "*.*")],
            initialdir="models/saved"
        )
        if file_path:
            self.data_ctrl.load_model(
                file_path,
                on_success=lambda p: (
                    self._log("Modelo cargado: {}".format(os.path.basename(p))),
                    messagebox.showinfo("Exito", "Modelo cargado correctamente")
                ),
                on_error=lambda e: self._show_error("Error cargando modelo", e)
            )

    def _show_db_stats(self):
        """Muestra estadisticas de la base de datos en una ventana."""
        stats = self.data_ctrl.get_database_stats()
        win = ctk.CTkToplevel(self.root)
        win.title("Estadisticas de la Base de Datos")
        win.geometry("380x300")

        ctk.CTkLabel(
            win, text="Base de Datos SQLite",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=15)

        labels = {
            'datasets': 'Datasets registrados',
            'analysis_results': 'Resultados de analisis ML',
            'chat_history': 'Mensajes de chat IA',
            'export_log': 'Exportaciones realizadas',
        }
        for key, label in labels.items():
            ctk.CTkLabel(
                win, text="{}: {}".format(label, stats.get(key, 0))
            ).pack(pady=6)

    def _show_export_history(self):
        """Muestra el historial de exportaciones desde la BD."""
        history = self.export_ctrl.get_export_history()

        win = ctk.CTkToplevel(self.root)
        win.title("Historial de Exportaciones")
        win.geometry("700x400")

        if history.empty:
            ctk.CTkLabel(win, text="No hay exportaciones registradas").pack(expand=True)
            return

        tree = ttk.Treeview(win, columns=('format', 'file', 'size_kb', 'date'), show='headings')
        tree.heading('format', text='Formato')
        tree.heading('file', text='Archivo')
        tree.heading('size_kb', text='KB')
        tree.heading('date', text='Fecha')
        tree.column('format', width=70)
        tree.column('file', width=300)
        tree.column('size_kb', width=70)
        tree.column('date', width=160)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for _, row in history.iterrows():
            tree.insert('', 'end', values=(
                row.get('format', ''),
                os.path.basename(str(row.get('file_path', ''))),
                "{:.1f}".format(row.get('file_size_kb', 0)),
                str(row.get('exported_at', ''))[:19]
            ))

    # ------------------------------------------------------------------
    # Metodos de renderizado de contenido
    # ------------------------------------------------------------------

    def _show_data_preview(self, df):
        for w in self.data_tree_frame.winfo_children():
            w.destroy()

        tree = ttk.Treeview(self.data_tree_frame)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        tree['columns'] = list(df.columns)
        tree['show'] = 'headings'

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, minwidth=80)

        for _, row in df.head(1000).iterrows():
            tree.insert('', 'end', values=list(row))

    def _create_auto_charts(self, df):
        for w in self.charts_frame.winfo_children():
            w.destroy()

        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns

            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.patch.set_facecolor('#2b2b2b')

            # Grafico 1: distribucion
            if len(numeric_cols) > 0:
                col = numeric_cols[0]
                data = df[col].dropna()
                if len(data) > 0:
                    n_bins = min(50, max(10, int(np.sqrt(len(data)))))
                    ax1.hist(data, bins=n_bins, color='#1f77b4', alpha=0.7, edgecolor='white')
                    ax1.axvline(data.mean(), color='red', linestyle='--',
                                label='Media: {:.2f}'.format(data.mean()))
                    ax1.legend()
                ax1.set_title('Distribucion: {}'.format(col), color='white', fontsize=12)
                ax1.set_xlabel(col, color='white')
                ax1.set_ylabel('Frecuencia', color='white')
            ax1.set_facecolor('#2b2b2b')
            ax1.tick_params(colors='white')

            # Grafico 2: valores faltantes
            missing = df.isnull().sum()
            missing_cols = missing[missing > 0].sort_values(ascending=False).head(10)
            if len(missing_cols) > 0:
                y_pos = range(len(missing_cols))
                ax2.barh(y_pos, missing_cols.values, color='#ff7f0e')
                ax2.set_yticks(list(y_pos))
                ax2.set_yticklabels(
                    [c[:15] + '...' if len(c) > 15 else c for c in missing_cols.index],
                    color='white'
                )
                ax2.set_title('Valores Faltantes', color='white', fontsize=12)
            else:
                ax2.text(0.5, 0.5, 'Sin valores faltantes',
                         ha='center', va='center', color='#00d4aa',
                         transform=ax2.transAxes, fontsize=12, weight='bold')
            ax2.set_facecolor('#2b2b2b')
            ax2.tick_params(colors='white')

            # Grafico 3: tipos de datos
            dtypes_clean = {}
            for dtype_str in df.dtypes.astype(str):
                if 'int' in dtype_str or 'float' in dtype_str:
                    key = 'Numerico'
                elif 'object' in dtype_str:
                    key = 'Texto'
                elif 'datetime' in dtype_str:
                    key = 'Fecha'
                else:
                    key = 'Otro'
                dtypes_clean[key] = dtypes_clean.get(key, 0) + 1

            if dtypes_clean:
                colors_pie = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                wedges, texts, autotexts = ax3.pie(
                    dtypes_clean.values(), labels=dtypes_clean.keys(),
                    autopct='%1.1f%%', startangle=90,
                    colors=colors_pie[:len(dtypes_clean)]
                )
                for t in texts:
                    t.set_color('white')
                for at in autotexts:
                    at.set_color('white')
                    at.set_fontweight('bold')
            ax3.set_title('Tipos de Datos', color='white', fontsize=12)

            # Grafico 4: correlacion
            if len(numeric_cols) > 1:
                cols_use = numeric_cols[:10]
                corr = df[cols_use].corr().fillna(0)
                im = ax4.imshow(corr, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
                n = len(corr.columns)
                ax4.set_xticks(range(n))
                ax4.set_yticks(range(n))
                xlbls = [c[:8] + '..' if len(c) > 8 else c for c in corr.columns]
                ax4.set_xticklabels(xlbls, rotation=45, ha='right', color='white')
                ax4.set_yticklabels(xlbls, color='white')
                for i in range(n):
                    for j in range(n):
                        v = corr.iloc[i, j]
                        tc = 'white' if abs(v) > 0.5 else 'black'
                        ax4.text(j, i, '{:.2f}'.format(v),
                                 ha='center', va='center', color=tc, fontsize=8)
                plt.colorbar(im, ax=ax4, shrink=0.8).ax.tick_params(colors='white')
            else:
                ax4.text(0.5, 0.5, 'Se necesitan >= 2\ncolumnas numericas',
                         ha='center', va='center', color='white',
                         transform=ax4.transAxes, fontsize=12)
            ax4.set_facecolor('#2b2b2b')
            ax4.set_title('Matriz de Correlacion', color='white', fontsize=12)

            for ax in (ax1, ax2, ax3, ax4):
                ax.set_facecolor('#2b2b2b')
                for spine in ax.spines.values():
                    spine.set_color('white')
                    spine.set_linewidth(0.5)

            plt.tight_layout(pad=2.0)

            canvas = FigureCanvasTkAgg(fig, self.charts_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        except Exception as e:
            ctk.CTkLabel(
                self.charts_frame,
                text="Error creando graficos: {}".format(str(e))
            ).pack(expand=True)

    def _show_ml_results(self, results):
        for w in self.ml_results_frame.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.ml_results_frame, text="Resultados de Machine Learning",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        for algorithm, metrics in results.items():
            if 'error' not in metrics:
                frame = ctk.CTkFrame(self.ml_results_frame)
                frame.pack(fill="x", padx=20, pady=10)

                ctk.CTkLabel(
                    frame, text=algorithm,
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(pady=10)

                inner = ctk.CTkFrame(frame)
                inner.pack(fill="x", padx=20, pady=10)

                for metric, value in metrics.items():
                    ctk.CTkLabel(
                        inner, text="{}: {:.4f}".format(metric, value)
                    ).pack(anchor="w", padx=10, pady=2)

    # ------------------------------------------------------------------
    # Utilidades de la Vista
    # ------------------------------------------------------------------

    def _log(self, message):
        """Escribe un mensaje en el panel de chat/log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.ai_chat.insert("end", "[{}] {}\n\n".format(timestamp, message))
        self.ai_chat.see("end")

    def _update_progress(self, value):
        """Actualiza la barra de progreso (thread-safe via after)."""
        self.root.after(0, lambda: self.progress.set(value))

    def _show_error(self, title, message):
        """Muestra un messagebox de error."""
        messagebox.showerror(title, str(message))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernDataAnalyzer()
    app.run()
