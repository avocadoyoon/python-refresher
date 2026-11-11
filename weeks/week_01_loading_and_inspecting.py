import pandas as pd
from pathlib import Path

# Paths are built from this file's own location, not from one computer's home
# folder, so they keep working after a clone and whatever directory you run
# from. parents[1] is the repository root, because this script lives in weeks/.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# File path
file_path = DATA / "raw" / "participants.csv"

# Load CSV
df = pd.read_csv(file_path)

# Show first 5 rows
print(df.head())

# "Using pandas (pd), read a CSV file located at file_path, and store the resulting DataFrame in df."

print(df.shape) # gives the first 5 lines of the table, rows x cols
print(df.columns)
df.info() 
df.describe()

#  Mission 1 Report

# Number of participants
total_entries = df["participant_id"].count()

print(total_entries)

# Number of controls 
total_controls = df["group"].value_counts().get("Control", 0)

print(total_controls)

# Number of patients

total_patients = df["group"].value_counts().get("Patient", 0)

print(total_patients)
  
# Mean Age
m_age = df["age"].mean()

print(m_age)

# Mean AQ

m_aq = df["WAB_AQ"].mean()

print(m_aq)

# Missing values
missing = df.isnull().sum()

print(missing)

# Returns a single integer representing the total duplicate count
duplicate_count = df.duplicated("participant_id").sum()
print(f"Total duplicate participant IDs: {duplicate_count}")


# Impossible values found
impossible_age = df[df["age"] > 110]
impossible_education = df[df["education_years"] < 0]
impossible_aq = df[df["WAB_AQ"] > 100]

print(impossible_age)
print(impossible_aq)
print(impossible_education)

    # pattern:
    # DataFrame -> column -> condition -> filtered DataFrame


# Average AQ by aphasia types (table)
avg_aq = df.groupby("aphasia_type")["WAB_AQ"].mean()

print(avg_aq)

# Mini challenge
    # Which aphasia type has the lowest average AQ?
min_aq = df.groupby("aphasia_type")["WAB_AQ"].mean()
print(min_aq)

    # Which aphasia type has the highest average age?
max_age = df.groupby("aphasia_type")["age"].mean()
print(max_age)

    # Are there more males or females?
gender = df["sex"].value_counts()
print(gender)


    # Do patients have lower MoCA scores than controls?
moca = df.groupby("group")["MoCA"].mean()
print(moca)

    # Show me only Broca participants
broca = df[df["aphasia_type"] == "Broca"]
print(broca)

# PROBLEMS OCCURED
    # I could not remember the order in the beginning.
    # I did not know some functions.
    # I forgot the [] rule.
    # I missed one bracket rule so the code did not work.

# PACKAGES I USED
    # pandas


# THINGS I LEARNED TODAY
    # 1. assign your table to something (e.g., df), then you will place is in front of the function most of the time (e.g., df.count()..)
    # 2. functions comes after the assigned file name, but you add the action in the end (e.g., count, mean)    
    # 3. I learned some functions (shape, info, describe, isnull, duplicated, groupby)
    # 4. df[["something", "another"]] -> multiple columns
    # 5. Learned the filtering (e.g., impossible_age = df[df["age"] > 110])
    # 6. The bracket rule -> df[df["COLUMN"] CONDITION]

