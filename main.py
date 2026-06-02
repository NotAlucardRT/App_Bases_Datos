#!/usr/bin/env python3
"""
Advanced Data Analyzer Pro v2.0 - Punto de entrada principal (MVC)

Arquitectura MVC implementada:
  Model      : models/ (database, ml_analyzer, ai_assistant, export_manager)
  View       : views/  (modern_ui)
  Controller : controllers/ (data_controller, ai_controller, export_controller)

Flujo de inicio:
  main.py -> verifica dependencias y directorios -> instancia la Vista
  La Vista instancia los Controladores
  Los Controladores instancian los Modelos
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def check_dependencies():
    """Verifica que las dependencias criticas esten instaladas."""
    required = [
        'pandas', 'numpy', 'matplotlib', 'sklearn',
        'customtkinter', 'joblib', 'reportlab', 'openpyxl'
    ]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    # Verificar Gemini por separado
    try:
        import google.generativeai
    except ImportError:
        missing.append('google-generativeai')

    if missing:
        print("Faltan las siguientes dependencias:")
        for pkg in missing:
            print("   - {}".format(pkg))
        print("\nInstalalas con:")
        print("   pip install -r requirements.txt")
        return False

    return True


def setup_directories():
    """Crea los directorios necesarios para la aplicacion."""
    for directory in ['data', 'exports', 'backups', 'models/saved', 'controllers']:
        os.makedirs(directory, exist_ok=True)


def main():
    """Funcion principal: verifica entorno e inicia la Vista."""
    print("Iniciando Advanced Data Analyzer Pro v2.0...")
    print("Arquitectura: MVC (Model-View-Controller)")

    if not check_dependencies():
        return

    setup_directories()

    from config import AI_CONFIG
    print("Proveedor IA: {}".format(AI_CONFIG['provider'].upper()))

    try:
        # La Vista es el unico componente que main.py instancia directamente.
        # La Vista a su vez instancia los Controladores, y estos los Modelos.
        from views.modern_ui import ModernDataAnalyzer

        print("Dependencias OK")
        print("Directorios OK")
        print("Iniciando interfaz MVC...")

        app = ModernDataAnalyzer()
        app.run()

    except Exception as e:
        print("Error iniciando la aplicacion: {}".format(e))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
 