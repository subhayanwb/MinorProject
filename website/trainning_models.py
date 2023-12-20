import pandas as pd
import numpy as np
import pickle

from sklearn.metrics import accuracy_score


def initialize():
    global X_train, X_test, y_train, y_test

    career = pd.read_csv('website/testdata.data', header = None)

    X = np.array(career.iloc[:, 0:17]) #X is skills
    y = np.array(career.iloc[:, 17]) #Y is Roles

    ##  attribute to return the column labels of the given Dataframe
    career.columns = ["Database Fundamentals","Computer Architecture","Distributed Computing Systems",
    "Cyber Security","Networking","Development","Programming Skills","Project Management",
    "Computer Forensics Fundamentals","Technical Communication","AI ML","Software Engineering","Business Analysis",
    "Communication skills","Data Science","Troubleshooting skills","Graphics Designing","Roles"]

    career.dropna(how ='all', inplace = True)
    career.head()
    ## splitting the data into training and test sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.3, random_state = 524)

initialize()

def svm_implementation():
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score

    model=SVC(probability=True)
    model.probability=True
    model.fit(X_train, y_train)
    model.kernel

    y_pred=model.predict(X_test)
    acc=accuracy_score(y_test,y_pred)

    pickle.dump(model, open('SVM.pkl','wb'))
    print('Trained Model saved in SVM.pkl')

    return acc*100

def knn_implementation():
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn import metrics
    scores = {}
    knn = KNeighborsClassifier(n_neighbors=5)

    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    scores[5] = metrics.accuracy_score(y_test, y_pred)

    pickle.dump(knn, open('KNN.pkl', 'wb'))
    print('Trained Model saved in KNN.pkl')
    return scores[5] * 100

def ensemble_voting_implementation():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import VotingClassifier
    from sklearn import metrics
    from sklearn.tree import DecisionTreeClassifier
    scores = {}

    # initializing all the model objects with default parameters
    model_1 = LogisticRegression()
    model_2 = DecisionTreeClassifier()
    model_3 = RandomForestClassifier()

    # Making the final model using voting classifier
    final_model = VotingClassifier(estimators=[('lr', model_1), ('dt', model_2), ('rf', model_3)], voting='soft')

    # training all the model on the train dataset
    final_model.fit(X_train, y_train)

    # predicting the output on the test dataset
    y_pred = final_model.predict(X_test)
    scores[5] = metrics.accuracy_score(y_test, y_pred)

    pickle.dump(final_model, open('ENSEMBLE_VOTING.pkl', 'wb'))
    print('Trained Model saved in ENSEMBLE_VOTING.pkl')

    return scores[5] * 100


def ensemble_bagging_implementation():
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    from sklearn.ensemble import BaggingClassifier

    estimator_range = [2, 4, 6, 8, 10, 12, 14, 16]

    models = []
    scores = []

    for n_estimators in estimator_range:
        # Create bagging classifier
        clf = BaggingClassifier(n_estimators=n_estimators, random_state=5)

        # Fit the model
        clf.fit(X_train, y_train)

        # Append the model and score to their respective list
        models.append(clf)
        scores.append(accuracy_score(y_true=y_test, y_pred=clf.predict(X_test)))
        accuracy = sum(scores) / len(scores)
    # Generate the plot of scores against number of estimators
    plt.figure(figsize=(9, 6))
    plt.plot(estimator_range, scores)

    # Adjust labels and font (to make visable)
    plt.xlabel("n_estimators", fontsize=18)
    plt.ylabel("score", fontsize=18)
    plt.tick_params(labelsize=16)

    # Visualize plot
    #plt.show()

    pickle.dump(clf, open('ENSEMBLE_BAGGING.pkl', 'wb'))
    print('Trained Model saved in ENSEMBLE_BAGGING.pkl')

    return accuracy*100