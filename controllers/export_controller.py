"""
ExportController - Controlador de Exportaciones (MVC)

Responsabilidades:
  - Recibir solicitudes de exportacion desde la Vista
  - Delegar en el modelo ExportManager
  - Registrar cada exportacion en export_log (DatabaseManager)
  - Retornar resultados a la Vista mediante callbacks

La Vista NO importa ExportManager directamente.
"""

import threading
from models.export_manager import ExportManager
from models.database import DatabaseManager


class ExportController:
    """
    Controlador que orquesta todas las operaciones de exportacion.
    """

    def __init__(self, db_manager=None):
        self.export_manager = ExportManager()
        self.db = db_manager if db_manager else DatabaseManager()

    
    # Exportaciones
    

    def export_csv(self, df, dataset_id=None, on_success=None, on_error=None):
        """Exporta el DataFrame a CSV y registra en la BD."""
        def _export():
            try:
                filepath = self.export_manager.export_to_csv(df)
                self.db.log_export(filepath, 'csv', dataset_id)
                if on_success:
                    on_success(filepath)
            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_export, daemon=True).start()

    def export_excel(self, df, dataset_id=None, on_success=None, on_error=None):
        """Exporta el DataFrame a Excel y registra en la BD."""
        def _export():
            try:
                filepath = self.export_manager.export_to_excel(df)
                self.db.log_export(filepath, 'excel', dataset_id)
                if on_success:
                    on_success(filepath)
            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_export, daemon=True).start()

    def export_json(self, df, dataset_id=None, on_success=None, on_error=None):
        """Exporta el DataFrame a JSON y registra en la BD."""
        def _export():
            try:
                filepath = self.export_manager.export_to_json(df)
                self.db.log_export(filepath, 'json', dataset_id)
                if on_success:
                    on_success(filepath)
            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_export, daemon=True).start()

    def generate_pdf_report(self, df, ml_results=None, insights=None,
                            dataset_id=None, on_success=None, on_error=None):
        """Genera un reporte PDF completo y registra en la BD."""
        def _export():
            try:
                filepath = self.export_manager.create_analysis_report(
                    df, ml_results, insights=insights
                )
                self.db.log_export(filepath, 'pdf', dataset_id)
                if on_success:
                    on_success(filepath)
            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_export, daemon=True).start()

    
    # Historial de exportaciones
    

    def get_export_history(self, limit=30):
        """Retorna el log de exportaciones desde la BD."""
        return self.db.get_export_log(limit=limit)
