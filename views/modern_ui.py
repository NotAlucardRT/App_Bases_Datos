import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import os
from datetime import datetime
import sys
sys.path.append('..')
from models.database import DatabaseManager
from models.ml_analyzer import MLAnalyzer
from models.unified_ai_assistant import UnifiedAIAssistant
from models.export_manager import ExportManager

class ModernDataAnalyzer:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.db = DatabaseManager()
        self.ml_analyzer = MLAnalyzer()
        self.ai_assistant = UnifiedAIAssistant()
        self.export_manager = ExportManager()
        
        self.df = None
        self.current_dataset_id = None
        self.ml_results = None
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root = ctk.CTk()
        self.root.title("Advanced Data Analyzer Pro")
        self.root.geometry("1400x900")
        
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(header_frame, text="🚀 Advanced Data Analyzer Pro", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(side="left", padx=20, pady=15)
        
        quick_actions = ctk.CTkFrame(header_frame)
        quick_actions.pack(side="right", padx=20, pady=10)
        
        self.backup_btn = ctk.CTkButton(quick_actions, text="💾 Backup", 
                                       command=self.backup_database, width=100)
        self.backup_btn.pack(side="left", padx=5)
        
        self.export_btn = ctk.CTkButton(quick_actions, text="📊 Export", 
                                       command=self.show_export_options, width=100)
        self.export_btn.pack(side="left", padx=5)
        
        left_panel = ctk.CTkFrame(main_frame, width=350)
        left_panel.pack(side="left", fill="y", padx=(10, 5), pady=10)
        left_panel.pack_propagate(False)
        
        data_section = ctk.CTkFrame(left_panel)
        data_section.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(data_section, text="📁 Gestión de Datos", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.load_btn = ctk.CTkButton(data_section, text="Cargar Archivo Excel", 
                                     command=self.load_file_with_progress)
        self.load_btn.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(data_section, text="No hay datos cargados")
        self.status_label.pack(pady=5)
        
        self.progress = ctk.CTkProgressBar(data_section)
        self.progress.pack(fill="x", padx=10, pady=5)
        self.progress.set(0)
        
        ml_section = ctk.CTkFrame(left_panel)
        ml_section.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ml_section, text="🤖 Machine Learning", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.target_combo = ctk.CTkComboBox(ml_section, values=["Seleccionar columna target"])
        self.target_combo.pack(fill="x", padx=10, pady=5)
        
        self.analyze_btn = ctk.CTkButton(ml_section, text="🔬 Análisis ML Completo", 
                                        command=self.run_advanced_analysis)
        self.analyze_btn.pack(fill="x", padx=10, pady=5)
        
        self.predict_btn = ctk.CTkButton(ml_section, text="🎯 Hacer Predicciones", 
                                        command=self.make_predictions)
        self.predict_btn.pack(fill="x", padx=10, pady=5)
        
        # Botón para guardar modelo
        self.save_model_btn = ctk.CTkButton(ml_section, text="💾 Guardar Modelo", 
                                           command=self.save_trained_model)
        self.save_model_btn.pack(fill="x", padx=10, pady=5)
        
        ai_section = ctk.CTkFrame(left_panel)
        ai_section.pack(fill="both", expand=True, padx=10, pady=10)
        
        ai_label = ctk.CTkLabel(ai_section, text=f"🧠 {self.ai_assistant.get_provider_info()}", 
                               font=ctk.CTkFont(size=14, weight="bold"))
        ai_label.pack(pady=10)
        
        self.ai_entry = ctk.CTkEntry(ai_section, placeholder_text="Pregunta sobre tus datos...")
        self.ai_entry.pack(fill="x", padx=10, pady=5)
        self.ai_entry.bind("<Return>", self.ask_ai)
        
        ai_buttons = ctk.CTkFrame(ai_section)
        ai_buttons.pack(fill="x", padx=10, pady=5)
        
        self.ask_btn = ctk.CTkButton(ai_buttons, text="💬 Preguntar", 
                                    command=self.ask_ai, width=100)
        self.ask_btn.pack(side="left", padx=2)
        
        self.insights_btn = ctk.CTkButton(ai_buttons, text="💡 Insights", 
                                         command=self.get_business_insights, width=100)
        self.insights_btn.pack(side="left", padx=2)
        
        self.ai_chat = ctk.CTkTextbox(ai_section, height=200)
        self.ai_chat.pack(fill="both", expand=True, padx=10, pady=10)
        
        right_panel = ctk.CTkFrame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        self.notebook = ctk.CTkTabview(right_panel)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.notebook.add("📊 Datos")
        self.notebook.add("📈 Gráficos")
        self.notebook.add("🤖 ML Results")
        
        self.setup_tabs()
        
    def setup_tabs(self):
        data_tab = self.notebook.tab("📊 Datos")
        self.data_tree_frame = ctk.CTkFrame(data_tab)
        self.data_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        charts_tab = self.notebook.tab("📈 Gráficos")
        self.charts_frame = ctk.CTkFrame(charts_tab)
        self.charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ml_tab = self.notebook.tab("🤖 ML Results")
        self.ml_results_frame = ctk.CTkScrollableFrame(ml_tab)
        self.ml_results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def load_file_with_progress(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")]
        )
        
        if file_path:
            def load_in_thread():
                try:
                    self.progress.set(0.2)
                    self.status_label.configure(text="Cargando archivo...")
                    
                    self.df = pd.read_excel(file_path)
                    self.progress.set(0.6)
                    
                    filename = os.path.basename(file_path)
                    self.current_dataset_id = self.db.save_dataset(filename, file_path, self.df)
                    self.progress.set(0.8)
                    
                    self.update_ui_after_load()
                    self.progress.set(1.0)
                    
                    self.status_label.configure(text=f"✅ {filename} - {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
                    self.log_ai_message(f"📁 Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
                    
                except Exception as e:
                    self.status_label.configure(text=f"❌ Error: {str(e)}")
                    messagebox.showerror("Error", f"Error cargando archivo: {str(e)}")
                finally:
                    self.progress.set(0)
            
            threading.Thread(target=load_in_thread, daemon=True).start()
    
    def update_ui_after_load(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.target_combo.configure(values=numeric_cols if numeric_cols else ["No hay columnas numéricas"])
        
        self.show_data_preview()
        self.create_auto_charts()
    
    def show_data_preview(self):
        for widget in self.data_tree_frame.winfo_children():
            widget.destroy()
        
        tree = ttk.Treeview(self.data_tree_frame)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree['columns'] = list(self.df.columns)
        tree['show'] = 'headings'
        
        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, minwidth=80)
        
        for idx, row in self.df.head(1000).iterrows():
            tree.insert('', 'end', values=list(row))
    
    def create_auto_charts(self):
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
        
        if self.df is None:
            return
        
        try:
            # Configurar matplotlib para threading
            import matplotlib
            matplotlib.use('TkAgg')
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.patch.set_facecolor('#2b2b2b')
            
            # Gráfico 1: Distribución de primera columna numérica
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                col = numeric_cols[0]
                data = self.df[col].dropna()
                if len(data) > 0:
                    # Calcular bins apropiados
                    n_bins = min(50, max(10, int(np.sqrt(len(data)))))
                    ax1.hist(data, bins=n_bins, color='#1f77b4', alpha=0.7, edgecolor='white')
                    ax1.set_title(f'Distribución: {col}', color='white', fontsize=12)
                    ax1.set_xlabel(col, color='white')
                    ax1.set_ylabel('Frecuencia', color='white')
                    
                    # Agregar estadísticas
                    mean_val = data.mean()
                    ax1.axvline(mean_val, color='red', linestyle='--', alpha=0.8, 
                               label=f'Media: {mean_val:.2f}')
                    ax1.legend()
                else:
                    ax1.text(0.5, 0.5, 'Sin datos válidos', ha='center', va='center', 
                            color='white', transform=ax1.transAxes)
                ax1.set_facecolor('#2b2b2b')
                ax1.tick_params(colors='white')
            else:
                ax1.text(0.5, 0.5, 'No hay columnas\nnuméricas', ha='center', va='center', 
                        color='white', transform=ax1.transAxes, fontsize=12)
                ax1.set_facecolor('#2b2b2b')
            
            # Gráfico 2: Valores faltantes (solo columnas con faltantes)
            missing = self.df.isnull().sum()
            missing_cols = missing[missing > 0].sort_values(ascending=False).head(10)
            
            if len(missing_cols) > 0:
                y_pos = range(len(missing_cols))
                ax2.barh(y_pos, missing_cols.values, color='#ff7f0e')
                ax2.set_yticks(y_pos)
                ax2.set_yticklabels([col[:15] + '...' if len(col) > 15 else col 
                                   for col in missing_cols.index], color='white')
                ax2.set_title('Valores Faltantes por Columna', color='white', fontsize=12)
                ax2.set_xlabel('Cantidad Faltante', color='white')
                
                # Agregar porcentajes
                total_rows = len(self.df)
                for i, (col, count) in enumerate(missing_cols.items()):
                    pct = (count / total_rows) * 100
                    ax2.text(count + max(missing_cols.values) * 0.01, i, f'{pct:.1f}%', 
                            va='center', color='white', fontsize=9)
            else:
                ax2.text(0.5, 0.5, '✓ Sin valores\nfaltantes', ha='center', va='center', 
                        color='#00d4aa', transform=ax2.transAxes, fontsize=12, weight='bold')
            
            ax2.set_facecolor('#2b2b2b')
            ax2.tick_params(colors='white')
            
            # Gráfico 3: Tipos de datos mejorado
            dtypes_clean = {}
            for dtype_str in self.df.dtypes.astype(str):
                if 'int' in dtype_str or 'float' in dtype_str:
                    key = 'Numérico'
                elif 'object' in dtype_str:
                    key = 'Texto/Categórico'
                elif 'datetime' in dtype_str:
                    key = 'Fecha/Hora'
                elif 'bool' in dtype_str:
                    key = 'Booleano'
                else:
                    key = 'Otro'
                dtypes_clean[key] = dtypes_clean.get(key, 0) + 1
            
            if dtypes_clean:
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                wedges, texts, autotexts = ax3.pie(dtypes_clean.values(), 
                                                  labels=dtypes_clean.keys(),
                                                  autopct='%1.1f%%', 
                                                  startangle=90,
                                                  colors=colors[:len(dtypes_clean)])
                ax3.set_title('Distribución de Tipos de Datos', color='white', fontsize=12)
                
                for text in texts:
                    text.set_color('white')
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            
            # Gráfico 4: Matriz de correlación mejorada
            if len(numeric_cols) > 1:
                # Limitar a máximo 10 columnas para legibilidad
                cols_to_use = numeric_cols[:10]
                corr_matrix = self.df[cols_to_use].corr()
                
                # Filtrar correlaciones válidas
                corr_matrix = corr_matrix.fillna(0)
                
                im = ax4.imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
                
                # Configurar ticks
                n_cols = len(corr_matrix.columns)
                ax4.set_xticks(range(n_cols))
                ax4.set_yticks(range(n_cols))
                
                # Labels truncados
                x_labels = [col[:8] + '...' if len(col) > 8 else col for col in corr_matrix.columns]
                y_labels = [col[:8] + '...' if len(col) > 8 else col for col in corr_matrix.columns]
                
                ax4.set_xticklabels(x_labels, rotation=45, ha='right', color='white')
                ax4.set_yticklabels(y_labels, color='white')
                ax4.set_title('Matriz de Correlación', color='white', fontsize=12)
                
                # Agregar valores de correlación en las celdas
                for i in range(n_cols):
                    for j in range(n_cols):
                        if not np.isnan(corr_matrix.iloc[i, j]):
                            text_color = 'white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black'
                            ax4.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                   ha='center', va='center', color=text_color, fontsize=8)
                
                # Colorbar
                cbar = plt.colorbar(im, ax=ax4, shrink=0.8)
                cbar.ax.tick_params(colors='white')
                cbar.set_label('Correlación', color='white')
            else:
                ax4.text(0.5, 0.5, 'Necesitas al menos\n2 columnas numéricas\npara correlación', 
                        ha='center', va='center', color='white', transform=ax4.transAxes, fontsize=12)
            
            ax4.set_facecolor('#2b2b2b')
            
            # Aplicar estilo a todos los ejes
            for ax in [ax1, ax2, ax3, ax4]:
                ax.set_facecolor('#2b2b2b')
                for spine in ax.spines.values():
                    spine.set_color('white')
                    spine.set_linewidth(0.5)
            
            plt.tight_layout(pad=2.0)
            
            # Limpiar figura anterior si existe
            plt.close('all')
            
            canvas = FigureCanvasTkAgg(fig, self.charts_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            print(f"Error detallado en gráficos: {e}")
            import traceback
            traceback.print_exc()
            error_label = ctk.CTkLabel(self.charts_frame, text=f"Error creando gráficos: {str(e)}")
            error_label.pack(expand=True)
    
    def run_advanced_analysis(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Carga un dataset primero")
            return
        
        target_col = self.target_combo.get()
        if target_col == "Seleccionar columna target" or not target_col:
            messagebox.showwarning("Advertencia", "Selecciona una columna target")
            return
        
        def analyze_in_thread():
            try:
                self.progress.set(0.3)
                self.log_ai_message("🔬 Iniciando análisis ML avanzado...")
                
                self.ml_results, best_algorithm = self.ml_analyzer.train_models(self.df, target_col)
                self.progress.set(0.7)
                
                for algorithm, metrics in self.ml_results.items():
                    if 'error' not in metrics:
                        self.db.save_analysis_result(
                            self.current_dataset_id, 
                            algorithm, 
                            metrics.get('r2_score', 0)
                        )
                
                self.show_ml_results()
                self.progress.set(1.0)
                
                self.log_ai_message(f"✅ Análisis completado. Mejor modelo: {best_algorithm}")
                
                try:
                    recommendations = self.ai_assistant.get_ml_recommendations(self.df, self.ml_results)
                    self.log_ai_message(f"🤖 Recomendaciones IA:\n{recommendations}")
                except Exception as ai_error:
                    self.log_ai_message(f"⚠️ No se pudieron generar recomendaciones IA: {str(ai_error)}")
                
            except Exception as e:
                self.log_ai_message(f"❌ Error en análisis: {str(e)}")
                print(f"Error detallado: {e}")
                import traceback
                traceback.print_exc()
            finally:
                self.progress.set(0)
        
        threading.Thread(target=analyze_in_thread, daemon=True).start()
    
    def make_predictions(self):
        if self.ml_analyzer.best_model is None:
            messagebox.showwarning("Advertencia", "Entrena un modelo primero")
            return
        
        # Ventana para elegir tipo de predicción
        pred_window = ctk.CTkToplevel(self.root)
        pred_window.title("Opciones de Predicción")
        pred_window.geometry("400x200")
        
        ctk.CTkLabel(pred_window, text="¿Qué tipo de predicción quieres?", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkButton(pred_window, text="📊 Predecir Dataset Actual", 
                     command=lambda: self.predict_current_data(pred_window)).pack(pady=10)
        
        ctk.CTkButton(pred_window, text="📁 Predecir Nuevo Archivo", 
                     command=lambda: self.predict_new_file(pred_window)).pack(pady=10)
    
    def predict_current_data(self, window):
        window.destroy()
        try:
            target_col = self.target_combo.get()
            predictions = self.ml_analyzer.predict(self.df, target_col)
            
            # Agregar predicciones al DataFrame
            df_with_pred = self.df.copy()
            df_with_pred['Prediccion'] = predictions
            
            self.log_ai_message(f"🎯 Predicciones generadas: {len(predictions)} valores")
            
            pred_stats = f"""📊 Estadísticas de Predicciones:
- Mínimo: {predictions.min():.2f}
- Máximo: {predictions.max():.2f}
- Media: {predictions.mean():.2f}
- Desviación estándar: {predictions.std():.2f}"""
            self.log_ai_message(pred_stats)
            
            # Exportar resultados
            filepath = self.export_manager.export_to_excel(df_with_pred, "predicciones_dataset.xlsx")
            self.log_ai_message(f"💾 Predicciones guardadas en: {filepath}")
            
        except Exception as e:
            self.log_ai_message(f"❌ Error en predicciones: {str(e)}")
    
    def predict_new_file(self, window):
        window.destroy()
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo para predicciones",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]
        )
        
        if file_path:
            try:
                # Cargar nuevo archivo
                if file_path.endswith('.csv'):
                    new_df = pd.read_csv(file_path)
                else:
                    new_df = pd.read_excel(file_path)
                
                target_col = self.target_combo.get()
                predictions = self.ml_analyzer.predict(new_df, target_col)
                
                # Agregar predicciones
                new_df['Prediccion'] = predictions
                
                # Guardar resultados
                output_path = file_path.replace('.xlsx', '_con_predicciones.xlsx').replace('.csv', '_con_predicciones.csv')
                if output_path.endswith('.csv'):
                    new_df.to_csv(output_path, index=False)
                else:
                    new_df.to_excel(output_path, index=False)
                
                self.log_ai_message(f"🎯 Predicciones para nuevo archivo completadas")
                self.log_ai_message(f"💾 Resultados guardados en: {output_path}")
                
                pred_stats = f"""📊 Estadísticas:
- Archivo: {os.path.basename(file_path)}
- Filas procesadas: {len(predictions)}
- Predicción promedio: {predictions.mean():.2f}"""
                self.log_ai_message(pred_stats)
                
            except Exception as e:
                self.log_ai_message(f"❌ Error procesando archivo: {str(e)}")
    
    def show_ml_results(self):
        for widget in self.ml_results_frame.winfo_children():
            widget.destroy()
        
        if not self.ml_results:
            return
        
        title = ctk.CTkLabel(self.ml_results_frame, text="🤖 Resultados de Machine Learning", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)
        
        for algorithm, metrics in self.ml_results.items():
            if 'error' not in metrics:
                algo_frame = ctk.CTkFrame(self.ml_results_frame)
                algo_frame.pack(fill="x", padx=20, pady=10)
                
                algo_label = ctk.CTkLabel(algo_frame, text=f"📊 {algorithm}", 
                                         font=ctk.CTkFont(size=16, weight="bold"))
                algo_label.pack(pady=10)
                
                metrics_frame = ctk.CTkFrame(algo_frame)
                metrics_frame.pack(fill="x", padx=20, pady=10)
                
                for metric, value in metrics.items():
                    metric_label = ctk.CTkLabel(metrics_frame, text=f"{metric}: {value:.4f}")
                    metric_label.pack(anchor="w", padx=10, pady=2)
    
    def ask_ai(self, event=None):
        question = self.ai_entry.get().strip()
        if not question or self.df is None:
            return
        
        self.ai_entry.delete(0, 'end')
        self.log_ai_message(f"👤 Tú: {question}")
        
        def ask_in_thread():
            try:
                response = self.ai_assistant.analyze_data_with_gpt(self.df, question)
                provider = 'Gemini' if self.ai_assistant.provider == 'gemini' else 'ChatGPT'
                self.log_ai_message(f"🤖 {provider}: {response}")
            except Exception as e:
                self.log_ai_message(f"❌ Error: {str(e)}")
        
        threading.Thread(target=ask_in_thread, daemon=True).start()
    
    def get_business_insights(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Carga un dataset primero")
            return
        
        def insights_in_thread():
            try:
                self.log_ai_message("🔍 Generando insights de negocio...")
                insights = self.ai_assistant.generate_business_insights(self.df)
                self.log_ai_message(f"💡 Insights de Negocio:\n{insights}")
            except Exception as e:
                self.log_ai_message(f"❌ Error generando insights: {str(e)}")
        
        threading.Thread(target=insights_in_thread, daemon=True).start()
    
    def log_ai_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.ai_chat.insert("end", f"[{timestamp}] {message}\n\n")
        self.ai_chat.see("end")
    
    def show_export_options(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Carga un dataset primero")
            return
        
        export_window = ctk.CTkToplevel(self.root)
        export_window.title("Opciones de Exportación")
        export_window.geometry("400x300")
        
        ctk.CTkButton(export_window, text="📄 Exportar a CSV", 
                     command=lambda: self.export_data('csv')).pack(pady=10)
        
        ctk.CTkButton(export_window, text="📊 Exportar a Excel", 
                     command=lambda: self.export_data('excel')).pack(pady=10)
        
        ctk.CTkButton(export_window, text="📋 Generar Reporte PDF", 
                     command=self.generate_pdf_report).pack(pady=10)
        
        ctk.CTkButton(export_window, text="💾 Cargar Modelo Guardado", 
                     command=self.load_saved_model).pack(pady=10)
    
    def export_data(self, format_type):
        try:
            if format_type == 'csv':
                filepath = self.export_manager.export_to_csv(self.df)
            elif format_type == 'excel':
                filepath = self.export_manager.export_to_excel(self.df, "datos_exportados.xlsx")
            
            self.log_ai_message(f"✅ Datos exportados: {filepath}")
            messagebox.showinfo("Éxito", f"Datos exportados a: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando: {str(e)}")
    
    def generate_pdf_report(self):
        try:
            insights = self.ai_assistant.generate_business_insights(self.df)
            
            filepath = self.export_manager.create_analysis_report(
                self.df, self.ml_results, insights=insights
            )
            
            self.log_ai_message(f"📋 Reporte PDF generado: {filepath}")
            messagebox.showinfo("Éxito", f"Reporte generado: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generando reporte: {str(e)}")
    
    def save_trained_model(self):
        if self.ml_analyzer.best_model is None:
            messagebox.showwarning("Advertencia", "No hay modelo entrenado para guardar")
            return
        
        try:
            model_path = f"models/saved/modelo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.joblib"
            self.ml_analyzer.save_model(model_path)
            self.log_ai_message(f"💾 Modelo guardado: {model_path}")
            messagebox.showinfo("Éxito", f"Modelo guardado en: {model_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error guardando modelo: {str(e)}")
    
    def backup_database(self):
        try:
            backup_path = self.db.backup_database()
            self.log_ai_message(f"💾 Backup creado: {backup_path}")
            messagebox.showinfo("Éxito", f"Backup creado: {backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error creando backup: {str(e)}")
    
    def load_saved_model(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar modelo guardado",
            filetypes=[("Joblib files", "*.joblib"), ("All files", "*.*")],
            initialdir="models/saved"
        )
        
        if file_path:
            try:
                self.ml_analyzer.load_model(file_path)
                self.log_ai_message(f"💾 Modelo cargado: {os.path.basename(file_path)}")
                messagebox.showinfo("Éxito", "Modelo cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error cargando modelo: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernDataAnalyzer()
    app.run()