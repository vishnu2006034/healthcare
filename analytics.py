from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from app import db, Patient, Doctor, Drugs

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/dashboard")
def analytics_dashboard():
    return render_template("analytics.html")

@analytics_bp.route("/patients-per-department")
def patients_per_department():
    rows = (
        db.session.query(Patient.department, func.count(Patient.id))
        .group_by(Patient.department)
        .all()
    )
    return jsonify({dept or "Unknown": int(count) for dept, count in rows})

@analytics_bp.route("/drugs-per-department")
def drugs_per_department():
    rows = (
        db.session.query(Drugs.department, func.sum(Drugs.quantity))
        .group_by(Drugs.department)
        .all()
    )
    return jsonify({dept or "Unknown": int(qty or 0) for dept, qty in rows})

@analytics_bp.route("/top-doctors")
def top_doctors():
    # Example placeholder (adjust to your schema/relations)
    rows = (
        db.session.query(Doctor.name, func.count(Patient.id).label("patients"))
        .join(Patient, Patient.doctor_id == Doctor.id)
        .group_by(Doctor.id)
        .order_by(func.count(Patient.id).desc())
        .limit(10)
        .all()
    )
    return jsonify([{"name": name, "patients": int(p)} for name, p in rows])
