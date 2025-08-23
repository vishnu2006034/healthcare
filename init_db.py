# from app import db, app, Patient, Doctor, Drugs
from model import db,Patient,Doctor,drug

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

    # Insert sample patients
    patient1 = Patient(name="John Doe", gender="Male", age=30, phone=1234567890, address="123 Main St", department="dental")
    patient2 = Patient(name="Jane Smith", gender="Female", age=25, phone=9876543210, address="456 Elm St", department="ENT")
#     patient1 = Patient(name="Arjun Mehta", gender="Male", age=34, phone=9876501234, address="12 MG Road", department="Dental")
# patient2 = Patient(name="Priya Sharma", gender="Female", age=28, phone=9123456789, address="45 Residency St", department="Dental")
    patient3 = Patient(name="Vikram Patel", gender="Male", age=41, phone=9988776655, address="78 Civil Lines", department="Dental")

    patient4 = Patient(name="Ananya Rao", gender="Female", age=25, phone=8899776655, address="22 Park Ave", department="ENT")
    patient5 = Patient(name="Rohan Kapoor", gender="Male", age=37, phone=7766554433, address="9 Lake View", department="ENT")
    patient6 = Patient(name="Sneha Nair", gender="Female", age=30, phone=6655443322, address="17 Green Park", department="ENT")

    patient7 = Patient(name="Karan Verma", gender="Male", age=29, phone=7788996655, address="4 Lotus Nagar", department="Eye")
    patient8 = Patient(name="Meera Iyer", gender="Female", age=33, phone=8877665544, address="15 Rose Colony", department="Eye")
    patient9 = Patient(name="Rajiv Singh", gender="Male", age=46, phone=9090901234, address="56 Central Rd", department="Eye")

    patient10 = Patient(name="Neha Gupta", gender="Female", age=31, phone=8001234567, address="33 Shanti Vihar", department="general")
    patient11 = Patient(name="Amit Khanna", gender="Male", age=52, phone=9002345678, address="20 Gandhi Nagar", department="general")
    patient12 = Patient(name="Divya Menon", gender="Female", age=27, phone=7003456789, address="65 Sunrise Apartments", department="general")

    # Insert sample doctors
    doctor1 = Doctor(name="Dr. House", gender="Male", age=45, phone=1112223333, email="vishnu@gmail.com", password="111", department="ENT", picture="static/profile_photo/doc1")
    doctor2 = Doctor(name="Dr. Priya Menon", gender="Female", age=39, phone=2223334444, email="priya.ent@gmail.com", password="111", department="ENT", picture="static/profile_photo/doc2")

    doctor3 = Doctor(name="Dr. Wilson", gender="Male", age=50, phone=4445556666, email="tharun@gmail.com", password="111", department="Dental", picture="static/profile_photo/doc3")
    doctor4 = Doctor(name="Dr. Anjali Verma", gender="Female", age=42, phone=5556667777, email="anjali.dental@gmail.com", password="111", department="Dental", picture="static/profile_photo/doc4")

    doctor5 = Doctor(name="Dr. Karan Rao", gender="Male", age=38, phone=6667778888, email="karan.eye@gmail.com", password="111", department="Eye", picture="static/profile_photo/doc5")
    doctor6 = Doctor(name="Dr. Meera Iyer", gender="Female", age=35, phone=7778889999, email="meera.eye@gmail.com", password="111", department="Eye", picture="static/profile_photo/doc6")

    doctor7 = Doctor(name="Dr. Amit Sharma", gender="Male", age=48, phone=8889990000, email="amit.general@gmail.com", password="111", department="general", picture="static/profile_photo/doc7")
    doctor8 = Doctor(name="Dr. Sneha Kapoor", gender="Female", age=40, phone=9990001111, email="sneha.general@gmail.com", password="111", department="general", picture="static/profile_photo/doc8")

    # Insert sample drugs
    # Dental Drugs
    drug1 = Drugs(name="Aspirin", department="dental", price=10.0, quantity=100)
    drug2 = Drugs(name="Paracetamol", department="dental", price=12.0, quantity=150)
    drug3 = Drugs(name="Chlorhexidine Mouthwash", department="dental", price=60.0, quantity=80)
    drug4 = Drugs(name="Lidocaine Gel", department="dental", price=45.0, quantity=90)
    drug5 = Drugs(name="Amoxicillin Clavulanate", department="dental", price=75.0, quantity=110)

    # ENT Drugs
    drug6 = Drugs(name="Ibuprofen", department="ENT", price=15.0, quantity=200)
    drug7 = Drugs(name="Cetirizine", department="ENT", price=8.0, quantity=120)
    drug8 = Drugs(name="Fluticasone Nasal Spray", department="ENT", price=150.0, quantity=70)
    drug9 = Drugs(name="Amoxicillin", department="ENT", price=25.0, quantity=180)
    drug10 = Drugs(name="Pseudoephedrine", department="ENT", price=35.0, quantity=95)

    # Eye Drugs
    drug11 = Drugs(name="Timolol Eye Drops", department="Eye", price=50.0, quantity=75)
    drug12 = Drugs(name="Artificial Tears", department="Eye", price=30.0, quantity=90)
    drug13 = Drugs(name="Latanoprost", department="Eye", price=200.0, quantity=60)
    drug14 = Drugs(name="Ciprofloxacin Eye Drops", department="Eye", price=120.0, quantity=85)
    drug15 = Drugs(name="Ketorolac Eye Drops", department="Eye", price=95.0, quantity=100)

    # General Drugs
    drug16 = Drugs(name="Amoxi", department="general", price=25.0, quantity=180)
    drug17 = Drugs(name="Metformin", department="general", price=40.0, quantity=130)
    drug18 = Drugs(name="Losartan", department="general", price=55.0, quantity=140)
    drug19 = Drugs(name="Atorvastatin", department="general", price=65.0, quantity=150)
    drug20 = Drugs(name="Omeprazole", department="general", price=35.0, quantity=160)


    db.session.add_all([
    # Patients
    patient1, patient2, patient3, patient4, patient5, patient6,
    patient7, patient8, patient9, patient10, patient11, patient12,

    # Doctors
    doctor1, doctor2, doctor3, doctor4,
    doctor5, doctor6, doctor7, doctor8,

    # Drugs
    drug1, drug2, drug3, drug4, drug5,
    drug6, drug7, drug8, drug9, drug10,
    drug11, drug12, drug13, drug14, drug15,
    drug16, drug17, drug18, drug19, drug20
    ])

# db.session.commit()

    db.session.commit()
    print("Sample data inserted successfully.")
