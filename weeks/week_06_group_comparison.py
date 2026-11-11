import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from pathlib import Path

# Repository-relative paths; see week_01 for why.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"

path_file = DATA / "raw" / "speech_features.csv"

df = pd.read_csv(path_file)

# Do patients and controls differ in speech rate?

table = (
    df.groupby("group")
      .agg(
          speech_rate_mean=("speech_rate_wpm", "mean"),
          speech_rate_std=("speech_rate_wpm", "std"),
          participant_count=("participant_id", "count")
      )
)

print(table)

# Answer these in comments.
# A. What is your outcome variable? > mean and standard deviation of speech rate (speech_rate_wpm), and the number of participants in each group (participant_count)
# B. What is your grouping/predictor variable? > group
# C. How many groups are there? > 2
# D. Is the outcome categorical or continuous? > continuous
# E. Are the Control and Patient groups independent? > yes
# F. Based on those answers, what kind of statistical comparison would make sense? > independent samples t-test


# Make a boxplot to visualize the data
plt.figure(figsize=(8, 6))
plt.boxplot(
    [df[df["group"] == "Control"]["speech_rate_wpm"].dropna(),
     df[df["group"] == "Patient"]["speech_rate_wpm"].dropna()],
    labels=["Control", "Patient"]
)
plt.title("Speech Rate by Group")
plt.ylabel("Speech Rate (words per minute)")

specific_path = FIGURES / "speech_rate_boxplot.png" 
plt.savefig(specific_path, dpi=300, bbox_inches='tight')  # Save the figure as a PNG file

plt.show()  

# A. Which group appears to have higher speech rate? > Control
# B. Which group appears more variable? > I do not know how to tell this from the boxplot (sd variance + onger box → greater middle-50% spread)
# C. Do the distributions look dramatically different? > No
# D. Does the plot make you think there might be a group difference? > Not a lot

# Is age related to speech rate?

corr = df["age"].corr(df["speech_rate_wpm"])
print(f"Correlation between age and speech rate: {corr:.2f}")

plt.scatter(df["age"], df["speech_rate_wpm"])
plt.xlabel("Age")
plt.ylabel("Speech Rate (words per minute)")
plt.title("Age vs. Speech Rate")
plt.show()

# correlation coefficient > 0.09
# positive or negative? > positive 
# weak, moderate, or strong? > weak, -1 to 1, 0.09 is very close to 0, so it is weak.
# one sentence interpreting it > There is a very weak positive correlation between age and speech rate (r = .09), indicating little evidence of a linear association between the two variables.


# first hypothesis
# Do patients and controls differ in speech rate?
# Null hypothesis
# H0: There is no difference in speech rate between patients and controls.
# Alternative hypothesis
# H1: There is a difference in speech rate between patients and controls.

from scipy.stats import ttest_ind
t_test = ttest_ind(df[df["group"] == "Control"]["speech_rate_wpm"].dropna(), df[df["group"] == "Patient"]["speech_rate_wpm"].dropna())

print(f"T-test results: t-statistic = {t_test.statistic:.2f}, p-value = {t_test.pvalue:.4f}")

# T-test results: t-statistic = 3.35, p-value = 0.0010

# Bonus mini challenge
# This one is deliberately designed to make you think like a researcher.
# Suppose your result is:
# Control: np.mean = 123.4
# Patient: np.mean = 108.2
# and your statistical test gives:
# p = 0.03
# Write one sentence describing the result.

# > "The statistical analysis indicates that there is a significant difference in speech rate between the Control group (mean = 123.4) and the Patient group (mean = 108.2), with a p-value of 0.03, suggesting that the Control group has a higher speech rate than the Patient group."


# PROBLEMS OCCURED
    # None.
 


# PACKAGES I USED
    # pandas
    # matplotlib.pyplot 
    # numpy


# THINGS I LEARNED TODAY
    # 1. I learned how to write the table better. 

