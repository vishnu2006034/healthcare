from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from models import db, Patient,Drugs,Doctor,Patientin,Patientout,DrugsHistory


analyticsdrug_bp = Blueprint("analyticsdrug", __name__)

@analyticsdrug_bp.route("/drugdashboard")
def analytics_drugdashboard():
    return render_template("druganalytics.html")

@analyticsdrug_bp.route("/top-prescribed-drugs")
def top_prescribed_drugs():
    rows = (
        db.session.query(Drugs.name, func.count(DrugsHistory.id).label('count'))
        .join(DrugsHistory, DrugsHistory.drugs_id == Drugs.id)
        .group_by(Drugs.id)
        .order_by(func.count(DrugsHistory.id).desc())
        .limit(10)
        .all()
    )
    return jsonify({name: int(count) for name, count in rows})

@analyticsdrug_bp.route("/department-drug-distribution")
def department_drug_distribution():
    rows = (
        db.session.query(Drugs.department, func.count(DrugsHistory.id).label('count'))
        .join(DrugsHistory, DrugsHistory.drugs_id == Drugs.id)
        .group_by(Drugs.department)
        .all()
    )
    return jsonify({dept or "Unknown": int(count) for dept, count in rows})

@analyticsdrug_bp.route("/drugs-low-stock")
def drugs_low_stock():
    rows = (
        db.session.query(Drugs.id, Drugs.name, Drugs.department, Drugs.quantity)
        .order_by(Drugs.quantity.asc())
        .limit(5)
        .all()
    )

    return jsonify([
        {
            "id": drug_id,
            "name": name,
            "department": dept,
            "quantity": int(qty),
            "threshold": 10
        }
        for drug_id, name, dept, qty in rows
    ])
