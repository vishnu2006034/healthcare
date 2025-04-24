from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import LoginManager, current_user, login_user, logout_user, login_required,UserMixin
import logger
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')



def is_active(self):
        return True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
login = LoginManager(app)
login.login_view = 'doclogin'

db = SQLAlchemy(app)

@login.user_loader
def load_user(user_id):
    try:
        return Doctor.query.get(int(user_id))
    except Exception as e:
        logger.error(e)
        return None


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

class Doctor(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)

class Patientin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(255))

class Patientout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientid = db.Column(db.Integer, db.ForeignKey('patient.id'),nullable=False)
    check_out_time = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(255))

class Medical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(15))

class Drugs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    prescription_text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

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
    return render_template('adminmain.html')

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

@app.route('/docreg', methods=["GET", "POST"])
def docreg():
    if current_user.is_authenticated:  # if the employee password is correct open the employee profile
        return redirect(url_for('docpro'))
    if request.method == "POST":  # to get information for employee
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('dep')
        phone = request.form.get('phone')
        age = request.form.get('age')
        gender = request.form.get('gender')
        password = request.form.get('password')
        
        newdoc = Doctor(name=name, email=email, department=department, phone=phone, age=age, gender=gender, password=password)
        db.session.add(newdoc)
        db.session.commit()
        flash("account is successfully created", "success")
        return redirect(url_for('doclogin')) # after the registraion returns to login page
    else:
        flash("check for the account already exists")
    return render_template("docreg.html")  # it is the registration html
    
@app.route('/doclogin', methods=["GET", "POST"])
def doclogin():
    if current_user.is_authenticated:  # checks the email and password
        return redirect(url_for('docpro'))
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        doc = Doctor.query.filter_by(email=email).first()
        if doc and doc.password == password:  # if the email and pass match show the profile
            login_user(doc)
            return redirect(url_for('docpro'))
        else:
            flash("login details is wrong", "error")
    return render_template("doclogin.html")


@app.route("/docpro")
@login_required
def docpro ():
    patients = db.session.query(Patientin, Patient).join(Patient, Patientin.patient_id == Patient.id).filter(Patient.department == current_user.department).all()

    # doc = Doctor.query.get(current_user.id) 
    return render_template("docpage.html",patients=patients)

@app.route('/add_prescription', methods=['POST'])
@login_required
def add_prescription():
    patient_id = request.form.get('patient_id')
    prescription_text = request.form.get('prescription_text')
    if not patient_id or not prescription_text:
        flash('Please provide all required fields', 'error')
        return redirect(url_for('docpro'))
    prescription = Prescription(patient_id=patient_id, doctor_id=current_user.id, prescription_text=prescription_text)
    db.session.add(prescription)
    db.session.commit()
    flash('Prescription added successfully', 'success')
    return redirect(url_for('docpro'))

@app.route('/search')
def search():
    q = request.args.get("q", "")
    query = Patient.query

    if q:
        query = query.filter(
            Patient.name.ilike(f"%{q}%") | Patient.address.ilike(f"%{q}%"  )
        )
    result = query.order_by(Patient.id.asc()).all()

    data = []
    for patient in result:
        data.append({
            "id":patient.id,
            "name": patient.name,
            "age":patient.age,
            "address": patient.address,
            "department": patient.department,
            "gender": patient.gender,
            "phone": patient.phone
            # add more fields as needed
        })

    return jsonify(data)


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
            existing_checkin = Patientin.query.filter_by(patient_id=patient_id).first()
            if existing_checkin:
                flash(f"Patient {patient1.name} is already checked in.", "error")
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

@app.route('/checkout' , methods=['GET' , 'POST'])
def checkout_page():
    if request.method == 'POST':
        patientid = request.form.get('patientid')
        notes= request.form.get('notes','')
        patientin = Patientin.query.get(patientid)
        if not patientin:
            flash("Patient not found!", "error")
            return redirect(url_for('checkout_page'))
        checkout = Patientout( patientid = patientin.patient_id,check_out_time = patientin.check_in_time , notes= patientin.notes)
        db.session.add(checkout)
        db.session.delete(patientin)
        db.session.commit()

    checkout1 = db.session.query(Patientout,Patient).join(Patient).all()
    return render_template('checkout.html', patients=checkout1 )

@app.route('/medl' , methods=['GET','POST'])
def medl():
    if request.method == 'POST':
        code="123"
        hpassword = Medical(password=code)
        db.session.add(hpassword)
        db.session.commit()
        password = request.form.get('password')
        passes = Medical.query.filter_by(password=code).first()
        if password == passes.password:
            flash('successfully login')
            return redirect('medp')
        else:
            flash('check the password ')
            return redirect(url_for('index'))
    return render_template('medlogin.html')

@app.route('/medp')
def medp():
    #press = db.session.query(Prescription,Patient,Doctor).join(Patient,Prescription.patient_id==Patient.id).join(Doctor,Prescription.doctor_id==Doctor.id).all()
    press = db.session.query(Prescription, Patient, Doctor).join(Patient, Prescription.patient_id == Patient.id).join(Doctor, Prescription.doctor_id == Doctor.id).all()
    return render_template('medpage.html',press=press)

@app.route('/drugsreg',methods=['GET','POST'])
def drugsreg():
    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        newdrug= Drugs(name=name, department=department,price=price,quantity=quantity)
        db.session.add(newdrug)
        db.session.commit()
        flash("the drugs has been added")
        return redirect(url_for('medp'))
    else:
        flash("the durgs is already there")
    return render_template('drugreg.html')

@app.route('/selectdrug', methods=['GET', 'POST'])
def selectdrug():
    drugs = Drugs.query.all()

    if request.method == 'POST':
        selected_id = request.form['drug_id']
        return redirect(url_for('updrugs', drug_id=selected_id))

    return render_template('selectdrug.html', drugs=drugs)
@app.route('/updrugs/<int:drug_id>',methods = ['GET','POST'])
def updrugs(drug_id):
    drug=Drugs.query.get(drug_id)
    if request.method == 'POST':
        drug.price=float(request.form['price'])
        drug.quantity=int(request.form['quantity'])
        db.session.commit()
    return render_template('updrug.html', drug=drug)

@app.route("/logout")
def logout():
    logout_user()  # log out user
    return redirect(url_for('doclogin'))
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
