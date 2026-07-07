"""
Script: total_volume_for_one_exercise.py
Purpose: This program generates Total Volume report for a selected exercise from the "Workouts" sheet 
         for each weight training sesssion. Total Volume = Summation (Reps * Weight) for every
         set in that weight training session. Data is pulled from data-log.ops spreadsheet - 
         sheet 'Workouts'.  
Author: Gary Dahnke
Date: July 2026
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

file = "fitness-log.ods"

exercise_data = None
weight_training_data = None
exercise = "Leg Press" # one exercise
output_type = "file" # file or online
sheet = "Workouts"

# Retrieve all data from the 'Workouts' sheet and load into a dataframe.
try:
    exercise_data = pd.read_excel(file, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Retrieve all data from the 'Workouts' sheet for weight training and load into a dataframe.
weight_training_data = exercise_data.loc[(exercise_data["Workout Type"] == "Weight Training") & \
    (exercise_data["Exercise"] != "Pull Ups") &  \
    (exercise_data["Exercise"] == exercise) , \
    ["Date","Exercise","Sets","Reps","Weight","Workout Type"]].copy()

# Ensure Date is datetime
weight_training_data["Date"] = pd.to_datetime(weight_training_data["Date"])
# Sort by date
weight_training_data = weight_training_data.sort_values("Date")

#  Add new columns 'Volume Inputs' which is the pairing of 'Reps' and 'Weight as a list to
#  to become elements in another list. The 'Reps' and 'Weight' will be multipied together
#  to calculate another new column 'Total Volume'.
weight_training_data["Reps"] = weight_training_data["Reps"].apply(lambda x: [int(i) for i in x.replace(" ", "").split(",")])
weight_training_data["Weight"] = weight_training_data["Weight"].apply(
    lambda x: (
        [int(i) for i in x.replace(" ", "").split(",")]
        if x.replace(" ", "").replace(",", "").isdigit()
        else ['"Body Weight"']
    )
)
weight_training_data["Volume Inputs"] = weight_training_data["Reps"].combine(
    weight_training_data["Weight"],
    lambda a, b: [[x, y] for x, y in zip(a, b)]
)

# Example. 'Volume Inputs' would be [[7,145],[8,145]] for 2 sets - 1 set of 7 reps of 145 lbs 
#           1 set of 8 reps of 145 lbs where 'Total Volume' = (7*145) + (8*145) = 2175
weight_training_data["Total Volume"] = \
    weight_training_data["Volume Inputs"].apply(lambda sets: sum(int(r) * int(w) for r, w in sets))

# Stacked bar chart
# Set figure size — use plt.figure(figsize=(width, height)) before plotting. Width and height are in inches.
# Wider chart — increase the first value (e.g., figsize=(12,6)) to stretch horizontally.
# Taller chart — increase the second value (e.g., figsize=(8,10)) to stretch vertically.
# Consistent scaling — set a default figure size with plt.rcParams["figure.figsize"] = (12,6) so all charts use that size.

#  Load the dataframe to plot a chart - bar chart - with an x-axis of date and a y-axis of
#  'Total Volume'.
plt.figure(figsize=(14, 6))
plt.bar(weight_training_data["Date"], weight_training_data["Total Volume"], label="Total Volume")
plt.title(f"Training Volume per Exercise - {exercise} - (2 Sets)")
plt.ylabel("Volume (lbs × reps × sets)")
plt.xlabel("Date")
plt.xticks(rotation=30)  # rotate labels for readability
plt.tight_layout()
plt.legend()

# Output chart to a file or online
if output_type == "file":
    # Save charts as *.svg and *.pdf files.    
    try:
        filename = f"total-volume-for-{exercise.lower().replace(" ","-")}.svg"
        print(f"Creating {filename}")
        plt.savefig(filename)
        filename = f"total-volume-for-{exercise.lower().replace(" ","-")}.pdf"
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    finally:
        print(f"Files for execise {exercise} have been created.")
else:
    # Generate image for chart.  
    print(f"Generating chart for {exercise}...")
    plt.show()
