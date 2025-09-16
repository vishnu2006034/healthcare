import sqlite3

# Path to your database
db_path = r"E:\programs\healthcare\instance\database.db"

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get updated doctor pictures
cursor.execute("SELECT id, name, picture FROM doctor")
doctors = cursor.fetchall()

print("Updated doctor pictures:")
for doc in doctors:
    print(f"ID: {doc[0]}, Name: {doc[1]}, Picture: {doc[2]}")

conn.close()
