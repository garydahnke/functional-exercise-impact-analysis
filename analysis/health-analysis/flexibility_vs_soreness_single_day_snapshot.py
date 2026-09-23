"""
Script: flexibility_vs_soreness_single_day_snapshot.py
Purpose: This program generates side-by-side bar chart (Flexibility vs Soreness — Single‑Day 
         Snapshot) to compare the flexibility to soreness of all joints for one day. All data is 
         extracted from the fitness-log.ods spreadsheet - sheet 'Daily_Health_Log'. Data in the 
         spreadsheet is for one calendar year. A user can generate a chart for multiple days is
         possible.
         User Set Variables:
         1. chart_date - starting date of the data to be extracted
         2. output_type - a flag to define the type of output for the chart 
            options: file (pdf, svg) or online         
Author: Gary Dahnke
Date: July 2026
"""
import os   
import pandas as pd
import matplotlib.pyplot as plt
import analytics
import numpy as np
import sys, json

is_called_from_ai_agent = False
if len(sys.argv) > 1:
    is_called_from_ai_agent = True

"""
User Set Variables - Start
"""
if is_called_from_ai_agent:
    arguments = json.loads(sys.argv[1])
    chart_date = arguments["chart_date"]
else:
    chart_date = "2026-08-15" # User sets chart_date YYYY-MM-DD format
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

# Filter between start and end (inclusive)
chart_data = daily_log_data[daily_log_data["Date"] == pd.to_datetime(chart_date)]

for date in chart_data["Date"]:
    file_date = date.strftime("%Y-%b-%d")
    chart_date = date.strftime("%B %d, %Y")
    # Define joints and pair columns
    joints = ["Shoulder", "Elbow", "Wrist", "Hip", "Knee", "Ankle"]

    flexibility_columns = [f"{j} Flexibility" for j in analytics.joints]
    soreness_columns = [f"{j} Soreness" for j in analytics.joints]
    chart_columns = flexibility_columns + soreness_columns

    # Replace all column values of 'N/A' and 'Nan' for the column names generated in chart_columns
    # with 0
    for column in chart_columns:
        chart_data.loc[:, column] = chart_data[column].replace("N/A", 0)
        chart_data.loc[:, column] = chart_data[column].fillna(0)

    x = np.arange(len(joints))
    width = 0.35
    plt.figure(figsize=(12, 6))

    # Assume df has one row for the day
    row = chart_data.iloc[0]

    # Generates flexibility and soreness value to display on charts
    flexibility_values = [row[c] for c in flexibility_columns]
    soreness_values = [row[c] for c in soreness_columns]

    # Generate side-by-side bar chart
    # Generate bars for joint flexibility and soreness
    plt.bar(x - width/2, flexibility_values, width, label="Flexibility", color="green")
    plt.bar(x + width/2, soreness_values, width, label="Soreness", color="red")
    plt.xticks(x, joints)
    plt.ylabel(f"Rating (1-10)")
    max_joint_value = int(max(flexibility_values + soreness_values))
    plt.yticks(range(1,11))
    plt.title(f"Flexibility vs Soreness — Single‑Day Snapshot for {date.strftime("%B %d, %Y")}")
    plt.legend()
    plt.tight_layout()
    
    # Output chart to a file or online
    if output_type in analytics.file_extensions:
        # Save charts as *.svg or *.pdf files.
        print("-" * 60)
        try:
            name = f"{analytics.health_analysis_charts}flexibility-vs-soreness-single-day-snapshot-{file_date}".lower()
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
        print(f"Generating chart for {file_date}...")
        plt.show()
