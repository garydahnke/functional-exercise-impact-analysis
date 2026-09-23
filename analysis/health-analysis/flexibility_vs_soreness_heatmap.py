"""
Script: flexibility_vs_soreness_heatmap.py
Purpose: This program generates two heatmaps (Flexibility Heatmap and Soreness Heatmap) for all joint
         for a user set month name or start date. The data is extracted from the fitness-log.ods 
         spreadsheet - sheet 'Daily_Health_Log'. Data in the spreadsheet is for one calendar year. 
         User Set Variables:
         1. month_name - name of month to generate charts
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
from datetime import datetime, timedelta
import seaborn as sns
import calendar
import sys, json

is_called_from_ai_agent = False
if len(sys.argv) > 1:
    is_called_from_ai_agent = True

"""
User Set Variables - Start
"""
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
month_number = datetime.strptime(month_name.strip(), "%B").month

# Retrieve all data from the 'Daily_Health_Log' sheet and load into a dataframe
sheet = "Daily_Health_Log"
try:
    daily_log_data = pd.read_excel(analytics.spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Create a list of columns with flexibility and soreness values to be extracted from
# the dataframe daily_log_data
joint_columns = [f"{joint} Flexibility" for joint in analytics.joints] + \
                [f"{joint} Soreness" for joint in analytics.joints]
for column in joint_columns:
    daily_log_data.loc[:, column] = daily_log_data[column].replace("N/A", 0)
    daily_log_data.loc[:, column] = daily_log_data[column].fillna(0)

month_number = datetime.strptime(month_name, "%B").month
daily_log_data = daily_log_data[daily_log_data["Date"].dt.month == month_number]

# Reconstruct the dataframe so the columns in the dataframe (Flexibility and Soreness ratings)
# are now row values and the Date column value are now the first row in the data frame     
rows = []
for _, row in daily_log_data.iterrows():
    date = row["Date"]
    axis_date = row["Date"].strftime("%b-%d")
    for joint in analytics.joints:
        flexibility_column = f"{joint} Flexibility"
        soreness_column = f"{joint} Soreness"
        rows.append({
            "Date": date,
            "Axis Date": axis_date,
            "Joint": joint,
            "Flexibility": row[flexibility_column],
            "Soreness": row[soreness_column]
        })
chart_data = pd.DataFrame(rows)

# Calulate minimum date and maximum date in the dataframe to be used in title and file names
min_date = chart_data["Date"].min()
max_date = chart_data["Date"].max()
title_date_range = f"{min_date.strftime("%B %d, %Y")} - {max_date.strftime("%B %d, %Y")}"
file_date_range = f"{min_date.strftime("%Y-%b-%d")}-{max_date.strftime("%Y-%b-%d")}"

# Create heatmap chart for Joint Soreness
# Pivot for soreness
soreness_matrix = chart_data.pivot(index="Joint", columns="Axis Date", values="Soreness")

title = f"Joint Soreness for {title_date_range}\n" + \
        f"Scale: 1 = No Soreness, 10 = Severe Soreness**"

plt.figure(figsize=(14, 8))
sns.heatmap(soreness_matrix, annot=True, cmap="Reds")
plt.xticks(rotation=45) 
plt.title(title)

# Output chart to a file or online
if output_type in analytics.file_extensions:
    # Save charts as *.svg or *.pdf files. 
    print("-" * 60)
    try:
        name = f"{analytics.health_analysis_charts}soreness-heatmap-for-{file_date_range}".lower()
        filename = name + "." + output_type
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    print(f"File for {file_date_range} have been created.")
else:
    # Generate image for chart. 
    print("-" * 60) 
    print(f"Generating chart for {title_date_range}...")
    plt.show()

# Create heatmap chart for Joint Flexibility
# Pivot for flexibility
flexibility_matrix = chart_data.pivot(index="Joint", columns="Axis Date", values="Flexibility")

title = f"Joint Flexibility for {title_date_range}\n" + \
        f"Scale: 1 = Limited Mobility, 10 = High Mobility**"

plt.figure(figsize=(14, 8))
sns.heatmap(flexibility_matrix, annot=True, cmap="Greens")
plt.xticks(rotation=45) 
plt.title(title)

# Output chart to a file or online
if output_type in analytics.file_extensions:
    # Save charts as *.svg or *.pdf files.    
    print("-" * 60)
    try:
        name = f"{analytics.health_analysis_charts}flexbility-heatmap-for-{file_date_range}".lower()
        filename = name + "." + output_type
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    print(f"File for {file_date_range} have been created.")
else:
    # Generate image for chart.
    print("-" * 60)  
    print(f"Generating chart for {title_date_range}...")
    plt.show()