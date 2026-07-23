"""
Script: flexibility-vs-soreness-single-day-snapshot.py
Purpose: This program generates side-by-side bar chart (Flexibility vs Soreness — Single-Joint 
         Snapshot) to compare the flexibility to soreness of a selected joint for seven days. All 
         data is extracted from the fitness-log.ods spreadsheet - sheet 'Daily_Health_Log'. Data 
         in the spreadsheet is for one calendar year. 
         User Set Variables:
         1. start_date - starting date of the data to be extracted
         2. joint - set the joint (Shoulder, Elbow, Wrist, Hip, Knee, Ankle) to generate a chart
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
from datetime import datetime, timedelta

"""
User Set Variables - Start
"""
start_date = pd.to_datetime("2026-07-14")
end_date = start_date + timedelta(days=7)
joint = "shoulder".lower().capitalize()
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

# Filter between start and end (inclusive)
chart_data = daily_log_data[(daily_log_data["Date"] >= start_date) & (daily_log_data["Date"] <= end_date)]

joint_columns = [f"{joint} Flexibility", f"{joint} Soreness"]
for column in joint_columns:
    chart_data.loc[:, column] = chart_data[column].replace("N/A", 0)
    chart_data.loc[:, column] = chart_data[column].fillna(0)

# Extract all dates and corresponding flexibility and soreness scores
chart_dates = chart_data["Date"].tolist()
joint_flexibility = chart_data[joint_columns[0]].tolist()
joint_soreness = chart_data[joint_columns[1]].tolist()


# Calculate vaiables for widthof bars
x = np.arange(len(chart_dates)) 
width = 0.35
plt.figure(figsize=(12, 6))

# Generate bars for joint flexibility and soreness
plt.bar(x - width/2, joint_flexibility, width, label=f"{joint} Flexibility", color="green")
plt.bar(x + width/2, joint_soreness, width, label=f"{joint} Soreness", color="red")
chart_dates_xticks = [chart_date.strftime("%B %d, %Y") for chart_date in chart_dates]
plt.xticks(x, chart_dates_xticks, rotation=45)
plt.ylabel(f"Rating (1-10)")
plt.yticks(range(1,11))
# Define date range for title
if len(chart_dates) > 1:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")} -".strip() + " " + \
        f"{chart_dates[(len(chart_dates) - 1)].strftime("%B %d, %Y")}".strip()
    file_date = f"{start_date.strftime("%Y-%b-%d")}" + "-" + f"{end_date.strftime("%Y-%b-%d")}" 
else:
    date_range = f"{chart_dates[0].strftime("%B %d, %Y")}"
    file_date = f"{chart_dates[0].strftime("%Y-%b-%d")}"
plt.title(f"{joint} Flexibility vs Soreness — Single Joint, Mulit‑Day Snapshot: {date_range.strip()}")
plt.legend()
plt.tight_layout()
    
# Output chart to a file or online
if output_type == "file":
    # Save charts as *.svg and *.pdf files.
    print("-" * 60)
    for extension in analytics.file_extensions:   
        try:
            name = f"{analytics.health_analysis_charts}flexibility-vs-soreness-{joint.lower()}-snapshot-{file_date}".lower()
            filename = name + extension
            print(f"Creating {filename}")
            plt.savefig(filename)  
        except FileNotFoundError:
            print("Directory does not exist.")
        except PermissionError:
            print(f"No permission to write the {filename}.")
        except OSError as e:
            print(f"OS error occurred: {e}")
    print(f"Files for {joint} Joint have been created.")
else:
    # Generate image for chart.
    print("-" * 60)  
    print(f"Generating chart for {joint} joint...")
    plt.show()
