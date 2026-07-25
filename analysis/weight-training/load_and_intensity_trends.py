"""
Script: load_and_intensity_trends.py
Purpose: This program generates Load and Intensity Trends chart for a selected or all exercises from 
         the "Workouts" sheet for each weight training sesssion. Total Volume shows how much work you 
         performed. Intensity shows how hard the work was.    
         Formulas:
            Total Volume = Σ(reps × weight)
            Total Intensity = Σ(reps × log(weight+1)
            Average Intensity = Total Intensity ÷ Sets 
         Intensity Score represents:
            -Strength progression
            -Hypertrophy stimulus
            -Neuromuscular demand
            -Training difficulty
         Total Volume = Summation (Reps * Weight) 
         Data is pulled from fitness-log.ods spreadsheet - sheet 'Workouts'. Data in the spreadsheet is 
         for one calendar year.
         User Set Variables:
         1. execises - a list of weight training exercise that the user wants to create charts. If the
            list is left, a default list of all weight training exercise will be processed
         2. start_date - starting date of the data to be extracted
         3. end_date - ending date of the data to be extracted
         4. chart_type - select which types of data points (Total Volume, Total Intensity, Average Intensity)
            to display on chart         
                 
Author: Gary Dahnke
Date: July 2026
"""
import os   
import pandas as pd
import matplotlib.pyplot as plt
import analytics
import math
import plotly.graph_objects as go

"""
User Set Variables - Start
"""
# To run one or more selected exercises, populate the list 'exercises'. Otherwise, the program will
# create a list with all exercises currently listed in the spreadsheet.
start_date = pd.to_datetime("2026-06-01")
end_date = pd.to_datetime("2026-07-24")
exercises = []
#exercises = ["Leg Press", "Hip Thrusts"]
exercises = ["Pectoral Flies", "Preacher Curls"]
chart_type = [("Average Intensity",True),("Total Intensity",True),("Total Volume",True)]
output_type = "file" # file or online
"""
User Set Variables - End
"""

