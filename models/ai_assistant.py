import openai
import json
from config import OPENAI_API_KEY

class AIAssistant:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.conversation_history = []
        
    def analyze_data_with_gpt(self, df, question):
        """Analiza datos usando ChatGPT"""
        # Preparar contexto de datos (serializable)
        try:
            dtypes_dict = {col: str(dtype) for col, dtype in df.dtypes.items()}
            missing_dict = {col: int(count) for col, count in df.isnull().sum().items()}
            
            data_summary = {
                'shape': [int(df.shape[0]), int(df.shape[1])],
                'columns': list(df.columns),
                'dtypes': dtypes_dict,
                'missing_values': missing_dict
            }
        except Exception as e:
            data_summary = {
                'shape': [int(df.shape[0]), int(df.shape[1])],
                'columns': list(df.columns),
                'error': f'Error preparando datos: {str(e)}'
            }
        
        system_prompt = f"""
        Eres un experto analista de datos con acceso a un dataset con las siguientes características:
        
        Forma del dataset: {data_summary['shape'][0]} filas, {data_summary['shape'][1]} columnas
        Columnas: {', '.join(data_summary['columns'])}
        
        Proporciona análisis detallados, insights y recomendaciones basadas en los datos.
        Responde en español de manera clara y profesional.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Guardar en historial (sin data_context para evitar errores)
            self.conversation_history.append({
                'question': question,
                'response': ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"Error conectando con ChatGPT: {str(e)}. Verifica tu API key en config.py"
    
    def get_ml_recommendations(self, df, ml_results):
        """Obtiene recomendaciones ML de ChatGPT"""
        # Simplificar ml_results
        simple_results = {}
        for model, metrics in ml_results.items():
            if isinstance(metrics, dict) and 'error' not in metrics:
                simple_results[model] = f"R² Score: {metrics.get('r2_score', 0):.3f}"
        
        context = f"""
        Resultados de modelos ML: {simple_results}
        Dataset: {df.shape[0]} filas, {df.shape[1]} columnas
        """
        
        question = "Basándote en estos resultados de machine learning, ¿qué recomendaciones darías para mejorar el modelo y qué insights puedes extraer?"
        
        return self.analyze_data_with_gpt(df, question)
    
    def generate_business_insights(self, df):
        """Genera insights de negocio usando ChatGPT"""
        question = """
        Analiza este dataset desde una perspectiva de negocio:
        1. ¿Qué patrones importantes observas?
        2. ¿Qué oportunidades de optimización identificas?
        3. ¿Qué riesgos o problemas potenciales detectas?
        4. ¿Qué métricas KPI recomendarías monitorear?
        5. ¿Qué acciones estratégicas sugieres?
        """
        
        return self.analyze_data_with_gpt(df, question)
    
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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un consultor de datos que explica análisis técnicos de manera simple y práctica."},
                    {"role": "user", "content": question}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error explicando resultados: {str(e)}"
    
    def get_conversation_history(self):
        """Retorna historial de conversación"""
        return self.conversation_history
    
    def clear_history(self):
        """Limpia historial de conversación"""
        self.conversation_history = []