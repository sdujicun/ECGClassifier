import heartpy as hp
import neurokit2 as nk
from scipy.signal import savgol_filter

import matplotlib.pyplot as plt

def preprocessing(ECGdata,sample_fs=256,method='nk'):
    ecg=[]
    for i in range(len(ECGdata)):
        #plt.plot(ECGdata[i][0:1024])
        #plt.show()

        #remove_baseline_wander
        ecg_clean=hp.remove_baseline_wander(ECGdata[i],sample_fs)
        #nk_filter
        ecg_clean=nk.ecg_clean(ecg_clean,sampling_rate=sample_fs,method=method)
        #smoothing
        ecg_clean=savgol_filter(ecg_clean,9,3,mode='nearest')
        #plt.plot(ecg_clean[0:1024])
        #plt.show()
        #ecg_clean=ecg_clean[256:]
        ecg.append(ecg_clean)
    return ecg
