import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb
import joblib
from config import ML_CONFIG

class MLAnalyzer:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.encoders = {}
        self.best_model = None
        self.best_score = 0
        self._last_results = None  # Ultimo resultado de train_models
        
    def prepare_data(self, df, target_col=None):
        """Prepara datos para ML con feature engineering automático"""
        df_processed = df.copy()
        
        # Remover columnas no útiles
        cols_to_drop = []
        for col in df_processed.columns:
            if col == target_col:
                continue
            # Remover columnas con demasiados valores únicos (IDs)
            if df_processed[col].dtype == 'object' and df_processed[col].nunique() > len(df_processed) * 0.5:
                cols_to_drop.append(col)
            # Remover columnas con un solo valor
            elif df_processed[col].nunique() <= 1:
                cols_to_drop.append(col)
        
        df_processed = df_processed.drop(columns=cols_to_drop)
        
        # Detectar columnas numéricas y categóricas
        numeric_cols = df_processed.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Remover target de las listas si existe
        if target_col in numeric_cols:
            numeric_cols.remove(target_col)
        if target_col in categorical_cols:
            categorical_cols.remove(target_col)
        
        # Encoding categórico con manejo de errores
        for col in categorical_cols:
            try:
                if col not in self.encoders:
                    self.encoders[col] = LabelEncoder()
                    # Llenar valores nulos antes del encoding
                    df_processed[col] = df_processed[col].fillna('Unknown')
                    df_processed[col] = self.encoders[col].fit_transform(df_processed[col].astype(str))
                else:
                    df_processed[col] = df_processed[col].fillna('Unknown')
                    # Manejar valores no vistos durante entrenamiento
                    unique_vals = set(df_processed[col].astype(str))
                    known_vals = set(self.encoders[col].classes_)
                    new_vals = unique_vals - known_vals
                    
                    if new_vals:
                        # Asignar valores desconocidos a la primera clase
                        df_processed[col] = df_processed[col].astype(str)
                        for val in new_vals:
                            df_processed.loc[df_processed[col] == val, col] = self.encoders[col].classes_[0]
                    
                    df_processed[col] = self.encoders[col].transform(df_processed[col].astype(str))
            except Exception as e:
                print(f"Error procesando columna {col}: {e}")
                # Si falla, convertir a numérico simple
                df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
        
        # Llenar valores nulos
        df_processed = df_processed.fillna(0)
        
        return df_processed
    
    def train_models(self, df, target_col):
        """Entrena múltiples modelos ML"""
        print(f"Iniciando entrenamiento con target: {target_col}")
        
        if target_col not in df.columns:
            raise ValueError(f"Columna target '{target_col}' no encontrada")
        
        # Verificar que target sea numérico
        if not pd.api.types.is_numeric_dtype(df[target_col]):
            try:
                df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
            except:
                raise ValueError(f"No se puede convertir '{target_col}' a numérico")
        
        # Preparar datos
        df_clean = df.copy()
        
        # Limpiar target
        df_clean = df_clean.dropna(subset=[target_col])
        print(f"Filas después de limpiar target: {len(df_clean)}")
        
        if len(df_clean) < 5:
            raise ValueError("Muy pocas filas válidas para entrenamiento")
        
        # Preparar características
        X_cols = []
        for col in df_clean.columns:
            if col != target_col:
                if pd.api.types.is_numeric_dtype(df_clean[col]):
                    X_cols.append(col)
                elif df_clean[col].dtype == 'object' and df_clean[col].nunique() < 20:
                    # Encoding simple para categóricas
                    try:
                        df_clean[col] = pd.Categorical(df_clean[col]).codes
                        X_cols.append(col)
                    except:
                        pass
        
        print(f"Características seleccionadas: {X_cols}")
        
        if len(X_cols) == 0:
            raise ValueError("No hay características válidas para entrenamiento")
        
        X = df_clean[X_cols].fillna(0)
        y = df_clean[target_col]
        
        print(f"Forma final X: {X.shape}, y: {y.shape}")
        
        # Split simple
        test_size = min(0.3, max(0.1, len(X) * 0.2 / len(X)))
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        results = {}
        
        # Modelo simple: Random Forest
        try:
            print("Entrenando Random Forest...")
            rf = RandomForestRegressor(
                n_estimators=20, 
                max_depth=5,
                random_state=42,
                n_jobs=1
            )
            rf.fit(X_train, y_train)
            rf_pred = rf.predict(X_test)
            rf_score = r2_score(y_test, rf_pred)
            
            self.models['RandomForest'] = rf
            self.scaler = None  # No usar scaler para simplicidad
            
            results['RandomForest'] = {
                'r2_score': rf_score,
                'mae': mean_absolute_error(y_test, rf_pred),
                'cv_score': rf_score
            }
            print(f"Random Forest R²: {rf_score:.3f}")
            
        except Exception as e:
            print(f"Error Random Forest: {e}")
            results['RandomForest'] = {'error': str(e)}
        
        # Modelo de respaldo: Regresión lineal simple
        try:
            from sklearn.linear_model import LinearRegression
            print("Entrenando Regresión Lineal...")
            
            lr = LinearRegression()
            lr.fit(X_train, y_train)
            lr_pred = lr.predict(X_test)
            lr_score = r2_score(y_test, lr_pred)
            
            self.models['LinearRegression'] = lr
            
            results['LinearRegression'] = {
                'r2_score': lr_score,
                'mae': mean_absolute_error(y_test, lr_pred),
                'cv_score': lr_score
            }
            print(f"Regresión Lineal R²: {lr_score:.3f}")
            
        except Exception as e:
            print(f"Error Regresión Lineal: {e}")
            results['LinearRegression'] = {'error': str(e)}
        
        # Seleccionar mejor modelo
        valid_results = {k: v for k, v in results.items() if 'error' not in v}
        print(f"Modelos válidos: {list(valid_results.keys())}")
        
        if not valid_results:
            # Modelo dummy como último recurso
            from sklearn.dummy import DummyRegressor
            dummy = DummyRegressor(strategy='mean')
            dummy.fit(X_train, y_train)
            dummy_pred = dummy.predict(X_test)
            
            self.models['Dummy'] = dummy
            results['Dummy'] = {
                'r2_score': 0.0,
                'mae': mean_absolute_error(y_test, dummy_pred),
                'cv_score': 0.0
            }
            valid_results = {'Dummy': results['Dummy']}
        
        best_algorithm = max(valid_results.keys(), key=lambda k: results[k]['r2_score'])
        self.best_model = self.models[best_algorithm]
        self.best_score = results[best_algorithm]['r2_score']
        
        print(f"Mejor modelo: {best_algorithm} con R²: {self.best_score:.3f}")
        
        self._last_results = results  # Almacena para acceso del controlador
        return results, best_algorithm
    
    def predict(self, df, target_col=None):
        """Hace predicciones con el mejor modelo"""
        if self.best_model is None:
            raise ValueError("No hay modelo entrenado")
        
        # Preparar datos de la misma forma que en entrenamiento
        df_clean = df.copy()
        
        # Preparar características igual que en entrenamiento
        X_cols = []
        for col in df_clean.columns:
            if col != target_col:
                if pd.api.types.is_numeric_dtype(df_clean[col]):
                    X_cols.append(col)
                elif df_clean[col].dtype == 'object' and df_clean[col].nunique() < 20:
                    try:
                        df_clean[col] = pd.Categorical(df_clean[col]).codes
                        X_cols.append(col)
                    except:
                        pass
        
        X = df_clean[X_cols].fillna(0)
        
        return self.best_model.predict(X)
    
    def get_feature_importance(self):
        """Obtiene importancia de características"""
        if self.best_model is None:
            return None
        
        if hasattr(self.best_model, 'feature_importances_'):
            return self.best_model.feature_importances_
        return None
    
    def save_model(self, path):
        """Guarda el modelo entrenado"""
        model_data = {
            'models': self.models,
            'scaler': self.scaler,
            'encoders': self.encoders,
            'best_model': self.best_model,
            'best_score': self.best_score
        }
        joblib.dump(model_data, path)
    
    def load_model(self, path):
        """Carga modelo guardado"""
        model_data = joblib.load(path)
        self.models = model_data['models']
        self.scaler = model_data['scaler']
        self.encoders = model_data['encoders']
        self.best_model = model_data['best_model']
        self.best_score = model_data['best_score']