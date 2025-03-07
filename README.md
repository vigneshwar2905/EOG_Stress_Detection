The proposed EOG-based stress detection system follows these steps:
Step 1: Data Acquisition
•	Record EOG signals from 20 subjects using AD Instruments BioAmp.
•	Capture signals under Normal, Happy, and Stressed conditions.
Step 2: Signal Preprocessing
•	Apply low-pass filtering (<30 Hz) to remove noise.
•	Normalize the signal to maintain uniformity across subjects.
Step 3: Feature Extraction
•	Extract key features: 
o	Blink Rate (BR) → Number of blinks per minute.
o	Fixation Duration (FD) → Average duration of fixations.
o	Saccadic Amplitude (SA) → Magnitude of rapid eye movements.
o	Eye Movement Velocity (EMV) → Speed of eye movements.
Step 4: Statistical Analysis
•	Perform ANOVA and t-tests to analyze differences across emotional states.
•	Validate feature significance in stress detection.
Step 5: Visualization & Interpretation
•	Generate bar graphs to compare feature variations across conditions.
•	Interpret results to assess EOG’s effectiveness in stress detection.
________________________________________


4.2 Algorithm for Feature Extraction
Input: Preprocessed EOG signal (Channel 3 for vertical, Channel 4 for horizontal movement)
Output: Extracted BR, FD, SA, and EMV features
1.	Read EOG Data 
o	Load signal data from all 60 files (20 subjects × 3 conditions).
2.	Filter Noise 
o	Apply low-pass filter (<30 Hz) to remove unwanted frequencies.
3.	Segment Data by Condition 
o	Extract first 2 minutes for Normal, 3 minutes for Happy & Stressed.
4.	Feature Calculation 
o	Blink Rate (BR): Count signal peaks corresponding to blinks.
o	Fixation Duration (FD): Compute average time spent in fixations.
o	Saccadic Amplitude (SA): Measure peak-to-peak amplitude of saccades.
o	Eye Movement Velocity (EMV): Compute rate of change in signal over time.
5.	Save Features 
o	Store extracted values in a CSV file for statistical analysis.
