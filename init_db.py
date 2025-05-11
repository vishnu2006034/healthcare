from app import db, app, Patient, Doctor, Drugs

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

    # Insert sample patients
    patient1 = Patient(name="John Doe", gender="Male", age=30, phone=1234567890, address="123 Main St", department="dental")
    patient2 = Patient(name="Jane Smith", gender="Female", age=25, phone=9876543210, address="456 Elm St", department="ENT")

    # Insert sample doctors
    doctor1 = Doctor(name="Dr. House", gender="Male", age=45, phone=1112223333, email="vishnu@example.com", password="111", department="ENT")
    doctor2 = Doctor(name="Dr. Wilson", gender="Male", age=50, phone=4445556666, email="tharun@example.com", password="111", department="dental")

    # Insert sample drugs
    drug1 = Drugs(name="Aspirin", department="dental", price=10.0, quantity=100)
    drug2 = Drugs(name="Ibuprofen", department="ENT", price=15.0, quantity=200)

    db.session.add_all([patient1, patient2, doctor1, doctor2, drug1, drug2])
    db.session.commit()
    print("Sample data inserted successfully.")
