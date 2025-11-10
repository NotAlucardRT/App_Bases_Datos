import sqlite3
import pandas as pd
import os
from datetime import datetime
from config import DATABASE_CONFIG

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_CONFIG['path']
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS datasets (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_path TEXT,
                    rows INTEGER,
                    columns INTEGER
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY,
                    dataset_id INTEGER,
                    algorithm TEXT,
                    accuracy REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (dataset_id) REFERENCES datasets (id)
                )
            ''')
    
    def save_dataset(self, name, file_path, df):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO datasets (name, file_path, rows, columns)
                VALUES (?, ?, ?, ?)
            ''', (name, file_path, len(df), len(df.columns)))
            return cursor.lastrowid
    
    def get_datasets(self):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query('SELECT * FROM datasets ORDER BY upload_date DESC', conn)
    
    def save_analysis_result(self, dataset_id, algorithm, accuracy):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO analysis_results (dataset_id, algorithm, accuracy)
                VALUES (?, ?, ?)
            ''', (dataset_id, algorithm, accuracy))
    
    def backup_database(self):
        backup_path = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as source:
            with sqlite3.connect(backup_path) as backup:
                source.backup(backup)
        return backup_path