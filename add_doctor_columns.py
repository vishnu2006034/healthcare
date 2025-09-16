import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Add address column to doctor table
try:
    cursor.execute("ALTER TABLE doctor ADD COLUMN address TEXT")
    print("Added address column to doctor table.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Address column already exists.")
    else:
        print(f"Error adding address column: {e}")

# Add bio column to doctor table
try:
    cursor.execute("ALTER TABLE doctor ADD COLUMN bio TEXT")
    print("Added bio column to doctor table.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Bio column already exists.")
    else:
        print(f"Error adding bio column: {e}")

conn.commit()
conn.close()

print("Database schema updated.")
