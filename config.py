# Configuración de la aplicación
import os

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'tu-openai-api-key-aqui')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCjt3eI8XHaURS2E2pZY6jCIiqMiyVGzGM')

# Configuración de IA
AI_CONFIG = {
    'provider': 'gemini',  # 'openai' o 'gemini'
    'model': 'gemini-2.5-flash'  # Modelo disponible y gratuito
}

# Base de datos
DATABASE_CONFIG = {
    'type': 'sqlite',
    'path': 'data/app_database.db'
}

# Configuración de ML
ML_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'cv_folds': 5,
    'algorithms': ['RandomForest', 'XGBoost', 'LightGBM']
}

# UI Config
UI_CONFIG = {
    'theme': 'dark',
    'colors': {
        'primary': '#00d4aa',
        'secondary': '#ff6b35',
        'background': '#1e1e1e',
        'surface': '#2d2d2d',
        'text': '#ffffff'
    }
}

# Exportación
EXPORT_CONFIG = {
    'formats': ['csv', 'excel', 'json', 'pdf'],
    'output_dir': 'exports'
}