import sqlite3
import csv
from pathlib import Path
from tqdm import tqdm

CSV_FILE = Path("datasets/report_data.csv")
DB_FILE = Path("database.db")

def load_reports():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            _id INTEGER PRIMARY KEY,
            id INTEGER,
            file_id INTEGER,
            legal_entity_registration_number TEXT,
            source_schema TEXT,
            source_type TEXT,
            year INTEGER,
            year_started_on TEXT,
            year_ended_on TEXT,
            employees INTEGER,
            rounded_to_nearest TEXT,
            currency TEXT,
            created_at TEXT
        )
    ''')

    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        total_rows = sum(1 for _ in f) - 1

    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)  

        with tqdm(total=total_rows, desc='Importing Reports', unit='rows', bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}') as pbar:
            for row in reader:
                cursor.execute('''
                    INSERT INTO reports (
                        _id,
                        id,
                        file_id,
                        legal_entity_registration_number,
                        source_schema,
                        source_type,
                        year,
                        year_started_on,
                        year_ended_on,
                        employees,
                        rounded_to_nearest,
                        currency,
                        created_at
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', row)
                pbar.update(1)

    conn.commit()
    conn.close()
