from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from models import db, Patient,Drugs,Doctor,Patientin,Patientout  # ✅ import db and Patient directly

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

@analytics_bp.route("/patients-by-gender")
def patients_by_gender():
    rows = (
    db.session.query(Patient.department, Patient.gender, func.count(Patient.id))
    .group_by(Patient.department, Patient.gender)
    .all()
)

    result = {}
    for dept, gender, count in rows:
        dept = dept or "Unknown Department"
        gender = gender or "Unknown Gender"
        
        if dept not in result:
            result[dept] = {}
        result[dept][gender] = int(count)

    return jsonify(result)

# Drugs per department
@analytics_bp.route("/drugs-per-department")
def drugs_per_department():
    rows = (
        db.session.query(Drugs.department, func.sum(Drugs.quantity))
        .group_by(Drugs.department)
        .all()
    )
    return jsonify({dept or "Unknown": int(qty or 0) for dept, qty in rows})

@analytics_bp.route("/drugs-stock-value")
def drugs_stock_value():
    rows = (
        db.session.query(Drugs.department, func.sum(Drugs.price * Drugs.quantity))
        .group_by(Drugs.department)
        .all()
    )
    return jsonify({dept or "Unknown": float(value) for dept, value in rows})

@analytics_bp.route("/low-stock-drugs")
def low_stock_drugs():
    # Define a threshold for low stock (e.g., 10 units)
    LOW_STOCK_THRESHOLD = 10
    rows = (
        db.session.query(Drugs.id, Drugs.name, Drugs.department, Drugs.quantity)
        .filter(Drugs.quantity <= LOW_STOCK_THRESHOLD)
        .all()
    )

    return jsonify([
        {
            "id": drug_id,
            "name": name,
            "department": dept,
            "quantity": int(qty),
            "threshold": LOW_STOCK_THRESHOLD
        }
        for drug_id, name, dept, qty in rows
    ])

@analytics_bp.route("/patients-by-age-group")
def patients_by_age_group():
    rows = (
        db.session.query(Patient.age)
        .filter(Patient.age != None)
        .all()
    )

    groups = {"0-18": 0, "19-35": 0, "36-60": 0, "60+": 0}
    for (age,) in rows:
        if age <= 18:
            groups["0-18"] += 1
        elif age <= 35:
            groups["19-35"] += 1
        elif age <= 60:
            groups["36-60"] += 1
        else:
            groups["60+"] += 1

    return jsonify(groups)

# Top doctors by number of patients
@analytics_bp.route("/patients-checkin-status")
def patients_checkin_status():
    checkins = db.session.query(func.count(Patientin.id)).scalar() or 0
    checkouts = db.session.query(func.count(Patientout.id)).scalar() or 0

    return jsonify({
        "Checked-in": int(checkins),
        "Checked-out": int(checkouts)
    })
