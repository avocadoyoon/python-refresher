import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Repository-relative paths; see week_01 for why.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"

path_file = DATA / "cleaned" / "participants_cleaned.csv"

clean_df = pd.read_csv(path_file)

# 1. What does the age distribution of our participants look like?
# Histogram 

# Create the histogram
plt.hist(clean_df["age"], bins=30, color="skyblue", edgecolor='black')

# Add labels and title
plt.xlabel("age")
plt.ylabel("frequency")
plt.title("Age Distribution")


specific_path = FIGURES / "age_distribution.png"

plt.savefig(specific_path, dpi=300, bbox_inches="tight")

# Display the plot
plt.show()

# Clear the current plot memory
plt.close()

# Is the distribution symmetric?
# Are there many older participants? Yes!
# Any strange values? 

# The age distribution is relatively broad and does not appear strongly symmetric. Participants range approximately from their mid-30s to around 90 years old, with relatively substantial representation across the age range.


# 2. Which aphasia type is most impaired?
# Create a bar plot showing:
# Average AQ for each aphasia type.
# Requirements:
# Sort from lowest to highest
# Label axes
# Add a title


# Calculate the grouped data first to keep the code clean
grouped_data = clean_df.groupby("aphasia_type")["WAB_AQ"].mean().sort_values(ascending=True)

# Pass BOTH the index (x) and the values (height) to plt.bar
plt.bar(grouped_data.index, grouped_data.values, color="pink", width=0.6)

plt.xlabel("aphasia type")
plt.ylabel("average AQ")
plt.title("AQ average per aphasia type")

# Save the plot
specific_path = FIGURES / "wab_aq_scores.png"
plt.savefig(specific_path, dpi=300, bbox_inches="tight")

# Display and close
plt.show()
plt.close()

# Then write 2 sentences interpreting it.
# The highest score belongs to anomic group while the lowest score belongs to global. This is natural since in the global aphasia almost all the modalities are lesioned, hence the lower score.
# Same logic applies to anomic, it is a milder type of aphasia, hence higher scores.


# 3. Do older participants tend to have lower AQ?
# Do a scatterplot.
# x = age
# y = WAB_AQ

plt.scatter(clean_df["age"], clean_df["WAB_AQ"], color="blue", alpha=0.7)

# Add titles and labels
plt.xlabel("Age")
plt.ylabel("AQ scores")
plt.title('Relationship between age and AQ scores')



specific_path = FIGURES / "age_aq_interaction.png"

plt.savefig(specific_path, dpi=300, bbox_inches="tight")

plt.show()

# Then answer:
# Do you see a trend? Yes. There is a lot of clustering around 100 across ages.
# Is it strong? I cannot say it without statistics, but it is possible!
# Are there clusters? Yes, around scores 100 and 60-80.


# 4. Create a bar plot comparing
# Average MoCA
# between
# Control
# Patient

grouped_data_2 = clean_df.groupby("group")["MoCA"].mean()

plt.bar(grouped_data_2.index, grouped_data_2.values, color="pink", width=0.6)

plt.xlabel("Group")
plt.ylabel("Mean MoCA")
plt.title("Mean MoCA by Group")


specific_path = FIGURES / "moca_group_interaction.png"
plt.savefig(specific_path, dpi=300, bbox_inches="tight")

plt.show()

# Question: If you were presenting this at a conference, what sentence would you say while showing the figure?
# "As figure illustrates, control group has a higher MoCA scores."

# Use a bar chart.
# Show Number of male-female participants.

# 1. Count the occurrences of each category in the 'sex' column
grouped_data_3 = clean_df["sex"].value_counts()

# 2. Plot using the categories (index) and the counts (values)
plt.bar(grouped_data_3.index, grouped_data_3.values, color="brown", width=0.6)

# Add clear labels for readability
plt.xlabel("sex")
plt.ylabel("number of participants")
plt.title("Distribution of participants by sex")

# Save and show
specific_path = FIGURES / "sex_distribution.png"
plt.savefig(specific_path, dpi=300, bbox_inches="tight")

plt.show()
plt.close()


# Question: Is the dataset balanced?
# The dataset is relatively balanced by sex, although there are somewhat more male than female participants.


# Bonus challenge

# Create a wide figure (10 inches wide, 4 inches high)
# I could not do it. Ask gpt bbygirl.



# PROBLEMS OCCURED
    # I forgot how to write the ascencing/descending order.
    # bar plot is a little annoying. I keep forgetting to add labels.


# PACKAGES I USED
    # pandas
    # matplotlib.pyplot


# THINGS I LEARNED TODAY
    # 1. I learned how to create histograms!
    # 2. Creating a histogram is similar to the way we do it in R!
        # plt.xlabel("age")
        # plt.ylabel("frequency")
        # plt.title("Age Distribution")
    # 3. I learned how to visualize the data (plt.show()), and how to save it to a specific path (plt.savefig())
    # 4. For some reason it is recommended to clear the plot memory (plt.close()).
    # 5. I learned how to use plot bar syntax. It is slightly different than hist. I need to assign the calculation of two separate values first, then write them in the plt.bar() function. It reads more cleanly.
    # 6. plt.scatter() is really easy to write.

  