from flask import Flask, render_template, request, redirect, url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'

db=SQLAlchemy(app)

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender=db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable= False)
    department = db.Column(db.String, nullable=False)
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'gender':self.gender,
            'department':self.department,
            'address':self.address,
            'phone':self.phone
        }

class patientin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False)
    check_in_time = db.Column(db.DateTime,default=datetime.utcnow)
    notes=db.Column(db.String(255))
#patient=db.relationship('Patient' ,backref='checkins')

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/adminl', methods=['GET','POST'])
def adminl():
    if request.method == 'POST':
        code="12345"
        hpassword= admin(password=code)
        db.session.add(hpassword)  # stores the hpassword in session and saves in db
        db.session.commit()
        password = request.form.get('password')  # it get the password from user
        passes = admin.query.filter_by(password=code).first()  # it takes the first value in man.db which is the first code stored
        if password == passes.password: 
            flash('successfully login')
            return redirect('adminp')  # guides to the admin page
        else:
            flash('check the password ')
            return redirect(url_for('index'))
    return render_template('adminlogin.html')

@app.route('/adminp')
def adminp():
    
    return render_template('adminpage.html')

@app.route('/patreg', methods=["GET", "POST"])
def patreg():
        if request.method == "POST":  # to get information for employee
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
            return redirect(url_for('adminp')) # after the registraion returns to login page
        else:
            flash("check for the account already exists")
        return render_template("patreg.html") 

# @app.route('/pati')
# def get_patients():
#     patients= Patient.query.all()
#     return jsonify([p.to_dict() for p in patients])

@app.route('/search')
def search():
    
    q = request.args.get("q")
    print(q)
    patients=Patient.query.all()
    
    if q:
        result = Patient.query.filter(Patient.name.icontains(q) | Patient.address.icontains(q)).order_by(Patient.department.asc()).all()
    else:
        result=Patient.query.all()

    return render_template('adminpage.html',result=result,patients=patients)

@app.route('/checkin', methods=['GET', 'POST'])
def checkin_page():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        notes1 = request.form.get('notes', '')
        #Patient = Patient.query.all()
        patient1 = Patient.query.get(patient_id)
        if not patient1:
            flash("Patient not found!", "error")
            return redirect(url_for('checkin_page'))
        record = patientin(patient_id=patient_id, notes=notes1)
        db.session.add(record)
        db.session.commit()
        flash(f"Patient {Patient.name} checked in.", "success")
        return redirect(url_for('checkin_page'))
    shift2 = db.session.query(Patientin, Patient).join(Patient).all()
    return render_template('checkin.html',patients=shift2)

if __name__ == '__main__':
    with app .app_context():
        db.create_all()
    app.run(debug=True)
