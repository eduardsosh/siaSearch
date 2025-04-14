import sqlite3
import csv
from pathlib import Path
from tqdm import tqdm

CSV_FILE = Path("datasets/uznemumi.csv")
DB_FILE = Path("database.db")

def load_business():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uznemumi (
            _id INTEGER PRIMARY KEY,
            regcode TEXT,
            sepa TEXT,
            name TEXT,
            name_before_quotes TEXT,
            name_in_quotes TEXT,
            name_after_quotes TEXT,
            without_quotes INTEGER,
            regtype TEXT,
            regtype_text TEXT,
            type TEXT,
            type_text TEXT,
            registered TEXT,
            terminated TEXT,
            closed TEXT,
            address TEXT,
            "index" INTEGER,
            addressid INTEGER,
            region INTEGER,
            city INTEGER,
            atvk INTEGER,
            reregistration_term TEXT
        )
    ''')
    
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        total_rows = sum(1 for _ in f) - 1

    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)

        with tqdm(total=total_rows, desc='Importing Businesses', unit='rows', bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}') as pbar:
            for row in reader:
                cursor.execute('''
                    INSERT INTO uznemumi (
                        _id, 
                        regcode, 
                        sepa, 
                        name, 
                        name_before_quotes, 
                        name_in_quotes, 
                        name_after_quotes, 
                        without_quotes, 
                        regtype, 
                        regtype_text, 
                        type, 
                        type_text, 
                        registered, 
                        terminated, 
                        closed, 
                        address, 
                        "index", 
                        addressid, 
                        region, 
                        city, 
                        atvk, 
                        reregistration_term
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', row)
                pbar.update(1)

    conn.commit()
    conn.close()
