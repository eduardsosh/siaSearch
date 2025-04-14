import sqlite3
from pathlib import Path
import matplotlib.pyplot as plt

DB_FILE = Path("../database.db")

def plot_net_income_by_year(cursor, regcode, business_name):
    """
    For a given regcode, query (year, SUM(net_income)) from reports + balance,
    then display a bar chart of net_income by year.
    """
    cursor.execute("""
        SELECT d.year, SUM(b.net_income)
        FROM reports d
        JOIN balance b ON d.file_id = b.file_id
        WHERE d.legal_entity_registration_number = ?
        GROUP BY d.year
        ORDER BY d.year
    """, (regcode,))
    rows = cursor.fetchall()

    if not rows:
        print(f"  No net_income data found for this business: {business_name} (regcode: {regcode}).")
        return

    # Separate the query results into two lists for plotting
    years = [row[0] for row in rows]
    net_incomes = [row[1] if row[1] else 0 for row in rows]

    # Create a simple bar chart
    plt.bar(years, net_incomes)
    plt.xlabel("Year")
    plt.ylabel("Net Income")
    plt.title(f"Net Income by Year for '{business_name}' (regcode: {regcode})")
    plt.show()

def search_business_reports(db_path, business_name):
    """
    Connects to the SQLite database, finds the business (or businesses)
    matching the given name, retrieves the registration code, and lists
    the available reports (from 'reports' + 'balance') for that business.
    Also generates a bar chart of net_income by year.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1) Find matching businesses by name
    cursor.execute("""
        SELECT regcode, name
        FROM uznemumi
        WHERE name LIKE ?
    """, (f"%{business_name}%",))
    matches = cursor.fetchall()

    if not matches:
        print(f"No business found matching name '{business_name}'.")
        conn.close()
        return

    # 2) For each match, show the business regcode, then list available reports
    for (regcode, name) in matches:
        print(f"\nFound business: {name}, regcode: {regcode}")

        # 3) Query reports (documents) joined to balance by file_id
        cursor.execute("""
            SELECT d._id,
                   d.year,
                   d.created_at,
                   b.net_turnover,
                   b.net_income
            FROM reports d
            JOIN balance b ON d.file_id = b.file_id
            WHERE d.legal_entity_registration_number = ?
        """, (regcode,))

        reports = cursor.fetchall()

        if not reports:
            print("  No reports found for this business.")
        else:
            print("  Available reports:")
            for row in reports:
                doc_id, doc_year, doc_created, net_turnover, net_income = row
                print(f"    Document ID: {doc_id}, Year: {doc_year}, "
                      f"Created: {doc_created}, Turnover: {net_turnover}, Income: {net_income}")

        # 4) Generate a bar chart of net_income by year
        plot_net_income_by_year(cursor, regcode, name)

    conn.close()

if __name__ == "__main__":
    db_file_path = DB_FILE  # Or specify a different path if desired
    name_to_search = input("Enter a business name to search: ")
    search_business_reports(db_file_path, name_to_search)
