import numpy as np


data_path = "../data/EmotionECG"

def read_emotion_data():

    labeldata = np.loadtxt(f"{data_path}/label_2.csv", delimiter=',')
    arousalLabel = labeldata[:,2].astype(np.int32)
    valenceLable = labeldata[:,3].astype(np.int32)
    path=labeldata[:,[0,1]].astype(np.int32)

    ECGdata=[]
    for i in range(len(path)):
        data=np.loadtxt(f"{data_path}/EXG3_{path[i,0]}_{path[i,1]}.csv", delimiter=',')
        data=data[3:].astype(np.float64)
        ECGdata.append(data)

    return ECGdata, arousalLabel,valenceLable



