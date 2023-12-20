import trainning_models

acc=trainning_models.svm_implementation()
print('ACCURACY=',round(acc, 4))

acc1=trainning_models.knn_implementation()
print('ACCURACY=',round(acc1, 4))

acc2=trainning_models.ensemble_voting_implementation()
print('ACCURACY=',round(acc2, 4))

acc3=trainning_models.ensemble_bagging_implementation()
print('ACCURACY=',round(acc3, 4))