import sqlite3

# Path to your database
db_path = r"E:\programs\healthcare\instance\database.db"

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("\n📋 Tables in Database:\n")
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    
    # Get schema of each table
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    print("Schema:")
    for col in schema:
        cid, name, dtype, notnull, dflt_value, pk = col
        print(f"  - {name} ({dtype}) {'PRIMARY KEY' if pk else ''}")
    print()

conn.close()
