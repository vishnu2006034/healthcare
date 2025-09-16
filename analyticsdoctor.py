from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import func, extract
from models import db, Patient, Doctor, Patientin, Patientout, Prescription
from flask_login import login_required, current_user

analyticsdoctor_bp = Blueprint("analyticsdoctor", __name__)

@analyticsdoctor_bp.route("/doctordashboard")
@login_required
def doctor_dashboard():
    return render_template("doctor_dashboard.html")

@analyticsdoctor_bp.route("/patient-flow-over-time")
@login_required
def patient_flow_over_time():
    # Group prescriptions by date for the current doctor
    rows = (
        db.session.query(
            func.date(Prescription.date).label('date'),
            func.count(Prescription.id).label('count')
        )
        .filter(Prescription.doctor_id == current_user.id)
        .group_by(func.date(Prescription.date))
        .order_by(func.date(Prescription.date))
        .all()
    )
    data = {str(date): int(count) for date, count in rows}
    return jsonify(data)

@analyticsdoctor_bp.route("/patient-visit-outcomes")
@login_required
def patient_visit_outcomes():
    from datetime import datetime, timedelta
    # Get daily patient counts for the past month (patients seen by this doctor)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    daily_counts = db.session.query(
        func.date(Prescription.date).label('date'),
        func.count(func.distinct(Prescription.patient_id)).label('count')
    ).filter(
        Prescription.doctor_id == current_user.id,
        Prescription.date >= start_date,
        Prescription.date <= end_date
    ).group_by(func.date(Prescription.date)).all()
    
    result = {str(row.date): int(row.count) for row in daily_counts}
    return jsonify(result)

@analyticsdoctor_bp.route("/patient-demographics")
@login_required
def patient_demographics():
    # Age groups for patients who have prescriptions by this doctor
    rows = (
        db.session.query(Patient.age)
        .join(Prescription, Prescription.patient_id == Patient.id)
        .filter(Prescription.doctor_id == current_user.id, Patient.age != None)
        .all()
    )

    age_groups = {"<18": 0, "18-40": 0, "40-60": 0, "60+": 0}
    for (age,) in rows:
        if age < 18:
            age_groups["<18"] += 1
        elif age <= 40:
            age_groups["18-40"] += 1
        elif age <= 60:
            age_groups["40-60"] += 1
        else:
            age_groups["60+"] += 1

    # Gender split
    gender_rows = (
        db.session.query(Patient.gender, func.count(Patient.id))
        .join(Prescription, Prescription.patient_id == Patient.id)
        .filter(Prescription.doctor_id == current_user.id)
        .group_by(Patient.gender)
        .all()
    )
    gender_data = {gender or "Unknown": int(count) for gender, count in gender_rows}

    return jsonify({"age_groups": age_groups, "gender": gender_data})