# Retrieve all data from the 'Workouts' sheet and load into a dataframe.
sheet = "Workouts"
try:
    exercise_data = pd.read_excel(analytics.spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Retrieve all data from the 'Workouts' sheet for weight training and load into a dataframe.
weight_training_data = exercise_data.loc[(exercise_data["Workout Type"] == "Weight Training") & (exercise_data["Weight"] != "Body Weight"), \
    ["Date","Exercise","Sets","Reps","Weight","Workout Type"]].copy()

# Select the rows from the dataframe that are exercises in the list 'exercises'.
if len(exercises) == 0:
    exercises = list(weight_training_data["Exercise"].unique())

# Traverse through each exercise in the list to accomplish the following:
#   1. Set the flags for which types of data points will be display on the chart
#      (Total Volume, Total Intensity, Average Intensity)
#   2. Select all rows from the from the dataframe for the current exercise being processed
#      by the loop
#   2. Add new columns 'Volume Inputs' which is the pairing of 'Reps' and 'Weight as a list to
#      to become elements in another list. The 'Reps' and 'Weight' will be multipied together
#      to calculate three new column 'Total Volume', 'Total Intensity', 'Average Intensity'
#           Total Volume = Σ(reps × weight)
#           Total Intensity = Σ(reps × log(weight+1)
#           Average Intensity = Total Intensity ÷ Sets
#   3. Load the dataframe 'chart_data to plot a chart - bar chart - with an x-axis of date and a y-axis of
#      'Total Volume' and/or 'Total Intensity' and/or 'Average Intensity'
#   4. Generate the chart and save as a *.html file.
average_intensity = False      
for type in chart_type:
    if (type[0].lower().find("average intensity") != -1) and type[1]:
        average_intensity = True
        break
total_intensity = False 
for type in chart_type:
    if (type[0].lower().find("total intensity") != -1) and type[1]:
        total_intensity = True
        break
total_volume = False
for type in chart_type:
    if (type[0].lower().find("total volume") != -1) and type[1]:
        total_volume = True
        break

# Loop through each exercise and generate a chart via HTML.
for current_exercise in exercises:
    chart_data = weight_training_data[(weight_training_data["Exercise"] == current_exercise) & \
                 (weight_training_data["Date"] >= start_date) & \
                 (weight_training_data["Date"] <= end_date)].copy()
    # Ensure Date is datetime
    chart_data["Date"] = pd.to_datetime(chart_data["Date"])
    # Sort by date
    chart_data = chart_data.sort_values("Date")

    chart_start_date = chart_data["Date"].min()
    chart_end_date = chart_data["Date"].max()
 
    
    # Define date range for title
    if start_date != end_date:
        date_range = f"{start_date.strftime("%B %d, %Y")} -".strip() + " " + \
            f"{end_date.strftime("%B %d, %Y")}".strip()
        file_date = f"{start_date.strftime("%Y-%b-%d")}" + "-" + f"{end_date.strftime("%Y-%b-%d")}" 
    else:
        date_range = f"{start_date.strftime("%B %d, %Y")}"
        file_date = f"{start_date.strftime("%Y-%b-%d")}"

    chart_data["Reps"] = chart_data["Reps"].apply(lambda x: [int(i) for i in x.replace(" ", "").split(",")])
    chart_data["Weight"] = chart_data["Weight"].apply(
        lambda x: (
            [int(i) for i in x.replace(" ", "").split(",")]
            if x.replace(" ", "").replace(",", "").isdigit()
            else ['"Body Weight"']
        )
    )

    # Build 'Volume Inputs' column
    chart_data["Volume Inputs"] = chart_data["Reps"].combine(
        chart_data["Weight"],
        lambda a, b: [[x, y] for x, y in zip(a, b)]
    )
    # Build 'Total Volume' column
    chart_data["Total Volume"] = \
        chart_data["Volume Inputs"].apply(lambda sets: sum(int(r)* int(w) for r, w in sets))
    
    # Total Intensity Score=weight * log(reps + 1)    
    # Build 'Total Intensity' column
    chart_data["Total Intensity"] = \
        chart_data["Volume Inputs"].apply(lambda sets: sum(int(w)* math.log(int(r+1)) for r, w in sets))

    # Average Intensity Score=(weight * log(reps + 1))/2       
    # Build 'Average Intensity' column
    chart_data["Average Intensity"] = \
        chart_data["Total Intensity"] / chart_data["Sets"]
    
    chart_data["Hover Text"] = chart_data.apply(
            lambda row: (
            f"{row['Sets']} Sets "
            + "".join([f"[{r} reps x {w} lbs]" for r, w in row["Volume Inputs"]])
            ),
            axis=1
    ) 
   

    """
    Understanding the Object Hierarchy
    The power of graph_objects comes from its structure. A Figure is the top-level object.
    It has two main components: data and layout. The data property is a list of trace objects. Each trace is a 
    single data series (like a line or bar set).
    The layout object controls non-data elements. This includes titles, axes, legends, and annotations.
    This hierarchy is very flexible. You can think of a Figure as a complex nested data structure. You navigate 
    and modify its properties to build your ideal chart.
    """
    # Create a Figure object and add the trace (add_trace)
    fig = go.Figure()

    # Generate the line and data points for Total Intensity on the chart
    if total_intensity:
        fig.add_trace(go.Scatter(
            x=chart_data["Date"],
            y=chart_data["Total Intensity"],
            mode="lines+markers",
            name="Total Intensity = Σ(reps × log(weight+1)",
            marker=dict(color="blue", symbol="square"),
            text=chart_data["Hover Text"],       # annotation for each row
            hoverinfo="text",                    # show only custom text
            hovertext=chart_data["Hover Text"]   # ensures tooltip shows annotation
          ))

    # Generate the line and data points for Average Intensity on the chart
    if average_intensity:
        fig.add_trace(go.Scatter(
            x=chart_data["Date"],
            y=chart_data["Average Intensity"],
            mode="lines+markers",
            name="Average Intensity = Total Intensity ÷ Sets",
            marker=dict(color="green", symbol="diamond"),
            text=chart_data["Hover Text"],       # annotation for each row
            hoverinfo="text",                    # show only custom text
            hovertext=chart_data["Hover Text"]   # ensures tooltip shows annotation
        ))

    # Generate the line and data points for Total Volume on the chart
    if total_volume:
            fig.add_trace(go.Scatter(
            x=chart_data["Date"],
            y=chart_data["Total Volume"],
            mode="lines+markers",
            name="Total Volume = Σ(reps × weight)",
            marker=dict(color="red", symbol="circle"),
            text=chart_data["Hover Text"],       # annotation for each row
            hoverinfo="text",                    # show only custom text
            hovertext=chart_data["Hover Text"]   # ensures tooltip shows annotation
        ))

    if (total_volume and (average_intensity or total_intensity)):
        chart_type_title = "Volume & Intensity"
    elif (average_intensity or total_intensity):
        chart_type_title = "Intensity"  
    elif (total_volume):
        chart_type_title = "Volume"
    else:
        chart_type_title = "" 

    fig.update_layout(
        title=dict(
            text=f"Load and Intensity Trends For {current_exercise} - {date_range}",
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        title_font=dict(size=20, color="darkblue"),
        xaxis_title="Date",
        yaxis_title=f"{chart_type_title}",
        xaxis=dict(tickangle=90),
        legend=dict(x=0, y=1)
    )

    try:
        filename = f"{analytics.weight_training_charts}load-and-intensity-trends-for" \
                   f"-{current_exercise.lower().replace(" ","-")}-for-{file_date.lower()}.html"
        print(f"Creating {filename}")
        fig.write_html(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    print(f"File - Load and Intensity Trends for {current_exercise.lower().title()} for {date_range} has been created.")
