from config import AI_CONFIG, OPENAI_API_KEY, GEMINI_API_KEY

class UnifiedAIAssistant:
    def __init__(self):
        self.provider = AI_CONFIG['provider']
        self.assistant = None
        
        if self.provider == 'gemini':
            try:
                from models.gemini_assistant import GeminiAssistant
                self.assistant = GeminiAssistant()
            except ImportError:
                print("Gemini no disponible, usando OpenAI")
                self.provider = 'openai'
        
        if self.provider == 'openai' or self.assistant is None:
            try:
                from models.ai_assistant import AIAssistant
                self.assistant = AIAssistant()
            except ImportError:
                print("Error: No hay asistente IA disponible")
                self.assistant = None
    
    def analyze_data_with_gpt(self, df, question):
        """Análisis unificado que usa el proveedor configurado"""
        if self.assistant is None:
            return "Error: No hay asistente IA configurado"
        
        if self.provider == 'gemini':
            return self.assistant.analyze_data_with_gemini(df, question)
        else:
            return self.assistant.analyze_data_with_gpt(df, question)
    
    def get_ml_recommendations(self, df, ml_results):
        """Recomendaciones ML unificadas"""
        if self.assistant is None:
            return "Error: No hay asistente IA configurado"
        
        return self.assistant.get_ml_recommendations(df, ml_results)
    
    def generate_business_insights(self, df):
        """Insights de negocio unificados"""
        if self.assistant is None:
            return "Error: No hay asistente IA configurado"
        
        return self.assistant.generate_business_insights(df)
    
    def explain_analysis_results(self, analysis_type, results):
        """Explicación de resultados unificada"""
        if self.assistant is None:
            return "Error: No hay asistente IA configurado"
        
        return self.assistant.explain_analysis_results(analysis_type, results)
    
    def get_conversation_history(self):
        """Historial unificado"""
        if self.assistant is None:
            return []
        
        return self.assistant.get_conversation_history()
    
    def clear_history(self):
        """Limpiar historial unificado"""
        if self.assistant is not None:
            self.assistant.clear_history()
    
    def get_provider_info(self):
        """Información del proveedor actual"""
        if self.provider == 'gemini':
            return "🤖 Gemini Pro (Google) - GRATIS"
        elif self.provider == 'openai':
            return "🤖 ChatGPT (OpenAI) - De pago"
        else:
            return "❌ Sin IA configurada"