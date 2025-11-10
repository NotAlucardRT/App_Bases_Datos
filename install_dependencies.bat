@echo off
echo Instalando Advanced Data Analyzer Pro v2.0...
echo.

echo [1/3] Actualizando pip...
pip install --upgrade pip

echo.
echo [2/3] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [3/3] Verificando instalacion...
python -c "import pandas, numpy, matplotlib, sklearn, customtkinter; print('Dependencias OK')"

echo.
echo ===== INSTALACION COMPLETADA =====
echo.
echo Para ejecutar: python main.py
echo.
echo IA GRATUITA: Configura Gemini API key en config.py
echo Gemini: https://makersuite.google.com/app/apikey
echo.
pause