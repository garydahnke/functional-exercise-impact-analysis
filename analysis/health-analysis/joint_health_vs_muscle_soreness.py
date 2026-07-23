"""
Script: joint_health_vs_muscle_soreness.py
Purpose: This program generates a chart of that displays a daily  Joint Health (Flexibility and Soreness) 
         scores compared to muscle soreness scores for a user-defined time frame. All data is 
         extracted from the fitness-log.ods spreadsheet - sheet 'Daily_Health_Log'. Data in the 
         spreadsheet is for one calendar year. 
         User Set Variables:
         1. joints - a list of one to six joints that have ratings data where every joint is part of 
            a list of tuples where the user set the second tuple element to True or False to
            create a chart
         2. start_date - starting date of the data to be extracted
         3. end_date - ending date of the data to be extracted
         4. output_type - a flag to define the type of output for the chart 
            options: file or online          
Author: Gary Dahnke
Date: July 2026
"""
import os   
import pandas as pd
import matplotlib.pyplot as plt
import analytics
import numpy as np

"""
User Set Variables - Start
"""
spreadsheet = "fitness-log.ods"
#joints = analytics.format_joints_list( \
#    [("shoulder",True),("elbow",True),("wrist",True), \
#     ("hip",True),("knee",True),("ankle",True)] \
#    )
joints = analytics.format_joints_list( \
    [("shoulder",True),("elbow",True),("wrist",True), \
     ("hip",False),("knee",False),("ankle",False)] \
    )
start_date = pd.to_datetime("2026-07-01")
end_date = pd.to_datetime("2026-07-22")
output_type = "file" # file or online
"""
User Set Variables - End
"""
# Retrieve all data from the 'Daily_Health_Log' sheet and load into a dataframe
sheet = "Daily_Health_Log"
try:
    daily_log_data = pd.read_excel(analytics.spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Ensure the column is datetime
daily_log_data["Date"] = pd.to_datetime(daily_log_data["Date"])

# Define your range
start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)

# Filter between start and end (inclusive)
chart_data = daily_log_data[(daily_log_data["Date"] >= start) & (daily_log_data["Date"] <= end)]

# Define the joint flexibility columns to be extracted from dataframe 'chart_data'
flexibility_columns = [f"{j[0]} Flexibility" for j in joints if j[1]]
soreness_columns = [f"{j[0]} Soreness" for j in joints if j[1]]

for column in flexibility_columns:
    chart_data.loc[:, column] = chart_data[column].replace("N/A", 0)
    chart_data.loc[:, column] = chart_data[column].fillna(0)
for column in soreness_columns:
    chart_data.loc[:, column] = chart_data[column].replace("N/A", 0)
    chart_data.loc[:, column] = chart_data[column].fillna(0)

chart_dates = chart_data["Date"].tolist()

# Define date range for title
if len(chart_dates) > 1:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")} -".strip() + " " + \
        f"{chart_dates[(len(chart_dates) - 1)].strftime("%B %d, %Y")}".strip()
    file_date = f"{start_date.strftime("%Y-%b-%d")}" + "-" + f"{end_date.strftime("%Y-%b-%d")}" 
else:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")}"
    file_date = f"{chart_dates[0].strftime("%Y-%b-%d")}"

for joint in [j[0] for j in joints if j[1]]:
    # Plot chart
    plt.figure(figsize=(12,6))
    # Load data for all dates in the chart from chart_data
    plt.plot(chart_data["Date"], chart_data["Muscle Soreness"], label="Daily Muscle Soreness (1-10)")
    plt.scatter(chart_data["Date"], chart_data["Muscle Soreness"],
                c="blue", label="Muscle Soreness Score", marker="s")
    column = [fc for fc in flexibility_columns if fc.lower().startswith(joint.lower())]    
    plt.scatter(chart_data["Date"], chart_data[column[0]],
                c="green", label=f"{column[0]} Score", marker="^")
    column = [fc for fc in soreness_columns if fc.lower().startswith(joint.lower())]
    plt.scatter(chart_data["Date"], chart_data[column[0]],
                c="red", label=f"{column[0]} Score", marker="v")
    plt.title(f"{joint} Joint Health vs. Muscle Soreness - {date_range}")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Low        -        Soreness (1-10)        -       High")
    plt.yticks(range(1,11))
    plt.tight_layout()
    plt.legend()
    
    # Output chart to a file or online
    if output_type == "file":
        # Save charts as *.svg and *.pdf files. 
        print("-" * 60)
        for extension in analytics.file_extensions:     
            try:
                name = f"{analytics.health_analysis_charts}{joint.lower()}-joint-health-vs-muscle-soreness-for-{file_date}".lower()
                filename = name + extension
                print(f"Creating {filename}")
                plt.savefig(filename)   
            except FileNotFoundError:
                print("Directory does not exist.")
            except PermissionError:
                print(f"No permission to write the {filename}.")
            except OSError as e:
                print(f"OS error occurred: {e}")
        print(f"Files for {date_range} have been created.")
    else:
        # Generate image for chart.  
        print("-" * 60)
        print(f"Generating chart for {joint} Health for {date_range}...")
        plt.show()
