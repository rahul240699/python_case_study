import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from flask.helpers import get_load_dotenv
from flask_mail import Message
from flask_case_study import app, db, bcrypt, mail
from flask_case_study.forms import LoginForm, SelectClass, AdminEntry, RegistrationForm, UpdateAccountForm, ClassDetails, EventForm
from flask_case_study.models import User, Class_, Student, Events, E_registration
from flask_login import login_user, current_user, logout_user, login_required
from flask_case_study.queryFn import queryFeesAdmin, queryFeesStudent, updateFeesStudent, queryEmails
from datetime import datetime


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


user_val = ""
user_id = ""
class_val = ""
@app.route('/login', methods=['GET','POST'])
def login():
    global user_val
    global user_id
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        session["name"] = request.form.get("username")
        if user:
            login_user(user)
            if user.user_type =='Admin':
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('admin'))
            elif user.user_type =='Student':
                user_val = user.email
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('student'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session["name"]=None
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
@login_required
def admin():
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route("/admin/fees",methods=['GET','POST'])
@login_required
def adminFees():
    global class_val
    form = SelectClass()
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
        return redirect(url_for('login'))
    else:
        if form.validate_on_submit():
            class_val = form.classVal.data
            data = queryFeesAdmin(form.classVal.data)
            return render_template('feesAdmin.html',posts=data)

    return render_template('feesAdminClass.html', title='Login', form=form)
    
@app.route("/student")
@login_required
def student():
    a=current_user.user_type
    if a!='Student':
        flash('You Are not Authorised to access an student page.','danger')
        return redirect(url_for('login'))
    return render_template('student.html')


@app.route("/student/fees",methods=['GET','POST'])
@login_required
def studentFees():
    global user_val
    a=current_user.user_type
    if a!='Student':
        flash('You Are not Authorised to access an student page.','danger')
        return redirect(url_for('login'))
    else:
        data = queryFeesStudent(user_val)
        return render_template('feesStudent.html',posts=data)
    

@app.route("/student/payment",methods=['GET','POST'])
@login_required
def payment():
    a=current_user.user_type
    if a!='Student':
        flash('You Are not Authorised to access an student page.','danger')
        return redirect(url_for('login'))
    else:
        return render_template('payment.html')


@app.route("/student/fees2",methods=['GET','POST'])
@login_required
def updatePayment():
    global user_val
    a=current_user.user_type
    if a!='Student':
        flash('You Are not Authorised to access an student page.','danger')
        return redirect(url_for('login'))
    updateFeesStudent(user_val)
    data = queryFeesStudent(user_val)
    return render_template('feesStudent.html',posts=data)

@app.route("/admin/notification",methods=['GET','POST'])
@login_required
def sendNotification():
    global class_val
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
        return redirect(url_for('login'))
    else:
        data = queryEmails(class_val)
        msg = Message('URGENT!!!!', sender = 'vbssrschool@gmail.com', recipients = data)
        msg.body = "\nPlease pay your fees!"
        mail.send(msg)
        data = queryFeesAdmin(class_val)
        return render_template('feesAdmin.html',posts=data)

    
@app.route("/admin/addadmin",methods=['GET','POST'])
@login_required
def addAdmin():
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
    form=AdminEntry()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data,user_type="Admin")
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
    return render_template('addAdmin.html', title='Data Entry', form=form)

