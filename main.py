from flask import Flask, render_template, url_for,flash,redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime
from forms import EventForm

app = Flask(__name__)
app.config['SECRET_KEY']='ff16b64ba5074f994657e6abb2fe9470'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db=SQLAlchemy(app)

# class User(db.Model):
#     id=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username=db.Column(db.String(20), unique=True, nullable=False)
#     email=db.Column(db.String(120), unique=True, nullable=False)
#     password=db.Column(db.String(60), nullable=False)
#     user_type=db.Column(db.String(20), nullable=False)
#     students=db.relationship('Student', backref='is_student',lazy=True)
    
#     def __repr__(self):
#         return f"User('{self.id}','{self.username}','{self.email}')"



    # def __repr__(self):
    #     return f"Student('{self.sid}','{self.Name}')"
# class Student(db.Model):
#     sid=db.Column(db.Integer, primary_key=True, autoincrement=True)
#     Name =db.Column(db.String(30), nullable=False)

#     def __repr__(self):
#         return f"Students('{self.sid}','{self.Name}')"
class Studentrecords(db.Model):
    sid=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name =db.Column(db.String(30), nullable=False,unique=True)



    def __repr__(self):
        return f"Students('{self.sid}','{self.Name}')"

class Events(db.Model):
    eid=db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_name=db.Column(db.String(30), nullable=False)
    description=db.Column(db.Text, nullable=False)
    date_of_event=db.Column(db.DateTime, nullable=False, default=datetime.now)
    # Status = db.Column(db.String(10),nullable=False)
    participants=db.relationship('e_registration',backref='part_taken',lazy=True)
    
    
    def __repr__(self):
        return f"Events('{self.eid}','{self.e_name}','{self.description}','{self.date_of_event}')"

class e_registration(db.Model):
    register_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id=db.Column(db.Integer,db.ForeignKey('events.eid'), nullable=False)
    stu_id=db.Column(db.Integer,db.ForeignKey('student.sid'), nullable=False)

    def __repr__(self):
        return f"e_registration('{self.register_id}','{self.event_id}','{self.stu_id}')"

class Fees(db.Model):
    f_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount=db.Column(db.Integer, nullable=False)
    last_paid=db.Column(db.DateTime, nullable=False, default=datetime.now)
    status=db.Column(db.String(15), nullable=False)
    stu_id=db.Column(db.Integer,db.ForeignKey('student.sid'), nullable=False)

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
    currentDate = datetime.now()
    # print(AllEvent)
    return render_template('ViewEvents.html',Events=AllEvent,today=currentDate)

@app.route('/admin/Events',methods=['GET'])
def AdminViEvents():
    AllEvent = Events.query.all()
    currentDate = datetime.now()
    # print(AllEvent)
    return render_template('adminViEvents.html',Events=AllEvent,today=currentDate)

#testing route
@app.route("/login")
def login():
    # db.session.query(Student).delete()
    # db.session.commit()
    print("sss")
    st = Studentrecords(Name='s1khavdk')
    db.session.add(st)
    db.session.commit()
    print("sss")
    print(StudentRecords.query.all())
    
    return redirect(url_for('RegisterEvents'))

@app.route("/Student/EventIdUpdate",methods=['GET'])
def EventIdUpdate():
    EventId = request.args.get('Eid')
    print(EventId)
    return redirect(url_for('addEvent'))
     

@app.route("/admin/addEvent",methods=['GET','POST'])
def addEvent():
    form = EventForm()
    print(form.data['EventName'])
    if form.validate_on_submit():
        Event = Events(e_name=form.data['EventName'],description=form.data['EventDescription'],date_of_event=form.data['EventDate'])
        db.session.add(Event)
        db.session.commit()
        # print(Events.query.all())
        flash(f'New Event is created','success')
        # print(form)
        return redirect(url_for('admin'))
        # print("sss")
    return render_template('addEvent.html',form=form)




if __name__ == '__main__':
    app.run(debug=True)