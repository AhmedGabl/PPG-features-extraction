import numpy as np
import scipy.signal as signal

# Load the PPG data from a text file
filename = 'Recorded_ppg/S2.txt'
delimiter = ','  # Specify the delimiter used in the file
ppg_signal = np.loadtxt(filename, delimiter=delimiter)

# Set the sampling frequency (in Hz)
fs = 120
#1000

# Filter the signal to remove noise and baseline wander
fc_lp = 10  # low-pass cutoff frequency (in Hz)
fc_hp = 0.5  # high-pass cutoff frequency (in Hz)
b_lp, a_lp = signal.butter(2, fc_lp / (fs / 2), 'low')  # design a 2nd-order low-pass Butterworth filter
b_hp, a_hp = signal.butter(2, fc_hp / (fs / 2), 'high')  # design a 2nd-order high-pass Butterworth filter
ppg_filtered = signal.filtfilt(b_lp, a_lp, signal.filtfilt(b_hp, a_hp, ppg_signal))

# Compute the first derivative of the PPG signal to detect the peaks
ppg_diff = np.diff(ppg_filtered)

# Find the peak locations (i.e., systolic peaks)
peak_locs, _ = signal.find_peaks(ppg_diff, height=0.1*np.std(ppg_diff), distance=0.6*fs)

# Compute the inter-peak intervals (IPIs) and heartrate variability (HRV)
IPIs = np.diff(peak_locs) / fs
HR = 60 / IPIs  # compute heart rate (HR) in bpm
## Filter the heart rate to remove outliers or erroneous values
#HR = signal.medfilt(HR, kernel_size=5)  # Apply median filtering with a suitable kernel size
HR_avg = np.mean(HR)  # Compute the average heart rate (HR_avg)

# Compute the pulse transit time (PTT)
PTT = (peak_locs[-1] - peak_locs[0]) / fs

# Compute the blood pressure (BP) estimate using the PTT method
SBP = 0.9 * PTT + 117
DBP = -0.6 * PTT + 80

# Compute the ratio of red and infrared PPG signals 
#assuming this is a combined ppg with red light like the one from max30100 
#O.W just put on a normal value (as it will be needed later )
R = ppg_filtered[::2]
IR = ppg_filtered[1::2]
R_mean = np.mean(R)
IR_mean = np.mean(IR)
ratio = R_mean / IR_mean

# Compute SpO2 using the Beer-Lambert law
SpO2 = -15 * ratio + 110

# Print the feature values
print(f'HR_avg = {HR_avg:.2f} bpm')
print(f'SBP = {SBP:.2f} mmHg')
print(f'DBP = {DBP:.2f} mmHg')
print(f'SpO2 = {SpO2:.2f}%')
