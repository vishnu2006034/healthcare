from flask import Blueprint, render_template, jsonify
from sqlalchemy import func
from models import db, Patient,Drugs,Doctor,Patientin,Patientout


analyticsdrug_bp = Blueprint("analyticsdrug", __name__)

@analyticsdrug_bp.route("/drugdashboard")
def analytics_drugdashboard():
    return render_template("druganalytics.html")

@analyticsdrug_bp.route("/drugs-per-department")
def drugs_per_department():
    rows = (
        db.session.query(Drugs.department, func.sum(Drugs.quantity))
        .group_by(Drugs.department)
        .all()
    )
    return jsonify({dept or "Unknown": int(qty) for dept, qty in rows})

@analyticsdrug_bp.route("/drugs-stock-value")
def drugs_stock_value():
    rows = (
        db.session.query(Drugs.department, func.sum(Drugs.price * Drugs.quantity))
        .group_by(Drugs.department)
        .all()
    )
    return jsonify({dept or "Unknown": float(value) for dept, value in rows})

@analyticsdrug_bp.route("/drugs-low-stock")
def drugs_low_stock():
    rows = (
        db.session.query(Drugs.id, Drugs.name, Drugs.department, Drugs.quantity, Drugs.update_quantity)
        .filter(Drugs.quantity <= Drugs.update_quantity)  # flag when below threshold
        .all()
    )

    return jsonify([
        {
            "id": drug_id,
            "name": name,
            "department": dept,
            "quantity": int(qty),
            "threshold": int(update_qty)
        }
        for drug_id, name, dept, qty, update_qty in rows
    ])
