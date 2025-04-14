import sqlite3
from pathlib import Path
from tqdm import tqdm
import csv

CSV_FILE = Path("datasets/profit_loss.csv")
DB_FILE = Path("database.db")

def load_balance():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS balance (
            _id INTEGER PRIMARY KEY,
            statement_id INTEGER,
            file_id INTEGER,
            net_turnover REAL,
            by_nature_inventory_change REAL,
            by_nature_long_term_investment_expenses REAL,
            by_nature_other_operating_revenues REAL,
            by_nature_material_expenses REAL,
            by_nature_labour_expenses REAL,
            by_nature_depreciation_expenses REAL,
            by_function_cost_of_goods_sold REAL,
            by_function_gross_profit REAL,
            by_function_selling_expenses REAL,
            by_function_administrative_expenses REAL,
            by_function_other_operating_revenues REAL,
            other_operating_expenses REAL,
            equity_investment_earnings REAL,
            other_long_term_investment_earnings REAL,
            other_interest_revenues REAL,
            investment_fair_value_adjustments REAL,
            interest_expenses REAL,
            extra_revenues REAL,
            extra_expenses REAL,
            income_before_income_taxes REAL,
            provision_for_income_taxes REAL,
            income_after_income_taxes REAL,
            other_taxes REAL,
            extra_dividends REAL,
            net_income REAL
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
                    INSERT INTO balance (
                        _id,
                        statement_id,
                        file_id,
                        net_turnover,
                        by_nature_inventory_change,
                        by_nature_long_term_investment_expenses,
                        by_nature_other_operating_revenues,
                        by_nature_material_expenses,
                        by_nature_labour_expenses,
                        by_nature_depreciation_expenses,
                        by_function_cost_of_goods_sold,
                        by_function_gross_profit,
                        by_function_selling_expenses,
                        by_function_administrative_expenses,
                        by_function_other_operating_revenues,
                        other_operating_expenses,
                        equity_investment_earnings,
                        other_long_term_investment_earnings,
                        other_interest_revenues,
                        investment_fair_value_adjustments,
                        interest_expenses,
                        extra_revenues,
                        extra_expenses,
                        income_before_income_taxes,
                        provision_for_income_taxes,
                        income_after_income_taxes,
                        other_taxes,
                        extra_dividends,
                        net_income
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', row)
                pbar.update(1)

    conn.commit()
    conn.close()
