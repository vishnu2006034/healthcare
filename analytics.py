from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from models import db, Patient,Drugs,Doctor   # ✅ import db and Patient directly

# analytics.py


analytics_bp = Blueprint("analytics", __name__)

# Dashboard page
@analytics_bp.route("/dashboard")
def analytics_dashboard():
    return render_template("analytics.html")


# Patients per department
@analytics_bp.route("/patients-per-department")
def patients_per_department():
    rows = (
        db.session.query(Patient.department, func.count(Patient.id))
        .group_by(Patient.department)
        .all()
    )
    return jsonify({dept or "Unknown": int(count) for dept, count in rows})


# Drugs per department
@analytics_bp.route("/drugs-per-department")
def drugs_per_department():
    rows = (
        db.session.query(Drugs.department, func.sum(Drugs.quantity))
        .group_by(Drugs.department)
        .all()
    )
    return jsonify({dept or "Unknown": int(qty or 0) for dept, qty in rows})


# Top doctors by number of patients
@analytics_bp.route("/top-doctors")
def top_doctors():
    rows = (
        db.session.query(Doctor.name, func.count(Patient.id).label("patients"))
        .join(Patient, Patient.doctor_id == Doctor.id)
        .group_by(Doctor.id)
        .order_by(func.count(Patient.id).desc())
        .limit(10)
        .all()
    )
    return jsonify([
        {"name": name, "patients": int(patients)}
        for name, patients in rows
    ])
