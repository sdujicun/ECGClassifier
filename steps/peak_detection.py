import neurokit2 as nk
import matplotlib.pyplot as plt
import numpy as np

def HRV_detection(ecg, sample_fs=256,method='nk'):
    HRV=[]
    for i in range(len(ecg)):
        data=ecg[i]

        signal, rpeaks = nk.ecg_peaks(data, sampling_rate=sample_fs,method=method)

        r_peaks= np.array(rpeaks['ECG_R_Peaks'])

        rr=np.diff(r_peaks)/sample_fs * 1000

        HRV.append(rr)

    return HRV

def peak_detection(ecg, sample_fs=256,method='nk'):
    Peaks_R=[]
    Length_R=[]
    Peaks_T=[]
    Length_T=[]
    Peaks_P=[]
    Length_P=[]

    for i in range(len(ecg)):
        data=ecg[i]

        signal, rpeaks = nk.ecg_peaks(data, sampling_rate=sample_fs,method=method)
        _, waves_peak = nk.ecg_delineate(data, rpeaks, sampling_rate=sample_fs, method="dwt")

        r_peaks= np.array(rpeaks['ECG_R_Peaks'])
        r_onsets=np.array(waves_peak['ECG_R_Onsets'])
        r_offsets=np.array(waves_peak['ECG_R_Offsets'])
        r_wave_length=(r_offsets-r_onsets)/sample_fs * 1000
        r_wave_length=r_wave_length[~np.isnan(r_wave_length)]
        r_peaks=r_peaks[~np.isnan(r_peaks)]
        Peaks_R.append(r_peaks)
        Length_R.append(r_wave_length)


        t_peaks=np.array(waves_peak['ECG_T_Peaks'])
        t_onsets=np.array(waves_peak['ECG_T_Onsets'])
        t_offsets=np.array(waves_peak['ECG_T_Offsets'])
        t_wave_length =(t_offsets-t_onsets)/sample_fs * 1000
        t_wave_length=t_wave_length[~np.isnan(t_wave_length)]
        t_peaks=t_peaks[~np.isnan(t_peaks)]
        Peaks_T.append(t_peaks)
        Length_T.append(t_wave_length)

        p_peaks=np.array(waves_peak['ECG_P_Peaks'])
        p_onsets=np.array(waves_peak['ECG_P_Onsets'])
        p_offsets=np.array(waves_peak['ECG_P_Offsets'])
        p_wave_length=(p_offsets-p_onsets)/sample_fs * 1000
        p_wave_length=p_wave_length[~np.isnan(p_wave_length)]
        p_peaks=p_peaks[~np.isnan(p_peaks)]

        Peaks_P.append(p_peaks)
        Length_P.append(p_wave_length)

    return Peaks_R, Length_R, Peaks_T, Length_T, Peaks_P, Length_P

    #return np.array(Peaks_R), np.array(Length_R), np.array(Peaks_T), np.array(Length_T), np.array(Peaks_P), np.array(Length_P)













