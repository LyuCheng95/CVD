import pandas as pd
import numpy as np

filename = "cardio_1dp.csv"

data = pd.read_csv(filename)
data.iloc[:,-1] = [1 if i>0.5 else 0 for i in data.iloc[:,-1]]

filename = "cardio_1dp_result.txt"

X = data.iloc[:,:-1]
y = data.iloc[:,-1]

from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
kfold = StratifiedKFold(n_splits = 10, shuffle = True, random_state = 2019)

#C for regularization
C = [0.001,0.01,0.1,1,10,100,1000,10000]

#SUPPORT VECTOR MACHINE
svm_score = []
svm_recall = []
svm_precision = []
svm_fl_score = []

from sklearn.svm import SVC

for i in C:
    
    svm_c_score = []
    svm_c_recall = []
    svm_c_precision = []
    svm_c_fl_score = []
    
    for train_index, test_index in kfold.split(X, y):
    
        X_train = X.iloc[train_index][:1000]
        y_train = y.iloc[train_index][:1000]
        X_test = X.iloc[test_index]
        y_test = y.iloc[test_index]
    
        classifier = SVC(kernel='rbf', C=i, decision_function_shape='ovr', gamma="scale")
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        
        svm_c_score.append(classifier.score(X_test, y_test))
        svm_c_recall.append(metrics.recall_score(y_test, y_pred))
        svm_c_precision.append(metrics.precision_score(y_test, y_pred))
        svm_c_fl_score.append(metrics.f1_score(y_test, y_pred))
        
    svm_score.append(np.mean(svm_c_score))
    svm_recall.append(np.mean(svm_c_recall))
    svm_precision.append(np.mean(svm_c_precision))
    svm_fl_score.append(np.mean(svm_c_fl_score))

    
print("")
print("=================Results=================")
print("C=\t",C)
print("Score:\t",[str(round(i*100,2)) + "%" for i in svm_score])
print("Recall:\t",[str(round(i*100,2)) + "%" for i in svm_recall])
print("Presc:\t",[str(round(i*100,2)) + "%" for i in svm_precision])
print("F1:\t",[str(round(i*100,2)) + "%" for i in svm_fl_score])
print("")
best_index = np.argmax(svm_score)
print("Best C:",C[np.argmax(svm_score)])
print("Score:",round(svm_score[best_index]*100,2))
print("Recall:",round(svm_recall[best_index]*100,2))
print("Prec:",round(svm_precision[best_index]*100,2))
print("F1:",round(svm_fl_score[best_index]*100,2))

file = open(filename, "w")
file.writelines("===SVM===\n")
file.writelines("C=\t" + str(C) + "\n")
file.writelines("Score:\t" + str([str(round(i*100,2)) + "%" for i in svm_score])+"\n")
file.writelines("Recall:\t"+str([str(round(i*100,2)) + "%" for i in svm_recall])+"\n")
file.writelines("Presc:\t"+str([str(round(i*100,2)) + "%" for i in svm_precision])+"\n")
file.writelines("F1:\t"+str([str(round(i*100,2)) + "%" for i in svm_fl_score])+"\n")
file.writelines("Best C:" + str(C[np.argmax(svm_score)])+"\n")
file.writelines("Score:" + str(round(svm_score[best_index]*100,2))+"\n")
file.writelines("Recall:"+str(round(svm_recall[best_index]*100,2))+"\n")
file.writelines("Prec:"+str(round(svm_precision[best_index]*100,2))+"\n")
file.writelines("F1:"+str(round(svm_fl_score[best_index]*100,2))+"\n")
file.writelines("=========\n")
file.close()

#GAUSSIAN NAIVE BAYES
nb_score = []
nb_recall = []
nb_precision = []
nb_fl_score = []

from sklearn.naive_bayes import GaussianNB

for train_index, test_index in kfold.split(X, y):
    
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    
    nb_score.append(classifier.score(X_test, y_test))
    nb_recall.append(metrics.recall_score(y_test, y_pred))
    nb_precision.append(metrics.precision_score(y_test, y_pred))
    nb_fl_score.append(metrics.f1_score(y_test, y_pred))

print("")
print("=================Results=================")
print("Score:\t",np.mean(nb_score))
print("Recall:\t",np.mean(nb_recall))
print("Presc:\t",np.mean(nb_precision))
print("F1:\t",np.mean(nb_fl_score))

file = open(filename, "a")
file.writelines("===GaussianNB===\n")
file.writelines("Score:\t"+str(np.mean(nb_score)) + "\n")
file.writelines("Recall:\t"+str(np.mean(nb_recall))+ "\n")
file.writelines("Presc:\t"+str(np.mean(nb_precision))+ "\n")
file.writelines("F1:\t"+str(np.mean(nb_fl_score))+ "\n")
file.writelines("=========\n")
file.close()

#K NEAREST NEIGHBOUR

knn_score = []
knn_recall = []
knn_precision = []
knn_fl_score = []

from sklearn.neighbors import KNeighborsClassifier

for k in range(1, 101):
    
    print("Processing", k)
    classifier = KNeighborsClassifier(n_neighbors=k)
    
    knn_k_score = []
    knn_k_recall = []
    knn_k_precision = []
    knn_k_fl_score = []

    for train_index, test_index in kfold.split(X, y):
        
        X_train = X.iloc[train_index][:1000]
        y_train = y.iloc[train_index][:1000]
        X_test = X.iloc[test_index]
        y_test = y.iloc[test_index]
        
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        
        knn_k_score.append(classifier.score(X_test, y_test))
        knn_k_recall.append(metrics.recall_score(y_test, y_pred))
        knn_k_precision.append(metrics.precision_score(y_test, y_pred))
        knn_k_fl_score.append(metrics.f1_score(y_test, y_pred))
    
    knn_score.append(np.mean(knn_k_score))
    knn_recall.append(np.mean(knn_k_recall))
    knn_precision.append(np.mean(knn_k_precision))
    knn_fl_score.append(np.mean(knn_k_fl_score))

print("")
print("=================Results=================")
print("Score:\t",knn_score)
print("Recall:\t",knn_recall)
print("Presc:\t",knn_precision)
print("F1:\t",knn_fl_score)
print("")
best_index = np.argmax(knn_score)
print("Score:", knn_score[best_index])
print("Recall:", knn_recall[best_index])
print("Prec:", knn_precision[best_index])
print("F1:", knn_fl_score[best_index])

file = open(filename, "a")
file.writelines("===kNN===\n")
file.writelines("Score:\t"+str(knn_score[best_index]) + "\n")
file.writelines("Recall:\t"+str(knn_recall[best_index])+ "\n")
file.writelines("Presc:\t"+str(knn_precision[best_index])+ "\n")
file.writelines("F1:\t"+str(knn_fl_score[best_index])+ "\n")
file.writelines("=========\n")
file.close()