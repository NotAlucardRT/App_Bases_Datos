import google.generativeai as genai
import json
from config import GEMINI_API_KEY, AI_CONFIG

class GeminiAssistant:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        # Usar modelo disponible
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except:
            try:
                self.model = genai.GenerativeModel('gemini-flash-latest')
            except:
                # Fallback a modelo básico
                self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.conversation_history = []
        
    def analyze_data_with_gemini(self, df, question):
        """Analiza datos usando Gemini"""
        # Preparar contexto de datos
        try:
            data_summary = {
                'shape': [int(df.shape[0]), int(df.shape[1])],
                'columns': list(df.columns),
                'missing_values': {col: int(count) for col, count in df.isnull().sum().items()},
                'sample_size': min(len(df), 1000)
            }
        except Exception as e:
            data_summary = {
                'shape': [int(df.shape[0]), int(df.shape[1])],
                'columns': list(df.columns),
                'error': f'Error preparando datos: {str(e)}'
            }
        
        system_prompt = f"""
        Eres un experto analista de datos. Tienes acceso a un dataset con:
        
        - Filas: {data_summary['shape'][0]}
        - Columnas: {data_summary['shape'][1]}
        - Columnas disponibles: {', '.join(data_summary['columns'][:10])}
        
        Proporciona análisis detallados y recomendaciones en español.
        Sé claro, profesional y práctico en tus respuestas.
        """
        
        try:
            full_prompt = f"{system_prompt}\n\nPregunta del usuario: {question}"
            response = self.model.generate_content(full_prompt)
            
            ai_response = response.text
            
            # Guardar en historial
            self.conversation_history.append({
                'question': question,
                'response': ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"Error conectando con Gemini: {str(e)}. Verifica tu API key en config.py"
    
    def get_ml_recommendations(self, df, ml_results):
        """Obtiene recomendaciones ML de Gemini"""
        # Simplificar ml_results
        simple_results = {}
        for model, metrics in ml_results.items():
            if isinstance(metrics, dict) and 'error' not in metrics:
                simple_results[model] = f"R² Score: {metrics.get('r2_score', 0):.3f}"
        
        question = f"""
        Basándote en estos resultados de machine learning: {simple_results}
        Dataset: {df.shape[0]} filas, {df.shape[1]} columnas
        
        ¿Qué recomendaciones darías para mejorar el modelo y qué insights puedes extraer?
        """
        
        return self.analyze_data_with_gemini(df, question)
    
    def generate_business_insights(self, df):
        """Genera insights de negocio usando Gemini"""
        question = f"""
        Analiza este dataset desde una perspectiva de negocio:
        
        Datos del dataset:
        - Filas: {df.shape[0]}
        - Columnas: {df.shape[1]}
        - Columnas disponibles: {', '.join(df.columns[:10])}
        
        Preguntas:
        1. ¿Qué patrones importantes observas?
        2. ¿Qué oportunidades de optimización identificas?
        3. ¿Qué riesgos o problemas potenciales detectas?
        4. ¿Qué métricas KPI recomendarías monitorear?
        5. ¿Qué acciones estratégicas sugieres?
        """
        
        return self.analyze_data_with_gemini(df, question)
    
    def explain_analysis_results(self, analysis_type, results):
        """Explica resultados de análisis en términos simples"""
        # Simplificar results
        simple_results = str(results)[:500] if results else "Sin resultados"
        
        question = f"""
        Explica estos resultados de {analysis_type} en términos simples:
        
        Resultados: {simple_results}
        
        Incluye:
        - Qué significan estos números
        - Si son buenos o malos resultados
        - Qué acciones recomiendas tomar
        """
        
        try:
            response = self.model.generate_content(question)
            return response.text
            
        except Exception as e:
            return f"Error explicando resultados: {str(e)}"
    
    def get_conversation_history(self):
        """Retorna historial de conversación"""
        return self.conversation_history
    
    def clear_history(self):
        """Limpia historial de conversación"""
        self.conversation_history = []