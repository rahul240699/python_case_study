from flask import render_template, url_for, flash, redirect, request
from flask_case_study import app, db, bcrypt
from flask_case_study.forms import LoginForm
from flask_case_study.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            if user.user_type =='Admin':
                return redirect(url_for('admin'))
            elif user.user_type =='student':
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
    return render_template('admin.html')

@app.route("/student")
def student():
    return render_template('student.html')
