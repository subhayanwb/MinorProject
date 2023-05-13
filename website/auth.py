from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from .models import User, UserPersonalInfo, CollegeMaster, QualificationMaster, UserEducationInfo, UserExperienceInfo, UserCertificateInfo
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import os
from resume_parser import resumeparse
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.registrationCompleted != 'Y':
                    flash('Your Registration has not completed yet. Please fill in this form to complete Registration.',
                          category='error')
                    return redirect(url_for('auth.register'))
                else:
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exists. Please Sign Up to gain access to this site.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('psw-repeat')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 2:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'),
                            role='User', registrationCompleted='N')
            db.session.add(new_user)
            db.session.commit()
            created_user = User.query.filter_by(email=email).first()
            login_user(created_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.register'))

    return render_template("signup.html", user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        new_user_personal_info = UserPersonalInfo(userid=form.userid.data, firstname=form.firstname.data,
                                                  lastname=form.lastname.data, dob=form.dob.data,
                                                  contactnumber=form.contactnumber.data, city=form.city.data,
                                                  state=form.state.data, country=form.country.data, pin=form.pin.data,
                                                  gender=form.gender.data)
        new_user_education_info = UserEducationInfo(userid=form.userid.data, qualification=form.qualification.data,
                                                  college=form.institute.data,
                                                  yearofcompletion=form.yearofcompletion.data,
                                                  grade=form.grade.data, rating=form.rating.data)
        new_user_experience_info = UserExperienceInfo(userid=form.userid.data, organization=form.organization.data,
                                                    started=form.started.data,
                                                    ended=form.ended.data,
                                                    designation=form.designation.data,
                                                      skills=form.skills.data)
        new_user_certificate_info = UserCertificateInfo(userid=form.userid.data,
                                                        certificatename=form.certificatename.data,
                                                        duration=form.duration.data,
                                                        completionyear=form.completionyear.data)
        db.session.merge(new_user_personal_info)
        db.session.merge(new_user_education_info)
        db.session.merge(new_user_experience_info)
        db.session.merge(new_user_certificate_info)
        user = User.query.filter_by(userId=current_user.userId).first()
        user.registrationCompleted = 'Y'
        db.session.merge(user)
        db.session.commit()
        flash('Data successfully saved!', category='success')
        return redirect(url_for('auth.register'))
    else:
        listofcolleges = CollegeMaster.query.all()
        listofqualification = QualificationMaster.query.order_by(QualificationMaster.qualificationname).all()

        userPersonalInfo = UserPersonalInfo.query.filter_by(userid=current_user.userId).first()
        userEducationInfo = UserEducationInfo.query.filter_by(userid=current_user.userId).first()
        userExperienceInfo = UserExperienceInfo.query.filter_by(userid=current_user.userId).first()
        userCertificateInfo = UserCertificateInfo.query.filter_by(userid=current_user.userId).first()

        form = RegistrationForm()
        if None != userPersonalInfo:
            form.firstname = userPersonalInfo.firstname
            form.lastname = userPersonalInfo.lastname
            form.dob = userPersonalInfo.dob
            form.contactnumber = userPersonalInfo.contactnumber
            form.city = userPersonalInfo.city
            form.state = userPersonalInfo.state
            form.country = userPersonalInfo.country
            form.pin = userPersonalInfo.pin
            form.gender = userPersonalInfo.gender

        else:
            form.firstname = ""
            form.lastname = ""
            form.dob = ""
            form.contactnumber = ""
            form.city = ""
            form.state = ""
            form.country = ""
            form.pin = ""
            form.gender = ""

        if None != userEducationInfo:
            form.qualification = userEducationInfo.qualification
            form.institute = userEducationInfo.college
            form.yearofcompletion = userEducationInfo.yearofcompletion
            form.grade = userEducationInfo.grade
            form.rating = userEducationInfo.rating
        else:
            form.qualification = ""
            form.institute = ""
            form.yearofcompletion = ""
            form.grade = ""
            form.rating = ""

        if None != userExperienceInfo:
            form.organization = userExperienceInfo.organization
            form.started = userExperienceInfo.started
            form.ended = userExperienceInfo.ended
            form.designation = userExperienceInfo.designation
            form.skills = userExperienceInfo.skills
        else:
            form.organization = ""
            form.started = ""
            form.ended = ""
            form.designation = ""
            form.skills = ""

        if None != userCertificateInfo:
            form.certificatename = userCertificateInfo.certificatename
            form.duration = userCertificateInfo.duration
            form.completionyear = userCertificateInfo.completionyear
        else:
            form.certificatename = ""
            form.duration = ""
            form.completionyear = ""
        return render_template("registration.html", user=current_user, RegistrationForm=form
                               , listofcolleges=listofcolleges, listofqualification=listofqualification)


class RegistrationForm(Form):
    userid = StringField('userid')
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    dob = StringField('dob')
    contactnumber = StringField('contactnumber')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    pin = StringField('pin')
    gender = StringField('gender')

    qualification = StringField('qualification')
    institute = StringField('institute')
    yearofcompletion = StringField('yearofcompletion')
    grade = StringField('grade')
    rating = StringField('rating')

    organization = StringField('organization')
    started = StringField('started')
    ended = StringField('ended')
    designation = StringField('designation')
    skills = StringField('skills')

    certificatename = StringField('certificatename')
    duration = StringField('duration')
    completionyear = StringField('completionyear')


@auth.route('/uploadfile', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':
        f = request.files['filename']
        f.save(secure_filename(f.filename))

        data = resumeparse.read_file(f.filename)

        form = RegistrationForm()

        if(data['name']) != None:
            if data['name'].split()[0] != None:
                form.firstname = data['name'].split()[0]
            else:
                form.firstname = ""
        else:
            form.firstname = ""
        if (data['name']) != None:
            if data['name'].split()[1] != None:
                form.lastname = data['name'].split()[1]
            else:
                form.lastname = ""
        else:
            form.lastname = ""

        if data['phone'] != None:
            form.contactnumber = data['phone']
        else:
            form.contactnumber = ""
        form.dob = ""
        form.city = ""
        form.state = ""
        form.country = ""
        form.pin = ""
        form.gender = ""

        if data['degree'] != None:
            degree = ', '.join(data['degree'])
            form.qualification = degree
        else:
            form.qualification = ""
        if data['university'] != None:
            institute = ', '.join(data['university'])
            form.institute = institute
        else:
            form.institute = ""
        form.yearofcompletion = ""
        form.grade = ""
        form.rating = ""

        if data['Companies worked at'] != None:
            organization = ', '.join(data['Companies worked at'])
            form.organization = organization
        else:
            form.organization = ""
        if data['designition'] != None:
            designation = ', '.join(data['designition'])
            form.designation = designation
        else:
            form.designation = ""
        if data['skills'] != None:
            skills = ', '.join(data['skills'])
            form.skills = skills
        else:
            form.skills = ""
        form.started = ""
        form.ended = ""

        form.certificatename = ""
        form.duration = ""
        form.completionyear = ""

        flash(data, category='success')
        flash('File Upload Successfull!', category='success')
        return render_template("registration.html", user=current_user, data=data, RegistrationForm=form)