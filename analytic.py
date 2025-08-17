from flask import Blueprint, render_template
from app import db, Patient
import pandas as pd
import plotly.express as px
import json

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.route("/dashboard")
def analytics_dashboard():
    # Query patient data
    patients = Patient.query.all()
    data = [{"age": p.age, "gender": p.gender, "department": p.department} for p in patients]
    df = pd.DataFrame(data)

    charts = {}

    # 1. Age Distribution
    fig1 = px.histogram(df, x="age", nbins=10, title="Patient Age Distribution")
    fig1.update_layout(template="plotly_white")
    charts["age_dist"] = json.dumps(fig1, cls=px.utils.PlotlyJSONEncoder)

    # 2. Gender Ratio
    fig2 = px.pie(df, names="gender", title="Gender Ratio")
    fig2.update_layout(template="plotly_white")
    charts["gender_ratio"] = json.dumps(fig2, cls=px.utils.PlotlyJSONEncoder)

    # 3. Department Count (replacing Disease Count)
    fig3 = px.bar(df["department"].value_counts().reset_index(),
                  x="index", y="department", title="Department Frequency",
                  labels={"index": "Department", "department": "Number of Patients"})
    fig3.update_layout(template="plotly_white")
    charts["department_count"] = json.dumps(fig3, cls=px.utils.PlotlyJSONEncoder)

    # 4. Age by Department (replacing Age by Disease)
    fig4 = px.box(df, x="department", y="age", title="Age Distribution by Department")
    fig4.update_layout(template="plotly_white")
    charts["age_by_department"] = json.dumps(fig4, cls=px.utils.PlotlyJSONEncoder)

    return render_template("dashboard.html", charts=charts)
