from flask_case_study.models import Student, Fees, Class_
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_case_study import db

def queryFeesAdmin(classData):
    fees = Fees.query.filter_by(status='Pending',cid=classData).all()
    data = []
    for fee in fees:
        dic = {}
        details = Student.query.filter_by(sid=fee.stu_id).first()

        dic['Sid'] = details.sid
        dic['Name'] = details.Name
        dic['Class'] = details.cid
        dic['amt'] = fee.amount
        dic['due_date'] = fee.Due_date
        dic['status'] = fee.status
        data.append(dic)

    return data

def queryFeesStudent(userVal):
    studentDetails = Student.query.filter_by(user_email=userVal).first()
    data = []
    fees = Fees.query.filter_by(stu_id=studentDetails.sid).all()
    for fee in fees:
        dic = {}
        details = Student.query.filter_by(sid=fee.stu_id).first()
        dic['Sid'] = fee.stu_id
        dic['Name'] = details.Name
        dic['Class'] = details.cid
        dic['amt'] = fee.amount
        dic['due_date'] = fee.Due_date
        dic['status'] = fee.status
        data.append(dic)
    
    return data

def updateFeesStudent(userVal):
    studentDetails = Student.query.filter_by(user_email=userVal).first()
    print(studentDetails)
    fees = Fees.query.filter_by(stu_id=studentDetails.sid).all()
    print(fees)
    for fee in fees:
        due_date = fee.Due_date
        print(due_date)
        dateobj = datetime.strptime(due_date,"%Y-%m-%d")
        dateobj = dateobj+relativedelta(months=1)
        print(datetime.strftime(dateobj,"%Y-%m-%d"))
        fee.Due_date = datetime.strftime(dateobj,"%Y-%m-%d")
        fee.status = "Paid"
        db.session.add(fee)
        db.session.commit()
    return