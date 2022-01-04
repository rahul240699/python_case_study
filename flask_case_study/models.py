from datetime import datetime
from flask_case_study import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

class User(db.Model, UserMixin):
    email=db.Column(db.String(120), primary_key=True, nullable=False)
    username=db.Column(db.String(20), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)
    user_type=db.Column(db.String(20), nullable=False)
    students=db.relationship('Student', backref='is_student',lazy=True)
    
    def get_id(self):
           return (self.email)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.user_type}')"

class Student(db.Model):
    sid=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name=db.Column(db.String(30), nullable=False)
    FName=db.Column(db.String(30), nullable=False)
    MName=db.Column(db.String(30), nullable=False)
    address=db.Column(db.Text, nullable=False)
    cid=db.Column(db.String(10), db.ForeignKey('class_.c_id'),nullable=False)
    phone=db.Column(db.String(11),nullable=False)
    p_email=db.Column(db.String(30))
    image_file=db.Column(db.String(20),nullable=False, default='default.jpg')
    user_email=db.Column(db.String(120),db.ForeignKey('user.email'), nullable=False)
    participation=db.relationship('E_registration',backref='taken_part',lazy=True)
    Fees=db.relationship('Fees',backref='Fee_Payment',lazy=True)

    def __repr__(self):
        return f"Student('{self.sid}','{self.Name}','{self.cid}','{self.user_email}')"

class Events(db.Model):
    eid=db.Column(db.Integer, primary_key=True, autoincrement=True)
    e_name=db.Column(db.String(30), nullable=False)
    description=db.Column(db.Text, nullable=False)
    date_of_event=db.Column(db.DateTime, nullable=False)
    participants=db.relationship('E_registration',backref='part_taken',lazy=True)
    
    
    def __repr__(self):
        return f"Events('{self.eid}','{self.e_name}','{self.date_of_event}')"

class E_registration(db.Model):
    register_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id=db.Column(db.Integer,db.ForeignKey('events.eid'), nullable=False)
    stu_id=db.Column(db.Integer,db.ForeignKey('student.sid'), nullable=False)

    def __repr__(self):
        return f"E_registration('{self.register_id}','{self.event_id}','{self.stu_id}')"

class Fees(db.Model):
    f_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid=db.Column(db.Integer,db.ForeignKey('class_.c_id'), nullable=False)
    amount=db.Column(db.Integer, nullable=False)
    Due_date=db.Column(db.String(30), nullable=False)
    status=db.Column(db.String(15), nullable=False)
    stu_id=db.Column(db.Integer,db.ForeignKey('student.sid'), nullable=False)

    def __repr__(self):
        return f"Fees('{self.f_id}','{self.cid}','{self.stu_id}',,'{self.amount}','{self.Due_date}','{self.status}')"
    

class Class_(db.Model):
    c_id=db.Column(db.String(10),primary_key=True)
    fee_amt=db.Column(db.Integer)
    in_class=db.relationship('Student',backref='Student_class',lazy=True)
    fee=db.relationship('Fees',backref='Student_Fees',lazy=True)

    def __repr__(self):
        return f"Class_('{self.c_id}','{self.fee_amt}')"