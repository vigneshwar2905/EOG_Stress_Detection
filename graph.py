import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📂 Define the folder where CSV files are stored
data_folder = r"C:\Users\Dell\OneDrive\Desktop\PYTHON\PROJECT"

# ✅ Load all three CSV files
normal_df = pd.read_csv(os.path.join(data_folder, "EOG_Features_NORMAL.csv"))
happy_df = pd.read_csv(os.path.join(data_folder, "EOG_Features_HAPPY.csv"))
stressed_df = pd.read_csv(os.path.join(data_folder, "EOG_Features_STRESSED.csv"))

# ✅ Add condition labels
normal_df["Condition"] = "NORMAL"
happy_df["Condition"] = "HAPPY"
stressed_df["Condition"] = "STRESSED"

# ✅ Merge all data
df = pd.concat([normal_df, happy_df, stressed_df], ignore_index=True)

# ✅ Define features to plot
features = ["Blink Rate", "Fixation Duration", "Saccade Amplitude", "Eye Movement Velocity"]

# ✅ Create subplots for all features
plt.figure(figsize=(12, 8))
for i, feature in enumerate(features, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(x="Condition", y=feature, data=df, palette="Set2")
    plt.title(f"{feature} Across Conditions")
    plt.xlabel("Condition")
    plt.ylabel(feature)
    plt.grid(True)

# ✅ Show the plots
plt.tight_layout()
plt.show()
