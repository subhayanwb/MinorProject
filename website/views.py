import os
import pickle
from . import trainning_models

import numpy as np
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

from .auth import RegistrationForm
from .models import UserPersonalInfo, UserEducationInfo, UserExperienceInfo, UserCertificateInfo

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET'])
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
        i = 0
        res = result.to_dict(flat=True)
        print(res)
        option_dict = {'1': 'Not Interested',
                       '2': 'Poor',
                       '3': 'Beginning',
                       '4': 'Below Average',
                       '5': 'Average',
                       '6': 'Above Average',
                       '7': 'Intermediate',
                       '8': 'Excellent',
                       '9': 'Professional'}

        input_data={}
        for key, value in res.items():
            input_data[key.replace("rate_", "")] = option_dict[value]

        arr1 = res.values()
        arr = ([value for value in arr1])
        data = np.array(arr, dtype=float)
        data = data.reshape(1, -1)

        #knn_accuracy = trainning_models.knn_implementation()
        #knn_accuracy=round(knn_accuracy, 4)
        knn_accuracy = '96.2598%'
        print('KNN ACCURACY = ', knn_accuracy)

        #svm_accuracy = trainning_models.svm_implementation()
        #svm_accuracy = round(svm_accuracy, 4)
        svm_accuracy = '97.1457%'
        print('SVM ACCURACY=', svm_accuracy)

        #voting_accuracy = trainning_models.ensemble_voting_implementation()
        #voting_accuracy = round(voting_accuracy, 4)
        voting_accuracy = '99.2782%'
        print('Voting ACCURACY=', voting_accuracy)

        #bagging_accuracy = trainning_models.ensemble_bagging_implementation()
        #bagging_accuracy = round(bagging_accuracy, 4)
        bagging_accuracy = '99.2249%'
        print('Bagging ACCURACY=', bagging_accuracy)

        knn_finalResults = findPredictions('KNN', data)
        svm_finalResults = findPredictionsWithoutProb('SVM', data)
        voting_finalResults = findPredictionsWithoutProb('VOTING', data)
        bagging_finalResults = findPredictions('BAGGING', data)

        userPersonalInfo = UserPersonalInfo.query.filter_by(userid=current_user.userId).first()
    return render_template("prediction.html", user=current_user, knn_finalResults=knn_finalResults, svm_finalResults=svm_finalResults, voting_finalResults=voting_finalResults, bagging_finalResults=bagging_finalResults, userPersonalInfo=userPersonalInfo, knn_accuracy=knn_accuracy, svm_accuracy=svm_accuracy, voting_accuracy=voting_accuracy, bagging_accuracy=bagging_accuracy, input_data=input_data)

def findPredictions(model_type, data):
    print(model_type)

    # filenamelst_abspathname = os.path.abspath('./website/ENSEMBLE_BAGGING.pkl')
    if model_type=='KNN':
        loaded_model = pickle.load(open('./website/KNN.pkl', 'rb'))
    elif model_type=='BAGGING':
        loaded_model = pickle.load(open('./website/ENSEMBLE_BAGGING.pkl', 'rb'))

    predictions = loaded_model.predict(data)
    print('Predictions = ', predictions)
    pred = loaded_model.predict_proba(data)
    pred = pred > 0.05
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
    index = 0
    for key, values in res.items():
        # if values != predictions[0]:
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

    finalList = {predictions[0]}
    i=0
    for key, value in final_res.items():
        if i<3:
            finalList.add(jobs_dict[value])
            i = i + 1

    print(finalList)
    return  finalList

def findPredictionsWithoutProb(model_type, data):
    print(model_type)

    # filenamelst_abspathname = os.path.abspath('./website/ENSEMBLE_BAGGING.pkl')
    if model_type=='SVM':
        loaded_model = pickle.load(open('./website/SVM.pkl', 'rb'))
    elif model_type == 'VOTING':
        loaded_model = pickle.load(open('./website/ENSEMBLE_VOTING.pkl', 'rb'))

    predictions = loaded_model.predict(data)
    print('Predictions = ', predictions)
    finalList = {predictions[0]}
    print(finalList)

    return  finalList