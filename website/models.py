from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'user_login_info'
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(250))
    role = db.Column(db.String(20))
    registrationCompleted = db.Column(db.String(1))

    def get_id(self):
        return (self.userId)


class UserPersonalInfo(db.Model):
    __tablename__ = 'user_personal_info'
    firstname = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    dob = db.Column(db.DateTime(timezone=True))
    contactnumber = db.Column(db.String(20))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    country = db.Column(db.String(45))
    pin = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    userid = db.Column(db.Integer, db.ForeignKey('user_login_info.userId'), primary_key=True)


class UserEducationInfo(db.Model):
    __tablename__ = 'user_education_info'
    qualification = db.Column(db.String(250))
    college = db.Column(db.String(250))
    yearofcompletion = db.Column(db.Integer)
    grade = db.Column(db.String(10))
    rating = db.Column(db.String(10))
    userid = db.Column(db.Integer, db.ForeignKey('user_login_info.userId'), primary_key=True)


class UserExperienceInfo(db.Model):
    __tablename__ = 'user_experience_info'
    organization = db.Column(db.String(200))
    started = db.Column(db.String(45))
    ended = db.Column(db.String(45))
    designation = db.Column(db.String(200))
    skills = db.Column(db.String(1000))
    userid = db.Column(db.Integer, db.ForeignKey('user_login_info.userId'), primary_key=True)


class UserCertificateInfo(db.Model):
    __tablename__ = 'user_certificate_info'
    certificatename = db.Column(db.String(200))
    duration = db.Column(db.String(45))
    completionyear = db.Column(db.String(45))
    userid = db.Column(db.Integer, db.ForeignKey('user_login_info.userId'), primary_key=True)


class CollegeMaster(db.Model):
    __tablename__ = 'college_master'
    collegeid = db.Column(db.Integer, primary_key=True)
    collegename = db.Column(db.String(200))


class QualificationMaster(db.Model):
    __tablename__ = 'qualification_master'
    qualificationid = db.Column(db.Integer, primary_key=True)
    qualificationname = db.Column(db.String(200))