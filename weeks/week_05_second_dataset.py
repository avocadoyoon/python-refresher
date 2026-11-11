import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from pathlib import Path

# Repository-relative paths; see week_01 for why.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"

path = DATA / "raw" / "speech_features.csv"

df = pd.read_csv(path)

# investigate

print(df.head())
print(df.shape) # gives the first 5 lines of the table, rows x cols
print(df.columns)
df.info() 
df.describe()


# a little table

headers = ["Variable" , "What kind of variable?", "What does it measure?" ]

prosodic_feautes = [
    ["age" , "continous" , "participant's age" ],
    ["group" , "categorical", "paricipant's group"],
    ["duration_s" , "continous", "how long does the speech last?"],
    ["mean_f0_hz" , "continous", "average fundemental frequency (f0)"],
    ["pitch_range_hz" , "continous", "max f0-min f0"],
    ["mean_intensity_db" , "continous", "average loudness"],
    ["hnr_db" , "continous", "acoustic quality measure"],
    ["jitter_local", "continous", "acoustic quality measure"],
    ["shimmer_local" , "continous",  "acoustic quality measure"],
    ["speech_rate_wpm" , "continous", "the speed at which person talks"],
]

print(tabulate(prosodic_feautes, headers=headers, tablefmt="grid"))


# Missing values#
# How many missing values does each column contain?

print(df.isnull().sum())


# try to get only the missing values

missing_speech = df[df[["mean_f0_hz", "hnr_db", "speech_rate_wpm"]].isnull().any(axis=1)]

print(missing_speech)

    # : means give me all the rows


# Which participants have missing speech measurements?

print(df.groupby("group")["mean_f0_hz"].mean())
print(df.groupby("group")["hnr_db"].mean())
print(df.groupby("group")["speech_rate_wpm"].mean())


# Acoustic descriptive stats (Task 4 and 5 together)

desc_stats = df.groupby("group").agg({
    "duration_s": ["mean", "std", "min", "max"],
    "mean_f0_hz": ["mean", "std", "min", "max"],
    "pitch_range_hz": ["mean", "std", "min", "max"],
    "mean_intensity_db": ["mean", "std", "min", "max"],
    "hnr_db": ["mean", "std", "min", "max"],
    "jitter_local": ["mean", "std", "min", "max"],
    "shimmer_local": ["mean", "std", "min", "max"],
    "speech_rate_wpm": ["mean", "std", "min", "max"]
})   

print(desc_stats)


# Plotting

# Plot A: A comparison of: mean speech rate between Control and Patient

speech_mean = df.groupby("group")["speech_rate_wpm"].mean()

plt.bar(speech_mean.index, speech_mean.values, color="orangered", width=0.6)

specific_path = FIGURES / "mean_speech_rate.png"

plt.xlabel("group")
plt.ylabel("average speech rate")
plt.title("Average speech rate per group")

plt.savefig(specific_path, dpi=300, bbox_inches="tight")

# Display and close
plt.show()
plt.close()

# Scatter plot of age x speech rate
# FIXED: Added quotes around column names
plt.scatter(df["age"], df["speech_rate_wpm"], color='indianred', alpha=0.7)

# FIXED: Added quotes around labels and title
plt.xlabel("Age")
plt.ylabel("Speech rate (WPM)")
plt.title("Speech rate based on age")

path_b = FIGURES / "speech_rate_age.png"

# FIXED: Changed bbox_inches to 'tight' so it crops the image perfectly without cutting off text
plt.savefig(path_b, dpi=300, bbox_inches='tight')

# Display and close
plt.show()
plt.close()

# Does speech rate appear to change with age? > The scatterplot does not show a clear linear relationship between age and speech rate. There is considerable variability across ages, with several potentially unusual observations.
# Is the relationship obvious or weak? > I cannot tell this without a statistics.
# Are there any unusual observations? > I see some outliers, like there is one in the age group 40, speech rate is lower than 40. also one above 180.
# Does the plot make you want to test the relationship statistically? > Yes.


