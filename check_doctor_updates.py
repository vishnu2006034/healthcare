import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Query to get all doctors with address and bio
cursor.execute("SELECT id, name, department, address, bio FROM doctor")
rows = cursor.fetchall()

print("Doctor Updates:")
for row in rows:
    doctor_id, name, department, address, bio = row
    print(f"ID: {doctor_id}, Name: {name}, Dept: {department}")
    print(f"  Address: {address}")
    print(f"  Bio: {bio}")
    print()

conn.close()
