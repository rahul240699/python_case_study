from datetime import datetime
from flask_case_study import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)
    user_type=db.Column(db.String(20), nullable=False)
    students=db.relationship('Student', backref='is_student',lazy=True)
    
    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}','{self.user_type}')"

class Student(db.Model):
    sid=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name=db.Column(db.String(30), unique=True, nullable=False)
    FName=db.Column(db.String(30), unique=True, nullable=False)
    LName=db.Column(db.String(30), unique=True, nullable=False)
    address=db.Column(db.Text, nullable=False)
    class_=db.Column(db.String(10), nullable=False)
    phone=db.Column(db.String(11),nullable=False)
    image_file=db.Column(db.String(20),nullable=False, default='default.jpg')
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    participation=db.relationship('e_registration',backref='taken_part',lazy=True)
    Fees=db.relationship('Fees',backref='Fee_Payment',lazy=True)

    def __repr__(self):
        return f"Student('{self.sid}','{self.Name}','{self.class_}')"

class Events(db.Model):
    eid=db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_name=db.Column(db.String(30), nullable=False)
    description=db.Column(db.Text, nullable=False)
    date_of_event=db.Column(db.DateTime, nullable=False, default=datetime.now)
    participants=db.relationship('e_registration',backref='part_taken',lazy=True)
    
    
    def __repr__(self):
        return f"Events('{self.eid}','{self.e_name}','{self.date_of_event}')"

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
