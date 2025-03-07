import pandas as pd
import matplotlib.pyplot as plt

# File paths for the three states
normal_file = "C:/Users/Dell/OneDrive/Desktop/PYTHON/PROJECT/EOG_Features_NORMAL.csv"
happy_file = "C:/Users/Dell/OneDrive/Desktop/PYTHON/PROJECT/EOG_Features_HAPPY.csv"
stressed_file = "C:/Users/Dell/OneDrive/Desktop/PYTHON/PROJECT/EOG_Features_STRESSED.csv"

# Load the data
df_normal = pd.read_csv(normal_file)
df_happy = pd.read_csv(happy_file)
df_stressed = pd.read_csv(stressed_file)

# ✅ Check if required columns exist
required_columns = ["Blink Rate", "Fixation Duration", "Saccade Amplitude", "Eye Movement Velocity"]
for df, state in zip([df_normal, df_happy, df_stressed], ["Normal", "Happy", "Stressed"]):
    for col in required_columns:
        if col not in df.columns:
            print(f"⚠️ Missing column: {col} in {state} dataset! Check the file.")
            exit()

# ✅ Compute mean values for each state
mean_values = {
    "Condition": ["HAPPY", "NORMAL", "STRESSED"],
    "Blink Rate": [df_happy["Blink Rate"].mean(), df_normal["Blink Rate"].mean(), df_stressed["Blink Rate"].mean()],
    "Fixation Duration": [df_happy["Fixation Duration"].mean(), df_normal["Fixation Duration"].mean(), df_stressed["Fixation Duration"].mean()],
    "Saccade Amplitude": [df_happy["Saccade Amplitude"].mean(), df_normal["Saccade Amplitude"].mean(), df_stressed["Saccade Amplitude"].mean()],
    "Eye Movement Velocity": [df_happy["Eye Movement Velocity"].mean(), df_normal["Eye Movement Velocity"].mean(), df_stressed["Eye Movement Velocity"].mean()]
}

# Convert to DataFrame
df_mean = pd.DataFrame(mean_values)

# ✅ Plot the features
plt.figure(figsize=(10, 6))

# Line plot for each feature
for feature in required_columns:
    plt.plot(df_mean["Condition"], df_mean[feature], marker="o", label=feature)

# Formatting
plt.xlabel("Condition")
plt.ylabel("Feature Value")
plt.title("Effect of Stress on EOG Features")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
