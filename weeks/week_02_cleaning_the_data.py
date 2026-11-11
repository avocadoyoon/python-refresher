# Task 1: Make a copy of your dataset first (in this case, it is "participants.csv")

import pandas as pd
from pathlib import Path

# Repository-relative paths; see week_01 for why.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# File path
file_path = DATA / "raw" / "participants.csv"

df = pd.read_csv(file_path)
clean_df = df.copy()

print(df.shape)
print(clean_df.shape)


# Task 2: Investigate categorical variables
# What different values exists as these column?

# Shows column names, data types, and row counts
clean_df[["group", "sex", "aphasia_type", "stroke_type"]].info()

# next time check them separately!
 
# Displays combinations sorted from most frequent to least frequent
print(clean_df[["group", "sex", "aphasia_type", "stroke_type"]].value_counts())

# Cleaning the sex column. I choose "male" and "female"
print(clean_df["sex"].unique())

# ['Male' 'female' 'Female' 'M' 'male' 'F' 'male ']

sex_repetitions = {
    "Male" : "male", "M" : "male", "male" : "male", "male ": "male",
    "Female" : "female", "female" : "female", "F" : "female"
    }

clean_df["sex"] = clean_df["sex"].map(sex_repetitions) 

print(clean_df["sex"].unique())

# Clean aphasia types

print(clean_df["aphasia_type"].unique())

# [nan ' broca' 'Broca' 'Broca ' 'BROCA' 'Wernicke' 'WERNICKE' 'Conduction', 'Anomic' 'Global']

aphasia_types = {
    "nan" : "NaN",
    " broca" : "broca", "Broca" : "broca", "Broca ": "broca", "BROCA" : "broca",
    "Wernicke" : "wernicke", "WERNICKE" : "wernicke",
    "Conduction" : "conduction",
    "Anomic" : "anomic",
    "Global" : "global"
    }

clean_df["aphasia_type"] = clean_df["aphasia_type"].map(aphasia_types)

print(clean_df["aphasia_type"].unique())

# you can use replace instead of map here too! why? 
# Because map() replaces anything not in the dictionary with NaN.
# replace() leaves unknown values untouched.

# Investigate impossible values
impossible_a = clean_df[clean_df["age"] > 110]
impossible_ed = clean_df[clean_df["education_years"] < 0]
impossible_aq = clean_df[clean_df["WAB_AQ"] > 100]

print(impossible_a)
print(impossible_aq)
print(impossible_ed)

#############################################################
# they are controls (PO06, P034, P013) the information of impossible values are easy to learn and report to if it is a new data. 
# If this was an old data, I would delete them. But for now I will act like I can ask it.

clean_df["age"] = clean_df["age"].replace(145, 45)
clean_df["education_years"] = clean_df["education_years"].replace(-2, 12)
clean_df["WAB_AQ"] = clean_df["WAB_AQ"].replace(105.0, 100)

# A little risky if there is more than 145. Use .loc from now on.

impossible_a = clean_df[clean_df["age"] > 110]
impossible_ed = clean_df[clean_df["education_years"] < 0]
impossible_aq = clean_df[clean_df["WAB_AQ"] > 100]

print(impossible_a)
print(impossible_aq)
print(impossible_ed)

# Missing values

missing = clean_df.isnull().sum()

print(missing)

no_control = clean_df["group"].value_counts().get("Control", 0)

print(no_control)

# confirmed. None's belong to controls, which is normal for controls not to have stroke, stroke and an aphasia type.
# one missing value in MoCa and age.

missing_any = clean_df[(clean_df["age"].isna()) | (clean_df["MoCA"].isna())]
print(missing_any[["participant_id", "group", "age", "MoCA"]])

# Output
###########################################
# participant_id    group   age  MoCA
# 40           P041  Control  60.0   NaN
# 41           P042  Control   NaN  26.2
###########################################

# They are controls. Again, I will act like I can learn the age but the MoCA is a task that in real life i could not ask the participant to redo it maybe. So I will keep it as NaN and when we reach to the point I do analysis here, I will just remove it.

# target rows where participant_id is 'P042', and update ONLY the 'age' column
clean_df.loc[clean_df["participant_id"] == "P042", "age"] = 58

# Double-check the missing value count
print(clean_df.isnull().sum())

# Duplicated participants
# find how many
duplicate_count = clean_df["participant_id"].duplicated().sum()

print(f"Number of duplicate IDs found: {duplicate_count}")

# 1, delete it
clean_df = clean_df.drop_duplicates(subset=['participant_id'], keep='first')

# check it
print(clean_df.shape)


# Bonus challenges
# A. See the new sex column

cleaned_gender = clean_df["sex"].value_counts()
print(f"Sex values of this dataset: {cleaned_gender}")

# B. Save the new dataset

file_path_new = DATA / "cleaned" / "participants_cleaned.csv"

clean_df.to_csv(file_path_new, index=False)

print(f"Your cleaned data has been added succesfully!")

# === Mission 2 Cleaning Report ===

# 1. Duplicate participants removed: 1

# Sex labels standardized:
# Before: Male, male, M...
# After: male, female

# 3. Aphasia labels standardized: All incapitalized (e.g., wernicke, broca, conduction, global)

# 4. Impossible values:
# Age: changed from 145 to 45
# Education: changed from -2 to 12
# AQ: 105.0 to 100

# Decision: They are controls (PO06, P034, P013) the information of impossible values are easy to learn and report to if it is a new data. 
# If this was an old data, I would delete them. But for now I will act like I can ask it.

# 5. Missing values:
# PO42 age -> added as 58, hypothetically we could ask for the age.
# MoCA value kept as a NaN, will be removed while analysing.


# 6. Remaining participants: 180


# PROBLEMS OCCURED
    # I complicated the copying process. It is just one line of code.
    # Tuples do not take () after. I wrote () after df.shape. Functions do, but tuples do not.
    # Does this do something? (copy, head, info, describe, groubpy, replace, drop_duplicated) -> use paranthesis / Just an info about df? (shape, columns, index, dtypes) -> no paranthesis
    # I tried to wtite the columns in separate brackets, it is not right. Add all in one bracket, separating them with "" and ,
    # I keep messing up the brackets, lol. I need to be more careful with it.
    # I ALMOST RUINED MY AGE COLUMN JESUS.
    # I could not find the duplicated participants first. Then did not know how to delete them.

# PACKAGES I USED
    # pandas


# THINGS I LEARNED TODAY
   # 1. df.copy()
   # 2. print(clean_df[["group", "sex", "aphasia_type", "stroke_type"]].value_counts())
   # 3. I can create a dictionary linking messy data with {
   # 4. with .replace(x,y) I can assign/change the values I want.
   # 5. I learned a cool tool .isna.
   # 6. I can separate two columns with "|" e.g., missing_any = clean_df[(clean_df["age"].isna()) | (clean_df["MoCA"].isna())]
   # 7. .replace() looks for a specific value, while .loc looks for a specific condition.
   # 8. You can add an extra function after one function (e.g., .duplicated().sum())
   # 9. The function to delete the duplicated value -> .drop_duplicates(subset=['participant_id'], keep='first')
   # 10. I learned how to save my data! (DataFrame -> to.csv()). Note, it is recommended to add index = False, idk exactly why ig it corrupts the CSV dataset.
   # I did not get to use unique() function here.


