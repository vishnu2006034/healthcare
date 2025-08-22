from flask import Blueprint, render_template
from sqlalchemy import func
from app import db
from app import Patient, Doctor, Drugs, Patientin, Patientout, Prescription, DrugsHistory

analytics_bp = Blueprint("analytics", __name__)

# --- Patients per department ---
@analytics_bp.route("/analytics/patients_by_dept")
def patients_by_dept():
    result = db.session.query(
        Patient.department, func.count(Patient.id)
    ).group_by(Patient.department).all()

    depts = [r[0] for r in result]
    counts = [r[1] for r in result]

    return render_template("patients_by_dept.html", depts=depts, counts=counts)

# --- Doctors per department ---
@analytics_bp.route("/analytics/doctors_by_dept")
def doctors_by_dept():
    result = db.session.query(
        Doctor.department, func.count(Doctor.id)
    ).group_by(Doctor.department).all()

    depts = [r[0] for r in result]
    counts = [r[1] for r in result]

    return render_template("doctors_by_dept.html", depts=depts, counts=counts)

# --- Drugs low stock ---
@analytics_bp.route("/analytics/drugs_low_stock")
def drugs_low_stock():
    result = db.session.query(Drugs.name, Drugs.quantity).filter(Drugs.quantity < 10).all()
    names = [r[0] for r in result]
    qtys = [r[1] for r in result]

    return render_template("drugs_low_stock.html", names=names, qtys=qtys)

# --- Average stay duration ---
@analytics_bp.route("/analytics/avg_stay")
def avg_stay():
    result = db.session.query(
        func.avg(func.julianday(Patientout.check_out_time) - func.julianday(Patientin.check_in_time))
    ).join(Patientout, Patientin.patient_id == Patientout.patientid).scalar()

    return render_template("avg_stay.html", avg_days=result)
