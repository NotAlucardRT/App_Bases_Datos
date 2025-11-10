#!/usr/bin/env python3
"""
Advanced Data Analyzer Pro - Aplicación mejorada con IA
Autor: Sistema de Análisis Avanzado
Versión: 2.0
"""

import sys
import os

# Agregar paths necesarios
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'sklearn', 'customtkinter',
        'xgboost', 'lightgbm', 'openai', 'reportlab', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    # Verificar Gemini por separado
    try:
        import google.generativeai
    except ImportError:
        missing_packages.append('google-generativeai')
    
    if missing_packages:
        print("Faltan las siguientes dependencias:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstala las dependencias con:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def setup_directories():
    """Crea directorios necesarios"""
    directories = ['data', 'exports', 'backups', 'models/saved']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Función principal"""
    print("Iniciando Advanced Data Analyzer Pro v2.0...")
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Crear directorios
    setup_directories()
    
    # Verificar configuración de IA
    from config import GEMINI_API_KEY, AI_CONFIG
    print(f"Usando IA: {AI_CONFIG['provider'].upper()}")
    if AI_CONFIG['provider'] == 'gemini':
        print("Gemini configurado - IA GRATUITA activada")
    else:
        print("Usando OpenAI - verifica tu API key")
    
    try:
        # Importar y ejecutar la aplicación
        from views.modern_ui import ModernDataAnalyzer
        
        print("Dependencias verificadas")
        print("Directorios creados")
        print("Iniciando interfaz...")
        
        app = ModernDataAnalyzer()
        app.run()
        
    except Exception as e:
        print(f"Error iniciando la aplicación: {e}")
        print("\nSoluciones posibles:")
        print("   1. Verifica que todas las dependencias estén instaladas")
        print("   2. Ejecuta: pip install -r requirements.txt")
        print("   3. Verifica tu configuración en config.py")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()