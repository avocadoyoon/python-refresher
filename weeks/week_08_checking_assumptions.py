# What is an assumption?
# An assumption is basically a condition that a statistical method expects your data to reasonably satisfy.

# Assumption 1: Normality
# The outcome should be reasonably normally distributed, particularly within groups.

# How do we check for normality?
# 1. Visual inspection: histograms, boxplots, Q-Q plots.
# 2. Shapiro-Wilk test: a formal statistical test of normality.
    # p < .05
    # ↓
    # evidence against normality


# Q-Q: If the points roughly follow the reference line, the data are reasonably compatible with normality.


# Assumption 2: Equal variance
# Suppose we have two groups, and we want to compare their means. If one group has a much larger variance than the other, it can affect the validity of the t-test.
# The assumption that groups have similar variances is called: homogeneity of variance or equal variance

# You may see this tested with Levene's test.

# control = df[df["group"] == "Control"]["speech_rate_wpm"].dropna()
# patient = df[df["group"] == "Patient"]["speech_rate_wpm"].dropna()

# stats.levene(control, patient)


# Why do we need non parametic test?

# We have tests for normal distributions, but when the variance is skewed, we use the following:

# | Parametric         | Non-parametric alternative |
# | ------------------ | -------------------------- |
# | Independent t-test | **Mann-Whitney U**         |
# | Paired t-test      | **Wilcoxon signed-rank**   |
# | One-way ANOVA      | **Kruskal-Wallis**         |


# Mann-Whitney U

# stats.mannwhitneyu(
#    control,
#    patient,
#    alternative="two-sided"
# )


# T-test -> t-test Primarily compares means.
# Mann-Whitney U -> Works with the ranks/order of observations rather than relying on the same distributional assumptions as the t-test.

# You can think of it as: "Instead of obsessing over the exact values, let's ask how the observations rank relative to each other."

# Paired t-test

# stats.ttest_rel(before, after)

# If assumptions are problematic:
# Wilcoxon signed-rank test

# stats.wilcoxon(before, after)

# So:
# Same people twice
  #     ↓
# Paired t-test
  #     OR
# Wilcoxon signed-rank


# One-way ANOVA
# But if the data violate assumptions substantially, a possible non-parametric alternative is:
# Kruskal-Wallis

# stats.kruskal(
  #  control,
#  anomic,
#    broca,
#    conduction,
#    wernicke,
#    global_group
# )

# Again:
# 3+ independent groups
  #      ↓
  #   ANOVA
  #      OR
# Kruskal-Wallis

######################

## CONTINUOUS OUTCOME
##      │
#       ▼
#How many groups?
#       │
#   ┌────┴────┐
#   │         │
#   2        3+
#   │         │
#   ▼         ▼
#Independent? ANOVA
#  │
# ┌─┴─┐       ↓
##Yes  No   Kruskal-Wallis
## │    │
## ▼    ▼
##t-test paired
##     t-test
## │     │
## ▼     ▼
## Mann-Whitney  Wilcoxon


##########################



# WEEK 8 MISSION 1: Diagnose the data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from pathlib import Path

# Repository-relative paths; see week_01 for why.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

path_file = DATA / "raw" / "speech_features.csv"

df = pd.read_csv(path_file)

control = df[df["group"] == "Control"]["speech_rate_wpm"].dropna()
patient = df[df["group"] == "Patient"]["speech_rate_wpm"].dropna()

print(control.describe())
print(patient.describe())


# A. Which group has the higher mean? -> controls have the higher mean
# B. Which group has the larger SD? -> controls have the larger SD, meaning they have more variability in their speech rate than patients.
# C. Which group appears more variable? -> controls appear more variable, as they have a larger SD and a wider range of values in their speech rate.


# Visualizition of the data
plt.hist(control)
plt.title("Control Speech Rate")
plt.xlabel("Speech Rate (WPM)")
plt.ylabel("Frequency")
plt.show()

plt.hist(patient)
plt.title("Patient Speech Rate")
plt.xlabel("Speech Rate (WPM)")
plt.ylabel("Frequency")
plt.show()


