import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

DB_FILE = Path("database.db")

def plot_top_10_profitable_businesses(db_path):
    """
    Connects to the SQLite database and produces a bar chart of
    the top 10 businesses by total net income.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to aggregate net_income by business
    cursor.execute("""
        SELECT u.name, SUM(b.net_income) AS total_income
        FROM uznemumi u
        JOIN reports r
            ON r.legal_entity_registration_number = u.regcode
        JOIN balance b
            ON b.file_id = r.file_id
        GROUP BY u.regcode
        ORDER BY total_income DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("No businesses found or no net_income data.")
        return

    # Separate the query results into lists for plotting
    business_names = [row[0] for row in rows]
    net_incomes = [row[1] if row[1] else 0 for row in rows]

    # Create a bar chart of net income vs business name
    plt.bar(business_names, net_incomes)
    plt.xlabel("Business")
    plt.ylabel("Total Net Income")
    plt.title("Top 10 Most Profitable Businesses by Net Income")
    
    # Make names readable if they're long
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()  # Adjust spacing so labels fit
    plt.show()

if __name__ == "__main__":
    plot_top_10_profitable_businesses(DB_FILE)
