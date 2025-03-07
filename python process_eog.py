import os
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

# 📂 Define the folder containing `.txt` EOG files
data_folder = r"C:\Users\Dell\OneDrive\Desktop\PYTHON\PROJECT"

# ✅ List all `.txt` files in the folder
file_list = [f for f in os.listdir(data_folder) if f.endswith(".txt")]

# ✅ Categorize files based on condition
normal_files = [f for f in file_list if "NORMAL" in f]
happy_files = [f for f in file_list if "HAPPY" in f]
stressed_files = [f for f in file_list if "STRESSED" in f]

print(f"✅ Found {len(normal_files)} Normal files")
print(f"✅ Found {len(happy_files)} Happy files")
print(f"✅ Found {len(stressed_files)} Stressed files")

# ✅ Define the required time limits (in seconds)
time_limits = {"NORMAL": 120, "HAPPY": 180, "STRESSED": 180}

# 🎯 **Low-Pass Filter (<30 Hz)**
def low_pass_filter(signal, sampling_rate=1000, cutoff_freq=30):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(4, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, signal)

# 🎯 **Read and Clean EOG Data**
def read_eog_file(file_path):
    try:
        # ✅ Read file, skipping metadata (first 27 rows)
        df = pd.read_csv(file_path, delimiter="\t", skiprows=27, header=None, 
                         names=["Time", "Channel3", "Channel4"], on_bad_lines='skip')
        
        # ✅ Convert to numeric and drop NaN values
        df = df.apply(pd.to_numeric, errors='coerce').dropna()

        # ✅ Convert time to seconds if necessary
        if df["Time"].max() > 10000:  # If time is in milliseconds
            df["Time"] = df["Time"] / 1000

        # ✅ Apply low-pass filter to both channels
        df["Channel3"] = low_pass_filter(df["Channel3"])
        df["Channel4"] = low_pass_filter(df["Channel4"])

        # ✅ Normalize EOG values (scaling)
        df["Channel3"] = (df["Channel3"] - df["Channel3"].mean()) / df["Channel3"].std()
        df["Channel4"] = (df["Channel4"] - df["Channel4"].mean()) / df["Channel4"].std()

        return df
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return None

# 🎯 **Extract EOG Features**
def extract_eog_features(df, condition_name, max_time):
    try:
        # ✅ Filter data up to the required time duration
        df = df[df["Time"] <= max_time]

        # ✅ **Blink Rate Calculation**
        blink_threshold = df["Channel3"].mean() + 3 * df["Channel3"].std()  # Dynamic threshold
        blinks = np.sum(np.diff((df["Channel3"] > blink_threshold).astype(int)) == 1)
        blink_rate = blinks / (max_time / 60)  # Blinks per minute

        # ✅ **Fixation Duration (Average Time between Blinks)**
        blink_indices = np.where(np.diff((df["Channel3"] > blink_threshold).astype(int)) == 1)[0]
        if len(blink_indices) > 1:
            fixation_duration = np.mean(np.diff(df["Time"].iloc[blink_indices]))
        else:
            fixation_duration = np.nan  # If no blinks detected

        # ✅ **Saccade Amplitude**
        saccade_amplitude = df["Channel4"].max() - df["Channel4"].min()

        # ✅ **Eye Movement Velocity**
        df["Velocity"] = np.gradient(df["Channel4"]) / np.gradient(df["Time"])
        eye_movement_velocity = df["Velocity"].abs().mean()

        return blink_rate, fixation_duration, saccade_amplitude, eye_movement_velocity
    except Exception as e:
        print(f"❌ Error processing features for {condition_name}: {e}")
        return None, None, None, None

# 🎯 **Process All EOG Files**
def process_eog_files(file_list, condition_name):
    feature_data = []

    for file_name in file_list:
        file_path = os.path.join(data_folder, file_name)
        print(f"🔄 Processing {file_name}...")

        df = read_eog_file(file_path)  # ✅ Read and clean data

        if df is not None:
            subject = file_name.split(" ")[0]  # Extract subject ID
            max_time = time_limits[condition_name]  # Get time limit
            
            # ✅ Extract features
            blink_rate, fixation_duration, saccade_amplitude, eye_movement_velocity = extract_eog_features(df, condition_name, max_time)

            if blink_rate is not None:
                feature_data.append([subject, condition_name, blink_rate, fixation_duration, saccade_amplitude, eye_movement_velocity])

    # ✅ Convert to DataFrame and Save
    df_features = pd.DataFrame(feature_data, columns=["Subject", "Condition", "Blink Rate", "Fixation Duration", "Saccade Amplitude", "Eye Movement Velocity"])
    output_csv = os.path.join(data_folder, f"EOG_Features_{condition_name}.csv")
    df_features.to_csv(output_csv, index=False)
    
    print(f"✅ Features for {condition_name} saved in {output_csv}")

# 🎯 **Process all conditions**
process_eog_files(normal_files, "NORMAL")
process_eog_files(happy_files, "HAPPY")
process_eog_files(stressed_files, "STRESSED")

# 🎯 **Final Summary**
print("\n🎯 EOG Feature Extraction Completed Successfully! 🚀")
print("🔹 Extracted features saved for Normal, Happy, and Stressed conditions.")
