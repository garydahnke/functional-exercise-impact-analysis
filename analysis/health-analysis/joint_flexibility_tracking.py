"""
Script: joint-flexibility-tracking.py
Purpose: This program generates line chart of Joint Flexibility for a user-defined time frame. 
         The user selects the joint to display in the 'joints' variable described below. All
         data is extracted from the fitness-log.ods spreadsheet - sheet 'Daily_Health_Log'. Data 
         in the spreadsheet is for one calendar year. 
         User Set Variables:
         1. joints - a list of six joints that have ratings data where every joint is part of 
            a list of tuples where the user set the second tuple element to True or False to
            display on the chart.
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
joints = [("Shoulder",True),("Elbow",True),("Wrist",True), \
          ("Hip",True),("Knee",True),("Ankle",True)]
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

for column in flexibility_columns:
    chart_data.loc[:, column] = chart_data[column].replace("N/A", 0)
    chart_data.loc[:, column] = chart_data[column].fillna(0)

# Extract columns from dataframe 'chart_data' to display on chart
joint_flexibility = []
for column in flexibility_columns:
    chart_dates = chart_data["Date"].tolist()
    [column, chart_data[column].tolist()]
    joint_flexibility.append([column,chart_data[column].tolist()])

format_chart_dates = [chart_date.strftime("%B %d") for chart_date in chart_dates] 

# Build chart
plt.figure(figsize=(12, 6))
for joint in joint_flexibility:
    plt.plot(format_chart_dates, joint[1], marker="o", label=joint[0])

# Define date range for title
if len(chart_dates) > 1:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")} -".strip() + " " + \
        f"{chart_dates[(len(chart_dates) - 1)].strftime("%B %d, %Y")}".strip()
    file_date = f"{start_date.strftime("%Y-%b-%d")}" + "-" + f"{end_date.strftime("%Y-%B-%d")}" 
else:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")}"
    file_date = f"{chart_dates[0].strftime("%Y-%b-%d")}"

x = np.arange(len(format_chart_dates)) 
plt.xticks(x, format_chart_dates, rotation=45)
plt.ylabel(f"Rating (1-10)")
plt.yticks(range(1,11))
plt.title(f"Joint Flexibility: {date_range.strip()}")
plt.legend()
plt.tight_layout()

# Output chart to a file or online
if output_type == "file":
    # Save charts as *.svg and *.pdf files.
    print("-" * 60)
    file_date = start_date.strftime("%Y-%b-%d") + "-" + end_date.strftime("%Y-%b-%d")
    for extension in analytics.file_extensions:     
        try:
            name = f"{analytics.health_analysis_charts}joint-flexibility-tracking-{file_date}".lower()
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
    print(f"Generating chart for {date_range}...")
    plt.show()