# Dataset
# How many participants?
# How many controls/patients?
# How many missing values? 

# 1. Total participants (Cleaned up the f-string)
par = df["participant_id"].count()
print(f"Total participants: {par}")

# 2. Total participants per group (Isolated to participant_id column)
group_no = df.groupby("group")["participant_id"].count()
print(f"Total participants per group:\n{group_no}")

# 3. Missing values (Fixed typo in 'Number' and f-string syntax)
missing = df.isnull().sum()
print(f"Number of missing values:\n{missing}")




# Acoustic measures
# Which feature has the largest variability?
# Which has the smallest? 
# Which feature seems most different between groups?

# Replace these with your actual acoustic column names
acoustic_features = ["duration_s", "pitch_range_hz", "mean_intensity_db", "hnr_db", "jitter_local", "shimmer_local", "speech_rate_wpm"] 


# Q1-2
# We use the Coefficient of Variation (CV = standard dev / mean) 
# This standardizes the variability across different units (Hz, dB, %).
cv_metrics = df[acoustic_features].std() / df[acoustic_features].mean()

largest_var_feature = cv_metrics.idxmax()
smallest_var_feature = cv_metrics.idxmin()

print(f"1. Feature with largest variability: {largest_var_feature} (CV: {cv_metrics.max():.4f})")
print(f"2. Feature with smallest variability: {smallest_var_feature} (CV: {cv_metrics.min():.4f})")


# Q3
# We calculate the absolute difference between group means, normalized by pooled standard deviation.
# For 2 groups, this is Cohen's d (Effect Size). For 3+ groups, we look at variance of means.

group_means = df.groupby("group")[acoustic_features].mean()
overall_std = df[acoustic_features].std()

# Find the feature where group averages deviate the most relative to their standard deviation
group_differences = (group_means.max() - group_means.min()) / overall_std
most_different_feature = group_differences.idxmax()

print(f"3. Feature most different between groups: {most_different_feature}")


# Age
# Does age appear related to speech rate? # We need a statistical test to see if there is any significance, but from the tables I have seen the difference is not huge, and sometimes the logic differs (for one feature, participants have higher, but for another, it is lower).


# Research interpretation
# Idk what to say except what I wrote about age.

# Bonus challenge
# Find the participant with:
# Highest speech rate and Lowest speech rate
# Return:
    # participant_id
    # group
    # age
    # speech_rate_wpm


highest_idx = df["speech_rate_wpm"].idxmax()
lowest_idx = df["speech_rate_wpm"].idxmin()

target_columns = ["participant_id", "group", "age", "speech_rate_wpm"]

# 3. Extract the full participant profiles
highest_speech_participant = df.loc[highest_idx, target_columns]
lowest_speech_participant = df.loc[lowest_idx, target_columns]

# 4. Print the results cleanly
print("=== Participant with Highest Speech Rate ===")
print(highest_speech_participant.to_string())

print("\n=== Participant with Lowest Speech Rate ===")
print(lowest_speech_participant.to_string())




# PROBLEMS OCCURED
   # When I read the file I keep forgetting that I should add pd instead of df.
   # When you read_csv a file, do not add "" around it.
   # I forgot to add , while creating the table after each [].
   # I forgot the .loc function
   # forgot add agg before creating the table with stats (min, max etc).
   # When I write print with a text, include the group inside "" (e.g., print(f"Number of missing values:\n{missing}")
   

# PACKAGES I USED
    # pandas
    # matplotlib.pyplot 


# THINGS I LEARNED TODAY
    # 1. tabulate is used to create a simple table.
    # 2. df[condition] / df.loc[:, condition]
    # 3. Added Newlines (\n): Added a line break before printing full series/tables (group_no and missing) 
    # so the data aligns beautifully underneath your text labels instead of breaking layout on the same line.
    # 4. I learned how to calculate variance.
    # Learned a new function:
        # .idxmax() / .idxmin(): Pinpoints the exact index location 
        # of the maximum and minimum values in the speech_rate_wpm column.

   