@app.route('/admin/registerStudent',methods=['GET','POST'])
@login_required
def registerStudent():
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
        return redirect(url_for('login'))
    else:
        form=RegistrationForm()
        if form.validate_on_submit():
            u=User(email=form.email.data,username=(form.name.data+form.fname.data),password="abc123",user_type="Student")
            db.session.add(u)
            db.session.commit()
            s=Student(Name=form.name.data,FName=form.fname.data,MName=form.mname.data,address=form.addr.data,cid=form.classs.data,phone=form.phno.data,p_email=form.person_email.data, user_email=form.email.data)
            db.session.add(s)
            db.session.commit()
            #fees added to table
            #studentDetails = Student.query.filter_by(user_email=form.email.data).first()
            flash(f'The data for student {form.name.data} has been succefully entered!','success')
            msg = Message('Your Account has been registered', sender = 'vbssrschool@gmail.com', recipients = [form.person_email.data])
            msg.body = "\nCongratulations!! \nYour student Account has been set up. \nUsername : {} \nPassword : {}".format(form.email.data,"abc123")
            mail.send(msg)
            flash(f'The Account has been created! and the Mail has been sent.', 'success')
            return redirect(url_for('home'))
    return render_template('addStudent.html',title='Register',form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/student/profile", methods=['GET', 'POST'])
@login_required
def displayStudent():
    a=current_user.user_type
    if a!='Student':
        flash('You Are not Authorised to access an student page.','danger')
        return redirect(url_for('login'))
    else:
        e=current_user.email
        s=Student.query.filter_by(user_email=e).first()
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                s.image_file = picture_file
            current_user.username = form.username.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('displayStudent'))
        elif request.method == 'GET':
            form.username.data = current_user.username
        s1=Student.query.filter_by(user_email=e).first()
        image_file = url_for('static', filename='profile_pics/' + s1.image_file)
    return render_template('displayStudent.html', title='Account',
                            image_file=image_file, form=form)

@app.route('/admin/class',methods=['GET','POST'])
@login_required
def about():
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
        return redirect(url_for('login'))
    else:
        form=ClassDetails()
        if form.validate_on_submit():
            idx=Student.query.filter_by(cid=form.classs.data)
            return render_template('displayClass.html',title='class-wise',posts=idx)
    return render_template('displayClassChoice.html',title='Details',form=form)

#sdalkfsa;ldkfjsa'pdkvjmsaldkvn/ms/lfdakvnjslkf/nj 
@app.route('/student/events',methods=['GET'])
@login_required
def RegisterEvents():
    a=current_user.user_type
    if a!='Student':
        flash('You Are not Authorised to access an student page.','danger')
        return redirect(url_for('login'))
    else:
        std = Student.query.filter_by(user_email=user_val).first()
        print(std)
        AllEvent = Events.query.all()
        print(AllEvent)
        currentDate = datetime.now()
        events = E_registration.query.filter_by(stu_id=std.sid).all()
        event_ids = []
        for e in events:
            event_ids.append(e.event_id)
        print(event_ids)
        return render_template('studentViEvents.html',Events=AllEvent,today=currentDate,RegisteredEvents=event_ids)

@app.route('/admin/events',methods=['GET'])
@login_required
def AdminViEvents():
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
        return redirect(url_for('login'))
    else:
        AllEvent = Events.query.all()
        currentDate = datetime.now()
        return render_template('adminViEvents.html',Events=AllEvent,today=currentDate)


@app.route("/student/eventIdUpdate",methods=['GET'])
@login_required
def EventIdUpdate():
    a=current_user.user_type
    if a!='Student':
        flash('You Are not Authorised to access an student page.','danger')
        return redirect(url_for('login'))
    else:
        std = Student.query.filter_by(user_email=user_val).first()
        EventId = request.args.get('Eid')
        eventRegistred = E_registration(event_id=EventId,stu_id=std.sid)
        db.session.add(eventRegistred)
        db.session.commit()
        return redirect(url_for('addEvent'))
     

@app.route("/admin/addEvent",methods=['GET','POST'])
@login_required
def addEvent():
    a=current_user.user_type
    if a!='Admin':
        flash('You Are not Authorised to access an admin page.','danger')
        return redirect(url_for('login'))
    else:
        form = EventForm()
        print(form.data['EventName'])
        if form.validate_on_submit():
            Event = Events(e_name=form.data['EventName'],description=form.data['EventDescription'],date_of_event=form.data['EventDate'])
            db.session.add(Event)
            db.session.commit()
            flash(f'New Event is created','success')
            return redirect(url_for('admin'))
    return render_template('addEvent.html',form=form)