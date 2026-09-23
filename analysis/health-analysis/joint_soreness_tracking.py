"""
Script: joint_soreness_tracking.py
Purpose: This program generates line chart of Joint Soreness for a user-defined month. 
         The user selects the joint to display in the 'joints' variable described below. All
         data is extracted from the fitness-log.ods spreadsheet - sheet 'Daily_Health_Log'. Data 
         in the spreadsheet is for one calendar year. 
         User Set Variables:
         1. joints - a list of six joints that have ratings data where every joint is part of 
            a list of tuples where the user set the second tuple element to True or False to
            display on the chart.
         2. month_name - name of month to generate charts
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
if is_called_from_ai_agent:
    arguments = json.loads(sys.argv[1])
    joints = arguments["joints"]
else:
    joints = [("Shoulder",True),("Elbow",True),("Wrist",True),("Hip",True),("Knee",True),("Ankle",True)]

if is_called_from_ai_agent:
    arguments = json.loads(sys.argv[1])
    month_name = arguments["month_name"]
else:
    month_name = "August" # User sets the month name

if is_called_from_ai_agent:
    arguments = json.loads(sys.argv[1])
    output_type = arguments["output_type"]
else:
    output_type = "pdf" # User sets file (pdf, svg) or online
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
chart_year = daily_log_data["Date"].dt.year.unique()[0]

# Define your range
start_date = analytics.first_day_of_month(month_name, chart_year).strftime("%Y-%m-%d")
end_date = analytics.last_day_of_month(month_name, chart_year).strftime("%Y-%m-%d")

# Filter between start and end (inclusive)
chart_data = daily_log_data[(daily_log_data["Date"] >= start_date) & (daily_log_data["Date"] <= end_date)]

# Define the joint soreness columns to be extracted from dataframe 'chart_data'
soreness_columns = [f"{j[0]} Soreness" for j in joints if j[1]]

for column in soreness_columns:
    chart_data.loc[:, column] = chart_data[column].replace("N/A", 0)
    chart_data.loc[:, column] = chart_data[column].fillna(0)

# Extract columns from dataframe 'chart_data' to display on chart
joint_soreness = []
for column in soreness_columns:
    chart_dates = chart_data["Date"].tolist()
    [column, chart_data[column].tolist()]
    joint_soreness.append([column,chart_data[column].tolist()])

format_chart_dates = [chart_date.strftime("%B %d") for chart_date in chart_dates] 

# Build chart
plt.figure(figsize=(12, 6))
for joint in joint_soreness:
    plt.plot(format_chart_dates, joint[1], marker="o", label=joint[0])

# Define date range for title
if len(chart_dates) > 1:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")} -".strip() + " " + \
        f"{chart_dates[(len(chart_dates) - 1)].strftime("%B %d, %Y")}".strip()
    file_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%b-%d")
    file_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%b-%d")
    file_date = f"{file_start_date}" + "-" + f"{file_end_date}" 
else:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")}"
    file_date = f"{chart_dates[0].strftime("%Y-%b-%d")}"

x = np.arange(len(format_chart_dates)) 
plt.xticks(x, format_chart_dates, rotation=45)
plt.ylabel(f"Rating (1-10)")
plt.yticks(range(1,11))
plt.title(f"Joint Soreness: {date_range.strip()}")
plt.legend()
plt.tight_layout()

# Output chart to a file or online
if output_type in analytics.file_extensions:
    # Save charts as *.svg or *.pdf files.
    print("-" * 60)  
    try:
        name = f"{analytics.health_analysis_charts}joint-soreness-tracking-{file_date}".lower()
        filename = name + "." + output_type
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    print(f"File for {date_range} have been created.")
else:
    # Generate image for chart.
    print("-" * 60)  
    print(f"Generating chart for {date_range}...")
    plt.show()

