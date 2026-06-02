# 🚀 Advanced Data Analyzer Pro v2.0

## Aplicación de Análisis de Datos con IA Avanzada

Aplicación de escritorio para análisis de datos, Machine Learning e Inteligencia Artificial, desarrollada en Python con arquitectura **MVC (Model-View-Controller)**.

---

## ¿Qué hace la aplicación?

Permite a cualquier usuario cargar un archivo Excel con datos de cualquier tipo (ventas, producción, finanzas, inventario, etc.) y automáticamente:

- Analizar estadísticamente los datos y visualizarlos en gráficos
- Entrenar modelos de Machine Learning para predicciones
- Consultar un asistente de Inteligencia Artificial (Google Gemini / OpenAI) en lenguaje natural
- Exportar resultados a CSV, Excel, JSON o reportes PDF
- Persistir todo el historial en una base de datos SQLite local

---

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
#### 1. Clonar o descargar
```bash
cd App_Bases_Datos
```

#### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 3. Configurar API Key (obligatorio para el asistente IA)

Abre `config.py` y configura tu clave:

```python
# Para Google Gemini (gratuito): https://aistudio.google.com/
GEMINI_API_KEY = "tu-api-key-aqui"

# Para OpenAI (de pago), alternativa:
OPENAI_API_KEY = "tu-api-key-aqui"
```

#### 4. Ejecutar aplicación
```bash
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

1. **Cargar datos**: Haz clic en "Cargar Archivo Excel" y selecciona tu archivo `.xlsx`
2. **Ver gráficos**: Se generan automáticamente al cargar
3. **Hacer Predicciones**: Clic en "Hacer Predicciones" tras entrenar
4. **Entrenar ML**: Selecciona la columna objetivo y clic en "Análisis ML Completo"
5. **Chat IA**: Pregunta sobre tus datos
6. **Exportar**: Genera reportes profesionales
7. **Ver BD**: Clic en "Ver Estadísticas BD" para ver los registros persistidos

---

### Base de datos

La aplicación crea automáticamente `data/app_database.db` (SQLite) con 4 tablas:

| Tabla | Contenido |
|---|---|
| `datasets` | Registro de cada archivo Excel cargado |
| `analysis_results` | Métricas de los modelos ML entrenados |
| `chat_history` | Historial completo de conversaciones con la IA |
| `export_log` | Registro de cada exportación realizada |

---

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

### Arquitectura del proyecto — MVC

```
App_Bases_Datos/
├── models/                      ← Capa Model: lógica de negocio y datos
│   ├── database.py              #   Persistencia SQLite (4 tablas)
│   ├── ml_analyzer.py           #   Entrenamiento y predicción ML
│   ├── unified_ai_assistant.py  #   Fachada del asistente IA
│   ├── gemini_assistant.py      #   Implementación con Google Gemini
│   ├── ai_assistant.py          #   Implementación con OpenAI
│   └── export_manager.py        #   Generación de archivos exportados
│
├── controllers/                 ← Capa Controller: coordinación
│   ├── data_controller.py       #   Coordina carga de datos y ML
│   ├── ai_controller.py         #   Coordina las interacciones con IA
│   └── export_controller.py     #   Coordina las exportaciones
│
├── views/                       ← Capa View: interfaz gráfica
│   └── modern_ui.py             #   UI en CustomTkinter
│
├── data/                        ← Base de datos SQLite
├── exports/                     ← Archivos exportados
├── backups/                     ← Copias de seguridad de la BD
├── config.py                    ← Configuración de API keys y rutas
├── main.py                      ← Punto de entrada
└── requirements.txt
```

### 🔧 Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.8+ | Lenguaje base |
| CustomTkinter | Interfaz gráfica de escritorio |
| SQLite 3 | Base de datos embebida |
| pandas | Manipulación y análisis de datos |
| scikit-learn | Algoritmos de Machine Learning |
| Matplotlib | Visualización de gráficos |
| Google Gemini | Asistente IA principal (gratuito) |
| OpenAI | Asistente IA alternativo |
| ReportLab | Generación de reportes PDF |

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

### Requisitos del sistema

- Python 3.8 o superior
- Windows / macOS / Linux
- Conexión a internet (solo para el asistente IA)
- API Key de Google Gemini (gratuita) u OpenAI