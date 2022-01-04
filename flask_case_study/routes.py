from flask import Flask, render_template, url_for,flash,redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_case_study.forms import EventForm
from flask_case_study import app, db
from flask_case_study.models import User, Class_,Student,Events,Fees,E_registration

User_id = ''

def dummyData():
   student = Student.query.first()
   std = Student.query.filter_by(sid=2).first()
   print(std)
   global User_id 
   User_id = student.sid
   print(User_id)
dummyData()
print("user_id",User_id)

@app.route('/')
@app.route('/home')
def hello():
    return 'Hello, World!'

@app.route('/admin')
def admin():
    return render_template('layout.html')


@app.route('/student/Events',methods=['GET'])
def RegisterEvents():
    AllEvent = Events.query.all()
    print(AllEvent)
    currentDate = datetime.now()
    events = E_registration.query.filter_by(stu_id=User_id).all()
    event_ids = []
    for e in events:
       event_ids.append(e.event_id)
    print(event_ids)
    return render_template('ViewEvents.html',Events=AllEvent,today=currentDate,RegisteredEvents=event_ids)

@app.route('/admin/Events',methods=['GET'])
def AdminViEvents():
    AllEvent = Events.query.all()
    currentDate = datetime.now()
    return render_template('adminViEvents.html',Events=AllEvent,today=currentDate)


@app.route("/Student/EventIdUpdate",methods=['GET'])
def EventIdUpdate():
    EventId = request.args.get('Eid')
    eventRegistred = E_registration(event_id=EventId,stu_id=User_id)
    db.session.add(eventRegistred)
    db.session.commit()
    return redirect(url_for('addEvent'))
     

@app.route("/admin/addEvent",methods=['GET','POST'])
def addEvent():
    form = EventForm()
    print(form.data['EventName'])
    if form.validate_on_submit():
        Event = Events(e_name=form.data['EventName'],description=form.data['EventDescription'],date_of_event=form.data['EventDate'])
        db.session.add(Event)
        db.session.commit()
        flash(f'New Event is created','success')
        return redirect(url_for('admin'))
    return render_template('addEvent.html',form=form)


