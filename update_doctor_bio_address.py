import sqlite3
import random

# List of sample streets, cities, states
streets = ["Main St", "Elm St", "Oak Ave", "Pine Rd", "Maple Ln", "Cedar Blvd", "Birch Way", "Willow Dr", "Ash Ct", "Spruce Pl"]
cities = ["Springfield", "Riverside", "Fairview", "Greenville", "Lakewood", "Hillcrest", "Sunnydale", "Woodland", "Brookside", "Meadowbrook"]
states = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]

# Bio templates based on department
bio_templates = {
    "ENT": [
        "Experienced ENT specialist dedicated to providing comprehensive care for ear, nose, and throat conditions.",
        "Passionate ENT doctor with expertise in diagnosing and treating a wide range of ENT disorders.",
        "Committed to improving patients' quality of life through advanced ENT treatments and surgeries."
    ],
    "Dental": [
        "Skilled dentist focused on preventive care and restorative dentistry to ensure healthy smiles.",
        "Dedicated dental professional specializing in cosmetic and general dentistry services.",
        "Committed to patient comfort and oral health through modern dental techniques and technology."
    ],
    "Eye": [
        "Expert ophthalmologist providing comprehensive eye care and vision correction services.",
        "Dedicated eye specialist with a focus on diagnosing and treating various eye conditions.",
        "Passionate about preserving and improving vision through advanced eye care treatments."
    ],
    "general": [
        "Compassionate general practitioner offering holistic healthcare for patients of all ages.",
        "Experienced family doctor committed to preventive medicine and patient education.",
        "Dedicated to providing comprehensive primary care with a patient-centered approach."
    ]
}

# Connect to the database
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Get all doctors
cursor.execute("SELECT id, department FROM doctor")
doctors = cursor.fetchall()

# Update each doctor
for doctor_id, department in doctors:
    # Generate random address
    street_num = random.randint(100, 999)
    street = random.choice(streets)
    city = random.choice(cities)
    state = random.choice(states)
    address = f"{street_num} {street}, {city}, {state}"

    # Generate bio based on department
    if department in bio_templates:
        bio = random.choice(bio_templates[department])
    else:
        bio = "Dedicated healthcare professional committed to providing excellent patient care."

    # Update the database
    cursor.execute("UPDATE doctor SET address = ?, bio = ? WHERE id = ?", (address, bio, doctor_id))
    print(f"Updated doctor {doctor_id} ({department}): Address - {address}, Bio - {bio}")

conn.commit()
conn.close()

print("All doctors updated with address and bio.")
