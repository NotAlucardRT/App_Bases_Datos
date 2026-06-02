"""
Modelo de Base de Datos - Capa de Persistencia (MVC)
Gestiona todas las operaciones con SQLite: datasets, análisis, chat y exportaciones.
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime
from config import DATABASE_CONFIG


class DatabaseManager:
    """
    Clase responsable de toda la persistencia en SQLite.
    En la arquitectura MVC, pertenece a la capa Model.
    Expone métodos CRUD para que los controladores los consuman.
    """

    def __init__(self):
        self.db_path = DATABASE_CONFIG['path']
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()

    # ------------------------------------------------------------------
    # Inicialización del esquema
    # ------------------------------------------------------------------

    def init_database(self):
        """Crea todas las tablas si no existen."""
        with sqlite3.connect(self.db_path) as conn:

            # Tabla 1: Datasets cargados
            conn.execute('''
                CREATE TABLE IF NOT EXISTS datasets (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT    NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_path   TEXT,
                    rows        INTEGER,
                    columns     INTEGER
                )
            ''')

            # Tabla 2: Resultados de análisis ML
            conn.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id  INTEGER NOT NULL,
                    algorithm   TEXT,
                    r2_score    REAL,
                    mae         REAL,
                    cv_score    REAL,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
                )
            ''')

            # Tabla 3: Historial de conversaciones con la IA
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id  INTEGER,
                    provider    TEXT,
                    question    TEXT    NOT NULL,
                    response    TEXT    NOT NULL,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE SET NULL
                )
            ''')

            # Tabla 4: Registro de exportaciones realizadas
            conn.execute('''
                CREATE TABLE IF NOT EXISTS export_log (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    dataset_id   INTEGER,
                    format       TEXT    NOT NULL,
                    file_path    TEXT    NOT NULL,
                    file_size_kb REAL,
                    exported_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE SET NULL
                )
            ''')

            conn.commit()

    # ------------------------------------------------------------------
    # CRUD - Datasets
    # ------------------------------------------------------------------

    def save_dataset(self, name, file_path, df):
        """Registra un dataset recien cargado. Retorna el ID generado."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO datasets (name, file_path, rows, columns) VALUES (?, ?, ?, ?)',
                (name, file_path, len(df), len(df.columns))
            )
            conn.commit()
            return cursor.lastrowid

    def get_datasets(self):
        """Retorna todos los datasets ordenados por fecha descendente."""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(
                'SELECT * FROM datasets ORDER BY upload_date DESC', conn
            )

    def delete_dataset(self, dataset_id):
        """Elimina un dataset y sus registros relacionados."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM datasets WHERE id = ?', (dataset_id,))
            conn.commit()

    # ------------------------------------------------------------------
    # CRUD - Resultados de analisis ML
    # ------------------------------------------------------------------

    def save_analysis_result(self, dataset_id, algorithm, metrics):
        """
        Guarda las metricas de un modelo ML.
        metrics debe contener: r2_score, mae, cv_score.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''INSERT INTO analysis_results
                   (dataset_id, algorithm, r2_score, mae, cv_score)
                   VALUES (?, ?, ?, ?, ?)''',
                (
                    dataset_id,
                    algorithm,
                    metrics.get('r2_score', 0.0),
                    metrics.get('mae', 0.0),
                    metrics.get('cv_score', 0.0),
                )
            )
            conn.commit()

    def get_analysis_results(self, dataset_id=None):
        """Retorna resultados de ML. Si se pasa dataset_id, filtra por el."""
        with sqlite3.connect(self.db_path) as conn:
            if dataset_id:
                return pd.read_sql_query(
                    'SELECT * FROM analysis_results WHERE dataset_id = ? ORDER BY created_at DESC',
                    conn, params=(dataset_id,)
                )
            return pd.read_sql_query(
                'SELECT * FROM analysis_results ORDER BY created_at DESC', conn
            )

    # ------------------------------------------------------------------
    # CRUD - Historial de chat IA
    # ------------------------------------------------------------------

    def save_chat_message(self, question, response, dataset_id=None, provider='gemini'):
        """Persiste un turno de conversacion con la IA."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''INSERT INTO chat_history (dataset_id, provider, question, response)
                   VALUES (?, ?, ?, ?)''',
                (dataset_id, provider, question, response)
            )
            conn.commit()

    def get_chat_history(self, dataset_id=None, limit=50):
        """Retorna el historial de chat, opcionalmente filtrado por dataset."""
        with sqlite3.connect(self.db_path) as conn:
            if dataset_id:
                return pd.read_sql_query(
                    '''SELECT * FROM chat_history WHERE dataset_id = ?
                       ORDER BY created_at DESC LIMIT ?''',
                    conn, params=(dataset_id, limit)
                )
            return pd.read_sql_query(
                'SELECT * FROM chat_history ORDER BY created_at DESC LIMIT ?',
                conn, params=(limit,)
            )

    def clear_chat_history(self, dataset_id=None):
        """Elimina el historial de chat, opcionalmente solo de un dataset."""
        with sqlite3.connect(self.db_path) as conn:
            if dataset_id:
                conn.execute('DELETE FROM chat_history WHERE dataset_id = ?', (dataset_id,))
            else:
                conn.execute('DELETE FROM chat_history')
            conn.commit()

    # ------------------------------------------------------------------
    # CRUD - Registro de exportaciones
    # ------------------------------------------------------------------

    def log_export(self, file_path, format_type, dataset_id=None):
        """Registra una exportacion realizada."""
        file_size_kb = 0.0
        if os.path.exists(file_path):
            file_size_kb = os.path.getsize(file_path) / 1024.0

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''INSERT INTO export_log (dataset_id, format, file_path, file_size_kb)
                   VALUES (?, ?, ?, ?)''',
                (dataset_id, format_type, file_path, file_size_kb)
            )
            conn.commit()

    def get_export_log(self, limit=30):
        """Retorna el historial de exportaciones."""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(
                'SELECT * FROM export_log ORDER BY exported_at DESC LIMIT ?',
                conn, params=(limit,)
            )

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def backup_database(self):
        """Crea una copia de seguridad del archivo .db."""
        backup_path = "backups/backup_{}.db".format(
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as source:
            with sqlite3.connect(backup_path) as backup:
                source.backup(backup)
        return backup_path

    def get_database_stats(self):
        """Retorna estadisticas generales de la base de datos."""
        stats = {}
        with sqlite3.connect(self.db_path) as conn:
            for table in ('datasets', 'analysis_results', 'chat_history', 'export_log'):
                cursor = conn.execute('SELECT COUNT(*) FROM {}'.format(table))
                stats[table] = cursor.fetchone()[0]
        return stats
