"""
Script: monthly_muscle_soreness_tracking.py
Purpose: This program generates a monthly Training Load vs. Recovery chart based on data from
         fitness-log.ods spreadsheet - sheet 'Daily_Health_Log'. The user can select one or more 
         month within the same calendar year.
         User Set Variables:
         1. spreadsheet - fitness log spreadsheet
         2. month_name_list - a list of months to generate charts
         3. date_annotation -  a flag to display the date of each data point on the char
            options: Y or N
         4. output_type - a flag to define the type of output for the chart 
            options: file or online
Author: Gary Dahnke
Date: July 2026
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import calendar
import analytics

"""
User Set Variables - Start
"""
# Fitness Log Spreadsheet
spreadsheet = "fitness-log.ods"
month_name_list = []
# month_name_list = ["May","June","July"]
# month_name_list = ["May","June"]
month_number_list = []
if len(month_name_list) > 0:
    month_number_list = [datetime.datetime.strptime(month_name, "%B").month  \
                        for month_name in month_name_list]
# Display dates on chart
date_annotation = "Y"
output_type = "file" # file or online
"""
User Set Variables - End
"""

# Retrieve all data from the 'Workouts' sheet and load into a dataframe.
sheet = "Workouts"
try:
    workout_data = pd.read_excel(spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Retrieve the year of the data on the sheet into a dataframe
year = str(workout_data["Date"].dt.year.unique()[0])    
if len(month_number_list) == 0:
    month_number_list = list(workout_data["Date"].dt.month.unique()) 

# Retrieve a exercises that are of type 'Weight Training' into a dataframe
weight_train_dates = workout_data.loc[workout_data["Workout Type"] == "Weight Training","Date"].unique()
    
# Select dates with weight training into a dataframe
weight_training_data = workout_data.loc[workout_data["Date"].isin(weight_train_dates),["Date"]].copy()
weight_training_data.drop_duplicates(inplace=True)
weight_training_data["Workout Type"] = "Weight Training"
# Select dates with no weight training into a dataframe
other_training_data = workout_data.loc[~workout_data["Date"].isin(weight_train_dates),["Date"]].copy()
other_training_data.drop_duplicates(inplace=True)
other_training_data["Workout Type"] = "No Weight Training"
# Concatente the two dataframes into a single dataframe to be used to match against data from the
# 'Daily_Health_Log'
training_data = pd.concat([weight_training_data,other_training_data])

# Retrieve all data from the 'Daily_Health_Log' sheet and load into a dataframe
sheet = "Daily_Health_Log"
try:
    daily_log_data = pd.read_excel(spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# shift(-1) takes Wednesday’s soreness and places it on Tuesday’s row.  
# That’s exactly what you need when comparing training on Day N → soreness on Day N+1.
# -Row shifting — Moves data up or down without changing the index.
# -Negative shift — -1 means “move values up one row.”
# -Lag alignment — Aligns a future measurement (soreness) with a past event (training).
muscle_soreness_data = daily_log_data[["Date","Muscle Soreness"]].copy().shift(+1)

# Merge the dataframe with muscle soreness data with the dataframe that list weight training and
# non-weight training dates
merged_data = pd.merge(
    muscle_soreness_data,
    training_data,
    on="Date",
    how="inner"
)

# Process each month of data to create the charts as files or display online 
for month_number in month_number_list:
    month_name = calendar.month_name[month_number]
    # Load all the data for the month select from the intial dataframe
    chart_data=merged_data.loc[merged_data["Date"].dt.month == month_number, \
        ["Date","Workout Type","Muscle Soreness"]]

    # Split all date into days when weight training occured and did not occur
    weight_train_chart_data=chart_data.loc[chart_data["Workout Type"] == "Weight Training", \
        ["Date","Workout Type","Muscle Soreness"]]
    no_weight_train_chart_data=chart_data.loc[chart_data["Workout Type"] == "No Weight Training", \
        ["Date","Workout Type","Muscle Soreness"]]

    # Plot chart
    plt.figure(figsize=(12,6))
    # Load data for all dates in the chart from chart_data
    plt.plot(chart_data["Date"], chart_data["Muscle Soreness"], label="Daily Muscle Soreness (1-10)")

    # Load data for all dates when weight training occured
    plt.scatter(weight_train_chart_data["Date"], weight_train_chart_data["Muscle Soreness"],
                c="red", label="Weight Training", marker="o")
    # Load data for all dates when no weight training occured
    plt.scatter(no_weight_train_chart_data["Date"], no_weight_train_chart_data["Muscle Soreness"],
                c="green", label="No Weight Training", marker="o")

    # Display the month and day as an annotation if selected
    if (date_annotation.casefold() == "y"):
        for date, soreness in zip(weight_train_chart_data["Date"], weight_train_chart_data["Muscle Soreness"]):
            plt.annotate(f"{date.strftime("%b-%d")}",
                        xy=(date, soreness),
                        xytext=(0,-15),  # offset text upward
                        textcoords="offset points",
                        ha="center",
                        color="red")
        for date, soreness in zip(no_weight_train_chart_data["Date"], no_weight_train_chart_data["Muscle Soreness"]):
            plt.annotate(f"{date.strftime("%b-%d")}",
                        xy=(date, soreness),
                        xytext=(0,-15),  # offset text upward
                        textcoords="offset points",
                        ha="center",
                        color="green")   

    plt.title(f"Training Load vs. Recovery - {month_name} {year}")
    plt.xlabel("Date")
    plt.ylabel("Low     -     Muscle Soreness on Next Day     -     High")
    plt.yticks(range(1,11))
    plt.tight_layout()
    plt.legend()
    plt.xticks(rotation=30)

    # Output chart to a file or online
    if output_type == "file":
        # Save charts as *.svg and *.pdf files.    
        try:
            print("-" * 60)
            filename = f"{analytics.health_analysis_charts}training-load-vs-recovery-for-{year}-{month_name.lower()}.svg"
            print(f"Creating {filename}")
            plt.savefig(filename)
            filename = f"{analytics.health_analysis_charts}training-load-vs-recovery-for-{year}-{month_name.lower()}.pdf"
            print(f"Creating {filename}")
            plt.savefig(filename)
        except FileNotFoundError:
            print("Directory does not exist.")
        except PermissionError:
            print(f"No permission to write the {filename}.")
        except OSError as e:
            print(f"OS error occurred: {e}")
        finally:
            print(f"Files for {month_name} of {year} have been created.")
    else:
        # Generate image for chart.  
        print("-" * 60)
        print(f"Generating chart for {month_name} of {year}...")
        plt.show()
