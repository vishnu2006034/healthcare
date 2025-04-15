from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

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

class Patientin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(255))

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/adminl', methods=['GET', 'POST'])
def adminl():
    if request.method == 'POST':
        code = "12345"
        hpassword = Admin(password=code)
        db.session.add(hpassword)
        db.session.commit()
        password = request.form.get('password')
        passes = Admin.query.filter_by(password=code).first()
        if password == passes.password:
            flash('successfully login')
            return redirect('adminp')
        else:
            flash('check the password ')
            return redirect(url_for('index'))
    return render_template('adminlogin.html')

@app.route('/adminp')
def adminp():
    return render_template('adminpage.html')

@app.route('/patreg', methods=["GET", "POST"])
def patreg():
    if request.method == "POST":
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age')
        phone = request.form.get('phone')
        address = request.form.get('address')
        department = request.form.get('dep')
        newpat = Patient(name=name, department=department, phone=phone, age=age, gender=gender, address=address)
        db.session.add(newpat)
        db.session.commit()
        flash("account is successfully created", "success")
        return redirect(url_for('adminp'))
    else:
        flash("check for the account already exists")
    return render_template("patreg.html")

@app.route('/search')
def search():
    q = request.args.get("q")
    patients = Patient.query.all()
    if q:
        result = Patient.query.filter(Patient.name.ilike(f'%{q}%') | Patient.address.ilike(f'%{q}%')).order_by(Patient.department.asc()).all()
    else:
        result = Patient.query.all()
    return render_template('adminpage.html', result=result, patients=patients)

@app.route('/checkin', methods=['GET', 'POST'])
def checkin_page():
    try:
        if request.method == 'POST':
            patient_id = request.form.get('patient_id')
            notes1 = request.form.get('notes', '')
            patient1 = Patient.query.get(patient_id)
            if not patient1:
                flash("Patient not found!", "error")
                return redirect(url_for('checkin_page'))

            record = Patientin(patient_id=patient_id, notes=notes1)
            db.session.add(record)
            db.session.commit()
            flash(f"Patient {patient1.name} checked in.", "success")
            return redirect(url_for('checkin_page'))

        shift2 = db.session.query(Patientin, Patient).join(Patient).all()
        return render_template('checkin.html', patients=shift2)

    except Exception as e:
        print("ERROR in checkin_page:", str(e))
        flash("An error occurred while processing your request", "error")
        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
