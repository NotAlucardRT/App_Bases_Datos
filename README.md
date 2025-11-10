# 🚀 Advanced Data Analyzer Pro v2.0

## Aplicación de Análisis de Datos con IA Avanzada

### ✨ Características Principales

#### 🤖 **IA Gratuita con Google Gemini**
- **Gemini 2.5 Flash** - Completamente GRATIS
- Chat inteligente para análisis de datos
- Generación automática de insights de negocio
- Recomendaciones ML personalizadas
- Explicaciones en lenguaje natural

#### 🔬 **Machine Learning Avanzado**
- **3 Algoritmos**: Random Forest, XGBoost, LightGBM
- **Feature engineering automático**
- **Validación cruzada** y métricas avanzadas
- **Comparación automática** de modelos
- **Predicciones** para nuevos datos

#### 💾 **Base de Datos Persistente**
- **SQLite integrado** para almacenamiento
- **Historial de análisis** guardado
- **Sistema de backup** automático
- **Gestión completa** de datasets

#### 📊 **Exportación Profesional**
- **Reportes PDF** con análisis completo
- **Múltiples formatos**: CSV, Excel, JSON
- **Gráficos en alta resolución**
- **Dashboard data** para web

#### 🎨 **Interfaz Moderna**
- **CustomTkinter** con tema oscuro
- **Gráficos automáticos** al cargar datos
- **Progress bars** para operaciones
- **Pestañas organizadas**

### 🛠️ Instalación Rápida

```bash
# 1. Clonar o descargar
cd App_Bases_Datos

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar aplicación
python main.py
```

### ⚙️ Configuración IA

#### Google Gemini (GRATIS - Recomendado)
1. Ve a: https://makersuite.google.com/app/apikey
2. Crea tu API key gratuita
3. Edita `config.py`:
```python
GEMINI_API_KEY = 'tu-api-key-aqui'
AI_CONFIG = {'provider': 'gemini'}
```

#### OpenAI ChatGPT (De pago)
```python
OPENAI_API_KEY = 'tu-openai-key'
AI_CONFIG = {'provider': 'openai'}
```

### 🚀 Uso Rápido

1. **Cargar datos**: Haz clic en "Cargar Archivo Excel"
2. **Seleccionar target**: Elige columna a predecir
3. **Análisis ML**: Clic en "Análisis ML Completo"
4. **Chat IA**: Pregunta sobre tus datos
5. **Exportar**: Genera reportes profesionales

### 📋 Funcionalidades Completas

#### 🔍 **Análisis Automático**
- ✅ Detección de tipos de datos
- ✅ Análisis de valores faltantes
- ✅ Correlaciones entre variables
- ✅ Detección de outliers
- ✅ Estadísticas descriptivas

#### 🤖 **Machine Learning**
- ✅ Entrenamiento automático de 3 modelos
- ✅ Selección del mejor algoritmo
- ✅ Métricas de evaluación completas
- ✅ Predicciones para nuevos datos
- ✅ Guardado/carga de modelos

#### 💬 **Asistente IA**
- ✅ Chat contextual sobre datos
- ✅ Insights de negocio automáticos
- ✅ Recomendaciones ML
- ✅ Explicaciones técnicas simples

#### 📊 **Visualización**
- ✅ Gráficos automáticos al cargar
- ✅ Distribuciones y histogramas
- ✅ Matriz de correlación
- ✅ Análisis de calidad de datos

#### 📤 **Exportación**
- ✅ Reportes PDF con gráficos
- ✅ Excel con formato profesional
- ✅ CSV para análisis externos
- ✅ JSON para APIs

### 🏗️ Arquitectura

```
App_Bases_Datos/
├── main.py                    # 🚀 Ejecutar aquí
├── config.py                  # ⚙️ Configuración
├── requirements.txt           # 📦 Dependencias
├── models/                    # 🧠 Lógica de negocio
│   ├── unified_ai_assistant.py # IA unificada
│   ├── gemini_assistant.py    # Gemini (GRATIS)
│   ├── ai_assistant.py        # ChatGPT
│   ├── ml_analyzer.py         # ML avanzado
│   ├── database.py            # Base de datos
│   └── export_manager.py      # Exportación
├── views/                     # 🎨 Interfaz
│   └── modern_ui.py           # UI moderna
├── data/                      # 💾 Datos guardados
├── exports/                   # 📊 Reportes
└── backups/                   # 🔄 Respaldos
```

### 🔧 Tecnologías

- **Frontend**: CustomTkinter (UI moderna)
- **Backend**: Python 3.8+
- **ML**: scikit-learn, XGBoost, LightGBM
- **IA**: Google Gemini (GRATIS) + OpenAI
- **Base de Datos**: SQLite
- **Visualización**: Matplotlib, Plotly
- **Exportación**: ReportLab, openpyxl

### 💡 Ejemplos de Uso

#### Análisis de Ventas
```
Dataset: ventas.xlsx
Target: ingresos
Resultado: Modelo R² = 0.94, predicciones precisas
IA: "Detecté estacionalidad en Q4, recomienda aumentar inventario"
```

#### Control de Calidad
```
Dataset: produccion.xlsx  
Target: defectos
Resultado: Identificación de factores críticos
IA: "Temperatura >80°C correlaciona con 65% más defectos"
```

### 🎯 Casos de Uso

- **📈 Análisis de Ventas**: Predicción de ingresos, tendencias
- **🏭 Control de Calidad**: Detección de anomalías
- **💰 Análisis Financiero**: Evaluación de riesgos
- **📊 Marketing**: Segmentación de clientes
- **⚙️ Operaciones**: Optimización de procesos

### 🆘 Solución de Problemas

#### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Error de IA
- Verifica API key en `config.py`
- Gemini es GRATIS: https://makersuite.google.com
- OpenAI requiere pago: https://platform.openai.com

#### Error de archivo
- Usa archivos Excel (.xlsx, .xls)
- Verifica que tenga datos válidos
- Mínimo 5 filas para ML

### 📊 Comparación IA

| Proveedor | Costo | Límites | Velocidad |
|-----------|-------|---------|-----------|
| **Gemini** | **GRATIS** | 15 req/min | Muy rápido |
| OpenAI | $0.002/1K tokens | Sin límite | Rápido |

### 🔮 Próximas Mejoras

- [ ] Dashboard web con Streamlit
- [ ] Análisis de series temporales
- [ ] Modelos de Deep Learning
- [ ] Integración con APIs externas
- [ ] Análisis de texto (NLP)

### 📄 Licencia

Código abierto para uso educativo y comercial.

---

**¡Analiza tus datos con IA de forma gratuita! 🚀📊🤖**

### 🚀 Inicio Rápido

```bash
git clone [repo]
cd App_Bases_Datos
pip install -r requirements.txt
python main.py
```

¡En 3 comandos tienes IA gratuita para análisis de datos! 🎉