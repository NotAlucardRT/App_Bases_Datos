"""
AIController - Controlador del Asistente de Inteligencia Artificial (MVC)

Responsabilidades:
  - Recibir preguntas desde la Vista
  - Delegar al modelo UnifiedAIAssistant
  - Persistir cada interaccion en chat_history (DatabaseManager)
  - Retornar la respuesta a la Vista mediante callbacks

La Vista NO importa ni instancia UnifiedAIAssistant directamente.
"""

import threading
from models.unified_ai_assistant import UnifiedAIAssistant
from models.database import DatabaseManager


class AIController:
    """
    Controlador que orquesta todas las interacciones con la IA.
    Actua como intermediario entre la Vista y los modelos de IA y BD.
    """

    def __init__(self, db_manager=None):
        self.ai = UnifiedAIAssistant()
        # Reutiliza el DatabaseManager si ya fue creado por DataController
        self.db = db_manager if db_manager else DatabaseManager()

    
    # Chat con la IA
    

    def ask(self, question, df, dataset_id=None, on_success=None, on_error=None):
        """
        Envia una pregunta al asistente IA en un hilo separado.
        Persiste la interaccion en la BD al recibir respuesta.

        Parametros:
            question   : texto de la pregunta del usuario
            df         : DataFrame actual (contexto para la IA)
            dataset_id : ID del dataset activo (para asociar en BD)
            on_success : callback(respuesta_str)
            on_error   : callback(error_str)
        """
        def _ask():
            try:
                response = self.ai.analyze_data_with_gpt(df, question)

                # Persistir en historial
                self.db.save_chat_message(
                    question=question,
                    response=response,
                    dataset_id=dataset_id,
                    provider=self.ai.provider
                )

                if on_success:
                    on_success(response)

            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_ask, daemon=True).start()

    def get_ml_recommendations(self, df, ml_results, dataset_id=None,
                               on_success=None, on_error=None):
        """
        Solicita recomendaciones ML a la IA y persiste la interaccion.
        """
        def _recs():
            try:
                response = self.ai.get_ml_recommendations(df, ml_results)

                self.db.save_chat_message(
                    question="[Recomendaciones ML automaticas]",
                    response=response,
                    dataset_id=dataset_id,
                    provider=self.ai.provider
                )

                if on_success:
                    on_success(response)

            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_recs, daemon=True).start()

    def get_business_insights(self, df, dataset_id=None,
                              on_success=None, on_error=None):
        """
        Genera insights de negocio y persiste la interaccion.
        """
        def _insights():
            try:
                response = self.ai.generate_business_insights(df)

                self.db.save_chat_message(
                    question="[Insights de negocio automaticos]",
                    response=response,
                    dataset_id=dataset_id,
                    provider=self.ai.provider
                )

                if on_success:
                    on_success(response)

            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_insights, daemon=True).start()

    def explain_results(self, analysis_type, results,
                        on_success=None, on_error=None):
        """Solicita explicacion de resultados en lenguaje natural."""
        def _explain():
            try:
                response = self.ai.explain_analysis_results(analysis_type, results)
                if on_success:
                    on_success(response)
            except Exception as e:
                if on_error:
                    on_error(str(e))

        threading.Thread(target=_explain, daemon=True).start()

    
    # Historial
    

    def get_chat_history_from_db(self, dataset_id=None, limit=50):
        """Retorna el historial persistido en la BD."""
        return self.db.get_chat_history(dataset_id=dataset_id, limit=limit)

    def clear_history(self, dataset_id=None):
        """Limpia el historial en memoria y en BD."""
        self.ai.clear_history()
        self.db.clear_chat_history(dataset_id=dataset_id)


    # Info del proveedor

    def get_provider_info(self):
        """Retorna el proveedor IA activo como cadena legible."""
        return self.ai.get_provider_info()
