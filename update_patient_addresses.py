import sqlite3
import random

# List of sample streets, cities, states
streets = ["Main St", "Elm St", "Oak Ave", "Pine Rd", "Maple Ln", "Cedar Blvd", "Birch Way", "Willow Dr", "Ash Ct", "Spruce Pl"]
cities = ["Springfield", "Riverside", "Fairview", "Greenville", "Lakewood", "Hillcrest", "Sunnydale", "Woodland", "Brookside", "Meadowbrook"]
states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]

# Connect to the database
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Get all patient IDs
cursor.execute("SELECT id FROM patient")
patient_ids = [row[0] for row in cursor.fetchall()]

# Update each patient's address with a random address
for patient_id in patient_ids:
    street_num = random.randint(100, 999)
    street = random.choice(streets)
    city = random.choice(cities)
    state = random.choice(states)
    address = f"{street_num} {street}, {city}, {state}"
    cursor.execute("UPDATE patient SET address = ? WHERE id = ?", (address, patient_id))
    print(f"Updated patient {patient_id} to address: {address}")

conn.commit()
conn.close()

print("All patient addresses updated successfully.")