# A. Do the distributions look roughly symmetric or skewed? Controls look roughly symmetric, while patients look slightly towards right.
# B. Do you notice any extreme observations? Some controls have outliers for example 2-4 people have speech rate 60 and 4 people have 180. Patients have higher values, most, but there is 1 or 2 outliers who has 40.
# C. Does either group look dramatically non-normal? Controls look somewhat normal, but patients have a slight right skew.


# Q-Q plots
stats.probplot(control, dist="norm", plot=plt)
plt.title("Q-Q Plot: Control Speech Rate")
plt.show()


stats.probplot(patient, dist="norm", plot=plt)
plt.title("Q-Q Plot: Patient Speech Rate")
plt.show()

# Do they follow the diagonal line?
# Control: Yes, somewhat. But there are some deviations at the tails, which may indicate some non-normality.
# Patient: Patients look like they follow the line more? I see some clustering, but they deviate more at the tails.

# Normality

control_shapiro = stats.shapiro(control)
patient_shapiro = stats.shapiro(patient)

print("Control:", control_shapiro)
print("Patient:", patient_shapiro)

# Control p-value: 0.5458558517713277
# Patient p-value: 0.2869677115555082

# Does either group show evidence against normality?
# Control: No, the p-value (0.546) is not significant, so we do not reject the null hypothesis of normality.
# Patient: No, the p-value (0.287) is not significant, so we do not reject the null hypothesis of normality.

# The Shapiro-Wilk test did not provide evidence of a departure from normality.

# I still am not sure how to interpret p values correctly. I know that if the p-value is less than 0.05, we reject the null hypothesis, but I am not sure what that means in terms of normality. Does it mean that the 
# data is not normally distributed? Or does it mean that we cannot conclude that the data is normally distributed?


# Levene's test for equal variance

levene_result = stats.levene(control, patient)

print(levene_result)

# Levene p-value: 0.7703125377386528
# Do we have evidence of unequal variances? -> No, the p-value (0.770) is not significant, so we do not reject the null 
# hypothesis of equal variances. There is no statistically significant evidence that the group variances differ.


# t-test and Mann-Whitney U test

t_result = stats.ttest_ind(
    control,
    patient
)

mw_result = stats.mannwhitneyu(
    control,
    patient,
    alternative="two-sided"
)

print("T-test:", t_result)
print("Mann-Whitney U:", mw_result)

# T-test:
# t = 3.349311944900295
# p = 0.0009910590193682636

# Mann-Whitney:
# U = 4470.0
# p = 0.004233697746648512

# A.Do both tests reach the same broad conclusion? -> Yes, both tests reach the same broad conclusion that there is a significant difference between the two groups. The t-test has a p-value of 0.00099, which is less than 0.05, indicating that we reject the null hypothesis of equal means. The Mann-Whitney U test has a p-value of 0.00423, which is also less than 0.05, indicating that we reject the null hypothesis of equal distributions.
# B. If yes, why do you think that might be reassuring? -> It is reassuring because it suggests that the results are robust to the choice of statistical test. Even though the two tests have different assumptions and methods, they both lead to the same conclusion, which increases our confidence in the validity of the findings.
# C. Which test compares means more directly? -> The t-test compares means more directly, as it is specifically designed to test for differences in means between two groups. The Mann-Whitney U test, on the other hand, compares the ranks of the observations and does not directly test for differences in means.
# D. Which test relies more on ranks? -> The Mann-Whitney U test relies more on ranks, as it is a non-parametric test that does not assume a specific distribution for the data.


# The t-test gives:
# p = .001
# Mann-Whitney gives:
# p = .002
# And both indicate Control > Patient.
# Write 2–3 sentences answering:
# What would you conclude about the difference between the groups?

# ANSWER
# Based on the results of both the t-test and the Mann-Whitney U test, we can conclude that there is a statistically significant difference in speech rates between the Control and Patient groups. 
# Specifically, the Control group has a higher mean/rank speech rate compared to the Patient group. 
# This suggests that the condition affecting the Patient group may be associated with slower speech rates.

# Bonus challenge
# 1. t-test
# 2. Mann-Whitney U test? or one of the non paramteric tests?
# 3. paired t-test
# 4. Wilxon signed-rank test?
# 5. One way ANOVA
# 6. Kruskal-Wallis test
