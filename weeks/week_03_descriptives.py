import pandas as pd
import numpy as np
from pathlib import Path

# Repository-relative paths; see week_01 for why.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

cleaned_path = DATA / "cleaned" / "participants_cleaned.csv"

clean_df = pd.read_csv(cleaned_path)

# 1. Create a small table showing:
# Number of participants
# Number of controls
# Number of patients
# Mean age
# Standard deviation of age
# Mean education years

# Number of participants
total_entries = clean_df["participant_id"].count()

# Number of controls 
total_controls = clean_df["group"].value_counts().get("Control", 0)


# Number of patients

total_patients = clean_df["group"].value_counts().get("Patient", 0)

# Mean Age
m_age = clean_df["age"].mean()
sd_age = clean_df["age"].std()

# Mean education years
m_yoe = clean_df["education_years"].mean()

# TABLE
# Create a clean, single-row summary table from scratch
summary_table = pd.DataFrame({
    "Number of participants": [total_entries],
    "Number of controls": [total_controls],
    "Number of patients": [total_patients],
    "Mean Age": [m_age],
    "SD Age": [sd_age],
    "Mean education year": [m_yoe]
})

print(summary_table)


# 2. Calculate the mean and standard deviation of:
# Age
# Education years
# WAB_AQ
# MoCA
# for Control vs Patient.
# a table, not separate print statements. You can use groupby().

# 1. Group by your participant type column and aggregate the metrics
summary_table = clean_df.groupby("group").agg({
    "age": ["mean", "std"],
    "education_years": ["mean", "std"],
    "WAB_AQ": ["mean", "std"],
    "MoCA": ["mean", "std"]
})

# 2. Round the values to 2 decimal places to keep it clean and readable
summary_table = summary_table.round(2)
print(summary_table)


# 3. Create a table of average WAB_AQ by aphasia type and sort it from lowest to highest.
# Which aphasia type appears most severe in this dataset?

# Group, calculate the mean without creating a MultiIndex, and sort lowest-to-highest
table_aq = clean_df.groupby("aphasia_type")["WAB_AQ"].mean().sort_values(ascending=True)

print(table_aq)

# 4. Investigate whether participants with higher education tend to have higher AQ.
# Just calculate a correlation and interpret it: positive? negative? near zero?

corr = clean_df["education_years"].corr(clean_df["WAB_AQ"])

print(corr)

# -0.0216515517517526

# -1.00 -------------------- +1.00

# strong negative

      #  -0.02

# basically nothing
# strong positive

# 5. Create a new column called age_group:
# "younger" if age < 65
# "older" if age ≥ 65
# Then compare the average AQ between the two age groups.

# 1. Create the new column using a fast conditional check


clean_df["age_group"] = np.where(clean_df["age"] < 65, "younger", "older")

# 2. Compare the average AQ between the two groups
aq_comparison = clean_df.groupby("age_group")["WAB_AQ"].mean()
print(aq_comparison)


# 6. List the 5 participants with the lowest AQ.
# Include: participant_id I aphasia_type I age I WAB_AQ

list_aq = clean_df[["participant_id", "aphasia_type", "age", "WAB_AQ"]].nsmallest(5, "WAB_AQ")

print(list_aq)


# Another way
# Sort ascending and take the top 5 rows, filtering for specific columns
lowest_aq = (
    clean_df.sort_values(by="WAB_AQ", ascending=True)
    .head(5)[["participant_id", "aphasia_type", "age", "WAB_AQ"]]
)

print(lowest_aq)


# Write 3–5 sentences in plain English answering:
# Which aphasia type had the lowest average AQ? > Global
# Did patients score lower on MoCA than controls? > Yes. Controls scored approx 7 points higher.
# Was education positively or negatively related to AQ? > There was essentially no linear relationship between education and AQ (r = -0.02).
# Did older participants have lower AQ? > Yes.

# Bonus Challenge
# Create a table showing the number of participants by:
    # aphasia_type
    # sex

# Group by both categories and count the rows
bonus_table = (
    clean_df.groupby(["aphasia_type", "sex"])
    .size()
    .reset_index(name="participant_count")
)

print(bonus_table)



# PROBLEMS OCCURED
    # I could not even make the table-it took me 30 minutes...
    # When I defined the age_group, I forgot I needed to add () after.
    # I forgot to write the several columns together (e.g., [["participant_id", "aphasia_type", "age", "WAB_AQ"]]).
    # I keep forgetting the easy syntax rules and basic stuff :(
    

# PACKAGES I USED
    # pandas
    # numpy

# THINGS I LEARNED TODAY
    # 1. .std()
    # 2. the rule is that I need to create a vector to assign things to (e.g., summary_table  pd.DataFrame({"x" : [y]})
    # 3. agg() -> It tells Pandas exactly which math function to apply to which specific column.
    # 4. round(2) -> round the values to 2 decimal places to keep it clean and readable
    # 5. I do not have to write the names of the calues all over again when creating a table: e.g., table_aq = clean_df.groupby("aphasia_type").agg({
    # 6.  "WAB_AQ":["min", "max"] -> agg should receive columns names.
    # 7. corr() for correlation. Statistic note: 
        # Positive (r > 0): Both variables move in the same direction (as one goes up, the other goes up).
        # Negative (r < 0): Variables move in opposite directions 
        # (as one goes up, the other goes down).Zero (r = 0): No linear pattern or connection between the variables

    # 8. np.where() -> np.where() is a NumPy function that acts like an "IF-THEN-ELSE" statement for entire columns of data
    # 9. .nsmallest(number, category) -> Gives you the desired number of lowest values.
    # 10. You can also use df.sort_values(by="cateogry", ascending=True).head(5)[["participant_id", "aphasia_type", "age", "WAB_AQ"]]
    # 11. .size() ->  This counts the total number of rows in each group created by your .groupby().
    # 12. .reset_index() -> beautifies the table layout and labels the results.



