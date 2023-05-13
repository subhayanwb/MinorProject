import os
import pickle

import numpy as np
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

from .auth import RegistrationForm
from .models import UserPersonalInfo, UserEducationInfo, UserExperienceInfo, UserCertificateInfo

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
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
    return render_template("home.html", user=current_user, RegistrationForm=form)


@views.route('/rateyourself', methods=['GET'])
@login_required
def rateyourself():
    return render_template("index.html", user=current_user)



@views.route('/predict', methods=['GET','POST'])
@login_required
def predict():
    if request.method == 'POST':
        result = request.form
        #flash(result, category="success")
        i = 0
        print(result)
        res = result.to_dict(flat=True)
        print("res:", res)
        arr1 = res.values()
        arr = ([value for value in arr1])

        data = np.array(arr, dtype=float)

        data = data.reshape(1, -1)
        print(data)
        filenamelst_abspathname = os.path.abspath('./website/careerlast.pkl')
        print(filenamelst_abspathname)
        loaded_model = pickle.load(open('./website/careerlast.pkl', 'rb'))
        predictions = loaded_model.predict(data)
        # return render_template('testafter.html',a=predictions)

        print(predictions)
        pred = loaded_model.predict_proba(data)
        print(pred)
        # acc=accuracy_score(pred,)
        pred = pred > 0.05
        # print(predictions)
        i = 0
        j = 0
        index = 0
        res = {}
        final_res = {}
        while j < 17:
            if pred[i, j]:
                res[index] = j
                index += 1
            j += 1
        # print(j)
        # print(res)
        index = 0
        for key, values in res.items():
            if values != predictions[0]:
                final_res[index] = values
                print('final_res[index]:', final_res[index])
                index += 1
        # print(final_res)
        jobs_dict = {0: 'AI ML Specialist',
                     1: 'API Integration Specialist',
                     2: 'Application Support Engineer',
                     3: 'Business Analyst',
                     4: 'Customer Service Executive',
                     5: 'Cyber Security Specialist',
                     6: 'Data Scientist',
                     7: 'Database Administrator',
                     8: 'Graphics Designer',
                     9: 'Hardware Engineer',
                     10: 'Helpdesk Engineer',
                     11: 'Information Security Specialist',
                     12: 'Networking Engineer',
                     13: 'Project Manager',
                     14: 'Software Developer',
                     15: 'Software Tester',
                     16: 'Technical Writer'}

        # print(jobs_dict[predictions[0]])
        job = {}
        # job[0] = jobs_dict[predictions[0]]
        index = 1

        data1 = predictions[0]
        print(data1)
        #return render_template("testafter.html", final_res=final_res, job_dict=jobs_dict, job0=data1)
        userPersonalInfo = UserPersonalInfo.query.filter_by(userid=current_user.userId).first()
    return render_template("prediction.html", user=current_user, final_res=final_res, job_dict=jobs_dict, job0=data1, userPersonalInfo=userPersonalInfo)