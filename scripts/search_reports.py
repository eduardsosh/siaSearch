import sqlite3
from pathlib import Path
import csv

DB_FILE = Path("../database.db")

def search_business_reports(db_path, business_name):
    """
    Connects to the SQLite database, finds the business (or businesses)
    matching the given name, retrieves the registration code, and lists
    the available reports (documents/statements) for that business.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1) Find matching businesses by name
    # Adjust to your actual table/column names
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

    # 2) For each match, show the business registration code and available reports
    for (regcode, name) in matches:
        print(f"\nFound business: {name}, regcode: {regcode}")

        # 3) Look up documents (or statements) for this regcode
        # Here, we assume 'documents.legal_entity_registration_number' matches 'regcode'
        # If you only want the “documents” table:
        #
        # cursor.execute("""
        #     SELECT id, year, created_at
        #     FROM documents
        #     WHERE legal_entity_registration_number = ?
        # """, (regcode,))
        #
        # Or if you want to join “documents” with “statements” (matching file_id):
        cursor.execute("""
            SELECT d._id,
                   d.year,
                   d.created_at,
                   s.net_turnover,
                   s.net_income
            FROM reports d
            JOIN balance s
                ON d.file_id = s.file_id
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

    conn.close()

if __name__ == "__main__":
    db_file_path = DB_FILE  # Adjust to your actual database path
    name_to_search = input("Enter a business name to search: ")
    search_business_reports(db_file_path, name_to_search)
