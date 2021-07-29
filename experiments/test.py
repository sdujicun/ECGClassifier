import numpy as np
import os
import csv
import time
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from steps.data_import import read_emotion_data
from steps.preprocessing import preprocessing
from steps.peak_detection import peak_detection,HRV_detection
from sklearn.model_selection import train_test_split


from shapelet.shapelet_transform import Shapelet,findBestKShapelet,findBestKShapeletWithSplitPoints,transform

pwd = os.getcwd()
father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
path = father_path + "/results/result.csv"


def classification():
    ECGdata, arousalLabel, valenceLable = read_emotion_data()
    ecg=preprocessing(ECGdata,sample_fs=256,method='nk')
    #Peaks_R, Length_R, Peaks_T, Length_T, Peaks_P, Length_P=peak_detection(ecg, sample_fs=256,method='nk')
    #X_train, X_test, arousal_train, arousal_test, valence_train, valence_test=train_test_split(Peaks_R,arousalLabel,valenceLable)
    HRV=HRV_detection(ecg, sample_fs=256,method='nk')

    X_train, X_test, arousal_train, arousal_test, valence_train, valence_test=train_test_split(HRV,arousalLabel,valenceLable,test_size=0.2)

    start = time.time()
    kShapelet=findBestKShapeletWithSplitPoints(X_train,arousal_train,5,20,25)
    end = time.time()
    print("运行时间",end-start)
    print("finally shapelet------------------------------------")
    for i in range(len(kShapelet)):
        shapelet=kShapelet[i]
        print(shapelet.seriesId,'\t',shapelet.startPos,'\t',shapelet.length,'\t',shapelet.values,'\t',shapelet.threshold,'\t',shapelet.gain,'\t',shapelet.gap)

    print(len(kShapelet))

    X_train_trans=transform(X_train,kShapelet)
    X_test_trans=transform(X_test,kShapelet)

    classifier0= KNN(n_neighbors =1)
    classifier0.fit(X_train_trans,arousal_train)
    yhat_test=classifier0.predict(X_test_trans)
    acc=accuracy_score(arousal_test,yhat_test)
    print("KNN准确率", acc)


    classifier1=SVC(kernel='rbf')
    classifier1.fit(X_train_trans,arousal_train)
    yhat_test=classifier1.predict(X_test_trans)
    acc=accuracy_score(arousal_test,yhat_test)
    print("SVM准确率", acc)

    classifier2 = RandomForestClassifier()
    classifier2.fit(X_train_trans,arousal_train)
    yhat_test=classifier2.predict(X_test_trans)
    acc=accuracy_score(arousal_test,yhat_test)
    print("随机准确率", acc)



if __name__ == '__main__':

    classification()