from flask import render_template, url_for, flash, redirect, request
from flask.helpers import get_load_dotenv
from flask_case_study import app, db, bcrypt
from flask_case_study.forms import LoginForm, SelectClass
from flask_case_study.models import User, Class_
from flask_login import login_user, current_user, logout_user, login_required
from flask_case_study.queryFn import queryFeesAdmin, queryFeesStudent, updateFeesStudent

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


user_val = ""
@app.route('/login', methods=['GET','POST'])
def login():
    global user_val
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        
        if user:
            login_user(user)
            if user.user_type =='Admin':
                return redirect(url_for('admin'))
            elif user.user_type =='Student':
                user_val = user.email
                return redirect(url_for('student'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
def admin():
    if current_user.is_authenticated:
        return render_template('layoutAdmin.html')
    else:
        return redirect(url_for('login'))

@app.route("/admin/fees",methods=['GET','POST'])
def adminFees():
    form = SelectClass()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            data = queryFeesAdmin(form.classVal.data)
            return render_template('feesAdmin.html',posts=data)
    else:
        return redirect(url_for('login'))
    return render_template('feesAdminClass.html', title='Login', form=form)
    

@app.route("/student")
def student():
    if current_user.is_authenticated:
        return render_template('layoutStudent.html')
    else:
        return redirect(url_for('login'))

@app.route("/student/fees",methods=['GET','POST'])
def studentFees():
    global user_val
    if current_user.is_authenticated:
        data = queryFeesStudent(user_val)
        return render_template('feesStudent.html',posts=data)
    else:
        return redirect(url_for('login'))

@app.route("/student/payment",methods=['GET','POST'])
def payment():
    if current_user.is_authenticated:
        return render_template('payment.html')
    else:
        return redirect(url_for('login'))

@app.route("/student/fees2",methods=['GET','POST'])
def updatePayment():
    global user_val
    updateFeesStudent(user_val)
    data = queryFeesStudent(user_val)
    return render_template('feesStudent.html',posts=data)


