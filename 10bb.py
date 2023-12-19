import csv
import matplotlib.pyplot as plt
import os

# Set the directory path
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
os.chdir(data_path)

# Initialize dictionaries to store the counts for each group
group_counts = {}

# Read the data from the csv file
with open("PumaPositions.csv", "r") as file:
    csv_reader = csv.DictReader(file)

    # Iterate over each row in the csv file
    for row in csv_reader:
        study_area = row["StudyArea"]
        sex = row["Sex"]

        # Create a key for the group (study area + sex)
        group_key = f"{study_area}({sex})"

        # Increment the count for the group
        group_counts[group_key] = group_counts.get(group_key, 0) + 1

# Extract the study areas and sexes from the group keys
study_areas = []
sexes = []
for group_key in group_counts.keys():
    study_area, sex = group_key.split("(")
    sex = sex[:-1]  # Remove the closing parenthesis
    study_areas.append(study_area)
    sexes.append(sex)

# Get the unique study areas and sexes
unique_study_areas = list(set(study_areas))
unique_sexes = list(set(sexes))

# Sort the study areas and sexes in the right order
unique_study_areas.sort(key=lambda x: ["CO", "Patagonia", "WY"].index(x))
unique_sexes.sort()

# Initialize lists to store the counts for each group
male_counts = []
female_counts = []

# Iterate over the study areas and sexes
for study_area in unique_study_areas:
    for sex in unique_sexes:
        # Create group key
        group_key = f"{study_area}({sex})"

        # Get count for the group
        count = group_counts.get(group_key, 0)

        # Append count to the respective list based on the sex
        if sex == "M":
            male_counts.append(count)
        elif sex == "F":
            female_counts.append(count)

# Set width of each bar
bar_width = 0.30

# Set x coordinates for the bars
x_male = range(len(unique_study_areas))
x_female = [x + bar_width for x in x_male]

# Create the bar plot
plt.bar(x_male, male_counts, width=bar_width, label="Male")
plt.bar(x_female, female_counts, width=bar_width, label="Female")

plt.xticks([x + bar_width / 2 for x in x_male], unique_study_areas)

# y-axis
plt.ylabel("Count")

# Set the title
plt.title("Puma Positions")
plt.legend()
plt.show()
