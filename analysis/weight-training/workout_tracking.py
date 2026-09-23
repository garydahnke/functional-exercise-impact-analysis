"""
Script: workout_tracking.py
Purpose: This program generates a chart to track the daily workout types based on data from
         fitness-log.ods spreadsheet - sheet 'Workous'. The user can set the chart type as  
         'heatmap' to display workout frequency in descending order or 'tracking' to display
         workout frequency in ascending order as well as the start and end dates of data to extract.
         User Set Variables:
         1. month_name - name of month to generate charts
         2. chart_type - heatmap (descending) or tracking (ascending)
         3. output_type - a flag to define the type of output for the chart 
            options: file or online          
Author: Gary Dahnke
Date: July 2026
"""
import os   
import pandas as pd
import matplotlib.pyplot as plt
import analytics
import numpy as np
import sys, json
from datetime import datetime

is_called_from_ai_agent = False
if len(sys.argv) > 1:
    is_called_from_ai_agent = True

"""
User Set Variables - Start
"""
# To run one or more selected exercises, populate the list 'exercises'. Otherwise, the program will
# create a list with all exercises currently listed in the spreadsheet.
if is_called_from_ai_agent:
    arguments = json.loads(sys.argv[1])
    month_name = arguments["month_name"]
else:
    month_name = "August" # User sets the month name

if is_called_from_ai_agent:
    arguments = json.loads(sys.argv[1])
    chart_type = arguments["chart_type"]
else:
    chart_type = "tracking" # heatmap (descending) or tracking (ascending)

if is_called_from_ai_agent:
    arguments = json.loads(sys.argv[1])
    output_type = arguments["output_type"]
else:
    output_type = "pdf" # User sets file (pdf, svg) or online
"""
User Set Variables - End
"""
# Retrieve all data from the 'Workouts' sheet and load into a dataframe
sheet = "Workouts"
try:
    exercise_data = pd.read_excel(analytics.spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Define date range
chart_year = exercise_data["Date"].dt.year.unique()[0]
start_date = analytics.first_day_of_month(month_name, chart_year).strftime("%Y-%m-%d")
end_date = analytics.last_day_of_month(month_name, chart_year).strftime("%Y-%m-%d")

# Retrieve data from the 'Workouts' sheets and load into a dataframe dropping any duplicate data
# for a specific date range.
workout_type_data = exercise_data.loc[(exercise_data["Date"] >= start_date) & (exercise_data["Date"] <= end_date), \
                                      ["Date","Workout Type"]].drop_duplicates().copy()
workout_type_data["Formatted Date"] = pd.to_datetime(workout_type_data["Date"]).dt.strftime("%B %d")

# Separate data from 'workout_type_data' dataframe by Workout Type into separate dataframes
workout_type_rank = []
plt.figure(figsize=(10,6))
for type in analytics.workout_types:
    match type:
        case "CAR/Mobility":
            df_car_mobility = workout_type_data.loc[workout_type_data["Workout Type"] == type].copy()
            workout_type_rank.append((type,len(df_car_mobility)))
        case "Tendon Training":
            df_tendon_training = workout_type_data.loc[workout_type_data["Workout Type"] == type].copy()
            workout_type_rank.append((type,len(df_tendon_training)))
        case "Elliptical Cardio":
            df_elliptical_cardio = workout_type_data.loc[workout_type_data["Workout Type"] == type].copy()
            workout_type_rank.append((type,len(df_elliptical_cardio)))
        case "Treadmill Cardio":
            df_treadmill_cardio = workout_type_data.loc[workout_type_data["Workout Type"] == type].copy()
            workout_type_rank.append((type,len(df_treadmill_cardio)))
        case "Weight Training":
            df_weight_training = workout_type_data.loc[workout_type_data["Workout Type"] == type].copy()
            workout_type_rank.append((type,len(df_weight_training)))

# Sort the 'Workout Type' in ascending or descending order for the total occurences of each 
# 'Workout Type'
if chart_type == "heatmap":
    workout_type_rank_sorted = sorted(workout_type_rank, key=lambda x: x[1], reverse=False)
else:
    workout_type_rank_sorted = sorted(workout_type_rank, key=lambda x: x[1], reverse=True)

# Plot the scatter points for each 'Workout Type' as sorted the statement above
for type in workout_type_rank_sorted:
    match type[0]:
        case "CAR/Mobility":
            plt.scatter(df_car_mobility["Formatted Date"], df_car_mobility["Workout Type"], marker="o")
        case "Tendon Training":
            plt.scatter(df_tendon_training["Formatted Date"], df_tendon_training["Workout Type"], marker="s")
        case "Elliptical Cardio":
            plt.scatter(df_elliptical_cardio["Formatted Date"], df_elliptical_cardio["Workout Type"], marker="^")
        case "Treadmill Cardio":
            plt.scatter(df_treadmill_cardio["Formatted Date"], df_treadmill_cardio["Workout Type"], marker="v")
        case "Weight Training":
            plt.scatter(df_weight_training["Formatted Date"], df_weight_training["Workout Type"], marker="*")

# Define date range for title
file_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%b-%d")
file_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%b-%d")
file_date = f"{file_start_date}" + "-" + f"{file_end_date}"
date_range_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%B %d, %Y")
date_range_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%B %d, %Y")
date_range = f"{date_range_start_date} - {date_range_end_date}"
 
plt.title(f"Daily Workout {chart_type.lower().capitalize()} For {date_range}")
plt.xlabel("Date")
x = np.arange(len(workout_type_data["Formatted Date"].unique())) 
plt.xticks(x, workout_type_data["Formatted Date"].unique(), rotation=45)
plt.ylabel("Workout Tracking ")
plt.grid(axis="x")
plt.tight_layout()

# Output chart to a file or online
if output_type in analytics.file_extensions:
    # Save charts as *.svg or *.pdf files.
    print("-" * 60)   
    try:
        name = f"{analytics.weight_training_charts}workout-{chart_type.lower()}-for-{file_date.lower()}"
        filename = name + "." + output_type
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    print(f"File for {file_date} have been created.")
else:
    # Generate image for chart.
    print("-" * 60)  
    print(f"Generating chart for {date_range}...")
    plt.show()
