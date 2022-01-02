from flask import render_template, url_for, flash, redirect, request, session
from flask_case_study import app, db, bcrypt,mail
from flask_case_study.forms import LoginForm, dataEntry
from flask_case_study.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message

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
            session["name"] = request.form.get("username")
            if user.user_type =='Admin':
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin'))
            elif user.user_type =='Student':
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('student'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session["name"] = None
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
@login_required
def admin():
    return render_template('admin.html')

@app.route("/student")
@login_required
def student():
    return render_template('student.html')

@app.route("/dataentry",methods=['GET','POST'])
@login_required
def dataentry():
    #user_types=['Admin','Student']
    form=dataEntry()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data,user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()
        e_mail=user.email
        user_name=user.username
        pwd=user.password
        us_type=user.user_type
        msg = Message('Your Account has been registered', sender = 'vbssrschool@gmail.com', recipients = [user.email])
        msg.body = "\nCongratulations!! \nYour {} Account has been set up. \nUsername : {} \nPassword : {}".format(us_type,user_name,pwd)
        mail.send(msg)
        flash(f'The Account has been created! and the Mail has been sent.', 'success')
        return redirect(url_for('home'))
    return render_template('dataentry.html', title='Data Entry', form=form)
