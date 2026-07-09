"""
Script: training_load_per_exercise.py
Purpose: This program generates Training Load per Exercise report for a selected or all exercises from 
         the "Workouts" sheet for each weight training sesssion. Total Volume = Summation (Reps * Weight) 
         for every set per exercise in that weight training session. Data is pulled from data-log.ops 
         spreadsheet - sheet 'Workouts'. At this time, data in the spreadsheet is for one calendar year.
         User Set Variables:
         1. spreadsheet - fitness log spreadsheet
         2. execises - a list of weight training exercise that the user wants to create charts. If the
            list is left, a default list of all weight training exercise will be processed
         2. output-type - a flag to define the type of output for the chart 
            options: file or online          
Author: Gary Dahnke
Date: July 2026
"""
import os   
import pandas as pd
import matplotlib.pyplot as plt
import analytics

"""
User Set Variables - Start
"""
spreadsheet = "fitness-log.ods"
# To run one or more selected exercises, populate the list 'exercises'. Otherwise, the program will
# create a list with all exercises currently listed in the spreadsheet.
exercises = []
# exercises = ["Leg Press", "Calf Raises"]
output_type = "file" # file or online
"""
User Set Variables - End
"""

# Retrieve all data from the 'Workouts' sheet and load into a dataframe.
sheet = "Workouts"
try:
    exercise_data = pd.read_excel(spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Retrieve all data from the 'Workouts' sheet for weight training and load into a dataframe.
weight_training_data = exercise_data.loc[(exercise_data["Workout Type"] == "Weight Training") & (exercise_data["Exercise"] != "Pull Ups"), \
    ["Date","Exercise","Sets","Reps","Weight","Workout Type"]].copy()

# Select the rows from the dataframe that are exercises in the list 'exercises'.
if len(exercises) == 0:
    exercises = list(weight_training_data["Exercise"].unique())

# Traverse through each exercise in the list to accomplish the following:
#   1. Select all rows from the from the dataframe for the current exercise being processed
#      by the loop
#   2. Add new columns 'Volume Inputs' which is the pairing of 'Reps' and 'Weight as a list to
#      to become elements in another list. The 'Reps' and 'Weight' will be multipied together
#      to calculate another new column 'Total Volume'.
#      Example. 'Volume Inputs' would be [[7,145],[8,145]] for 2 sets - 1 set of 7 reps of 145 lbs 
#                1 set of 8 reps of 145 lbs where 'Total Volume' = (7*145) + (8*145) = 2175
#   3. Load the dataframe to plot a chart - bar chart - with an x-axis of date and a y-axis of
#      'Total Volume'.
#   4. Save the chart as a *.svg file and *.pdf file.
for current_exercise in exercises:
    print("-" * 60)
    print(f"Processing Exercise {current_exercise}")
    selected_data = weight_training_data[weight_training_data["Exercise"] == current_exercise].copy()
    # Ensure Date is datetime
    selected_data["Date"] = pd.to_datetime(selected_data["Date"])
    # Sort by date
    selected_data = selected_data.sort_values("Date")

    selected_data["Reps"] = selected_data["Reps"].apply(lambda x: [int(i) for i in x.replace(" ", "").split(",")])
    selected_data["Weight"] = selected_data["Weight"].apply(
        lambda x: (
            [int(i) for i in x.replace(" ", "").split(",")]
            if x.replace(" ", "").replace(",", "").isdigit()
            else ['"Body Weight"']
        )
    )

# Build 'Volume Inputs' column
    selected_data["Volume Inputs"] = selected_data["Reps"].combine(
        selected_data["Weight"],
        lambda a, b: [[x, y] for x, y in zip(a, b)]
    )
# Build 'Total Volume' column
    selected_data["Total Volume"] = \
        selected_data["Volume Inputs"].apply(lambda sets: sum(int(r)* int(w) for r, w in sets))

# Create Stacked bar chart
# Set figure size — use plt.figure(figsize=(width, height)) before plotting. Width and height are in inches.
# Wider chart — increase the first value (e.g., figsize=(12,6)) to stretch horizontally.
# Taller chart — increase the second value (e.g., figsize=(8,10)) to stretch vertically.
# Consistent scaling — set a default figure size with plt.rcParams["figure.figsize"] = (12,6) so all charts use that size.
    plt.figure(figsize=(14, 6))
    plt.bar(selected_data["Date"], selected_data["Total Volume"], label="Total Volume")
    plt.title(f"Training Load per Exercise - {current_exercise} - (2 Sets)")
    plt.ylabel("Volume (lbs × reps × sets)")
    plt.xlabel("Date")
    plt.xticks(rotation=30)  # rotate labels for readability
    plt.tight_layout()
    plt.legend()

    # Output chart to a file or online
    if output_type == "file":
        # Save charts as *.svg and *.pdf files.   
        try:
            filename = f"training-load-for-{current_exercise.lower().replace(" ","-")}.svg"
            print(f"Creating {filename}")
            plt.savefig(filename)
            filename = f"training-load-for-{current_exercise.lower().replace(" ","-")}.pdf"
            print(f"Creating {filename}")
            plt.savefig(filename)
        except FileNotFoundError:
            print("Directory does not exist.")
        except PermissionError:
            print(f"No permission to write the {filename}.")
        except OSError as e:
            print(f"OS error occurred: {e}")
        finally:
            print(f"Files for execise {current_exercise} have been created.")
    else:
        # Generate image for chart.  
        print(f"Generating chart for {current_exercise}...")
        plt.show()

        