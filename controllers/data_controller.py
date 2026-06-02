"""
DataController - Controlador de Datos y Machine Learning (MVC)

Responsabilidades:
  - Coordinar la carga de archivos Excel con el modelo MLAnalyzer
  - Orquestar el entrenamiento y prediccion de modelos
  - Persistir datasets y resultados en DatabaseManager
  - Notificar a la Vista mediante callbacks (on_progress, on_result, on_error)

La Vista NUNCA accede directamente a MLAnalyzer ni a DatabaseManager;
siempre pasa por este controlador.
"""

import os
import threading
import pandas as pd
from models.database import DatabaseManager
from models.ml_analyzer import MLAnalyzer


class DataController:
    """
    Controlador central para operaciones de datos y ML.
    Recibe eventos de la Vista, ejecuta la logica en modelos
    y devuelve resultados mediante callbacks.
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.ml_analyzer = MLAnalyzer()
        self.current_df = None
        self.current_dataset_id = None
        self.current_dataset_name = None

    
    # Carga de archivos
    

    def load_file(self, file_path, on_progress=None, on_success=None, on_error=None):
        """
        Carga un archivo Excel en un hilo separado para no bloquear la UI.
        Persiste el dataset en la base de datos al finalizar.

        Parametros:
            file_path   : ruta completa al archivo .xlsx / .xls
            on_progress : callback(float 0-1) para actualizar barra de progreso
            on_success  : callback(df, dataset_id, columns) al terminar con exito
            on_error    : callback(str) si ocurre un error
        """
        def _load():
            try:
                if on_progress:
                    on_progress(0.2)

                df = pd.read_excel(file_path)

                if on_progress:
                    on_progress(0.6)

                name = os.path.basename(file_path)
                dataset_id = self.db.save_dataset(name, file_path, df)

                self.current_df = df
                self.current_dataset_id = dataset_id
                self.current_dataset_name = name

                if on_progress:
                    on_progress(1.0)

                if on_success:
                    on_success(df, dataset_id, list(df.columns))

            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_load, daemon=True).start()

    
    # Machine Learning
    

    def run_analysis(self, target_col, on_progress=None, on_success=None, on_error=None):
        """
        Entrena modelos ML en un hilo separado y persiste los resultados.

        Parametros:
            target_col  : nombre de la columna objetivo
            on_progress : callback(float)
            on_success  : callback(results_dict, best_algorithm)
            on_error    : callback(str)
        """
        if self.current_df is None:
            if on_error:
                on_error("No hay datos cargados. Carga un archivo Excel primero.")
            return

        def _analyze():
            try:
                if on_progress:
                    on_progress(0.1)

                results, best_algorithm = self.ml_analyzer.train_models(
                    self.current_df, target_col
                )

                if on_progress:
                    on_progress(0.8)

                # Persistir cada resultado en la BD
                if self.current_dataset_id:
                    for algorithm, metrics in results.items():
                        if 'error' not in metrics:
                            self.db.save_analysis_result(
                                self.current_dataset_id, algorithm, metrics
                            )

                if on_progress:
                    on_progress(1.0)

                if on_success:
                    on_success(results, best_algorithm)

            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_analyze, daemon=True).start()

    def make_predictions(self, on_success=None, on_error=None):
        """
        Realiza predicciones con el mejor modelo entrenado.

        Parametros:
            on_success : callback(predictions_array)
            on_error   : callback(str)
        """
        if self.current_df is None:
            if on_error:
                on_error("No hay datos cargados.")
            return

        try:
            predictions = self.ml_analyzer.predict(self.current_df)
            if on_success:
                on_success(predictions)
        except Exception as e:
            if on_error:
                on_error(str(e))

    def get_feature_importance(self):
        """Retorna la importancia de features del mejor modelo, o None."""
        return self.ml_analyzer.get_feature_importance()

    def save_model(self, path, on_success=None, on_error=None):
        """Guarda el modelo entrenado en disco."""
        try:
            self.ml_analyzer.save_model(path)
            if on_success:
                on_success(path)
        except Exception as e:
            if on_error:
                on_error(str(e))

    def load_model(self, path, on_success=None, on_error=None):
        """Carga un modelo previamente guardado desde disco."""
        try:
            self.ml_analyzer.load_model(path)
            if on_success:
                on_success(path)
        except Exception as e:
            if on_error:
                on_error(str(e))

    
    # Base de datos - consultas de la Vista
    

    def get_datasets(self):
        """Retorna el DataFrame de datasets almacenados."""
        return self.db.get_datasets()

    def get_analysis_results(self, dataset_id=None):
        """Retorna resultados ML almacenados."""
        return self.db.get_analysis_results(dataset_id)

    def get_database_stats(self):
        """Retorna estadisticas generales de la BD."""
        return self.db.get_database_stats()

    def backup_database(self, on_success=None, on_error=None):
        """Crea un backup de la base de datos."""
        try:
            path = self.db.backup_database()
            if on_success:
                on_success(path)
        except Exception as e:
            if on_error:
                on_error(str(e))

    
    # Propiedades de estado
    

    @property
    def has_data(self):
        return self.current_df is not None

    @property
    def has_trained_model(self):
        return self.ml_analyzer.best_model is not None

    @property
    def ml_results(self):
        return getattr(self.ml_analyzer, '_last_results', None)
