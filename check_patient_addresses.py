import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Query to get all patient addresses
cursor.execute("SELECT id, name, address FROM patient")
rows = cursor.fetchall()

print("Current Patient Addresses:")
for row in rows:
    patient_id, name, address = row
    print(f"ID: {patient_id}, Name: {name}, Address: {address}")

conn.close()
