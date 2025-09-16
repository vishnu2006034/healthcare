from flask import Blueprint, render_template, jsonify
from models import db, Patient, Doctor, Medical, Patientin, Patientout, Prescription, DrugsHistory, Drugs
from sqlalchemy import func
from datetime import datetime, timedelta

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/superadmin/dashboard")
def superadmin_dashboard():
    return render_template("analytics.html")

@analytics_bp.route("/superadmin/workflow")
def workflow_data():
    # Total patients registered
    total_patients = db.session.query(func.count(Patient.id)).scalar() or 0

    # Total doctors registered
    total_doctors = db.session.query(func.count(Doctor.id)).scalar() or 0

    # Total medical staff registered
    total_medical = db.session.query(func.count(Medical.id)).scalar() or 0

    # Patients currently checked in
    checked_in = db.session.query(func.count(Patientin.id)).scalar() or 0

    # Patients currently checked out (today)
    today = datetime.now().date()
    checked_out = db.session.query(func.count(Patientout.id)).filter(
        func.date(Patientout.check_out_time) == today
    ).scalar() or 0

    # Prescriptions count in last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    prescriptions_last_month = db.session.query(func.count(Prescription.id)).filter(
        Prescription.date >= start_date,
        Prescription.date <= end_date
    ).scalar() or 0

    # Drugs inventory summary
    total_drugs = db.session.query(func.count(Drugs.id)).scalar() or 0
    total_drugs_quantity = db.session.query(func.sum(Drugs.quantity)).scalar() or 0

    return jsonify({
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_medical": total_medical,
        "checked_in": checked_in,
        "checked_out": checked_out,
        "prescriptions_last_month": prescriptions_last_month,
        "total_drugs": total_drugs,
        "total_drugs_quantity": total_drugs_quantity
    })

@analytics_bp.route("/patients-per-department")
def patients_per_department():
    result = db.session.query(
        Patient.department, func.count(Patient.id)
    ).group_by(Patient.department).all()
    data = {r[0]: r[1] for r in result}
    return jsonify(data)

@analytics_bp.route("/patients-by-age-group")
def patients_by_age_group():
    rows = db.session.query(Patient.age).filter(Patient.age != None).all()
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
    return jsonify(age_groups)

@analytics_bp.route("/patients-checkin-status")
def patients_checkin_status():
    checked_in = db.session.query(func.count(Patientin.id)).scalar() or 0
    checked_out = db.session.query(func.count(Patientout.id)).scalar() or 0
    return jsonify({"Checked In": checked_in, "Checked Out": checked_out})

@analytics_bp.route("/workflow-overview")
def workflow_overview():
    # Workflow steps: Registration -> Check-in -> Prescription -> Drug Dispensing -> Check-out
    total_patients = db.session.query(func.count(Patient.id)).scalar() or 0
    checked_in = db.session.query(func.count(Patientin.id)).scalar() or 0
    prescriptions = db.session.query(func.count(Prescription.id)).scalar() or 0
    drugs_dispensed = db.session.query(func.count(DrugsHistory.id)).scalar() or 0
    checked_out = db.session.query(func.count(Patientout.id)).scalar() or 0
    
    return jsonify({
        "Registered": total_patients,
        "Checked In": checked_in,
        "Prescribed": prescriptions,
        "Drugs Dispensed": drugs_dispensed,
        "Checked Out": checked_out
    })
