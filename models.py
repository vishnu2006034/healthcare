from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

def without_microseconds():
    return datetime.utcnow().replace(microsecond=0)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)

class Doctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=True, default='default_profile.png')

class Patientin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, default=without_microseconds)
    notes = db.Column(db.String(255))

class Patientout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientid = db.Column(db.Integer, db.ForeignKey('patient.id'),nullable=False)
    check_out_time = db.Column(db.DateTime, default=without_microseconds)
    notes = db.Column(db.String(255))

class Medical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(15))

class Drugs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    prescription_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=without_microseconds)

class DrugsHistory(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    patient_id= db.Column(db.Integer , db.ForeignKey('patient.id'),nullable =False)
    drugs_id = db.Column(db.Integer, db.ForeignKey('drugs.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=without_microseconds)
