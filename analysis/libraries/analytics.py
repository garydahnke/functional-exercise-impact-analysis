scatter_markers = \
"""
🔹 Basic markers
"." → point
"," → pixel
"o" → circle
"v" → triangle down
"^" → triangle up
"<" → triangle left
">" → triangle right
"1" → tri-down (small)
"2" → tri-up (small)
"3" → tri-left (small)
"4" → tri-right (small)

🔹 Squares, diamonds, and stars
"s" → square
"p" → pentagon
"P" → plus (filled)
"*"→ star
"h" → hexagon1
"H" → hexagon2
"D" → diamond
"d" → thin diamond

🔹 Lines and crosses
"|" → vertical line
"_" → horizontal line
"+" → plus
"x" → cross (x-shape)
"X" → filled X
"""
joints = ["Shoulder", "Elbow", "Wrist", "Hip", "Knee", "Ankle"]
joints_to_chart = [("Shoulder",False),("Elbow",False),("Wrist",False),("Hip",False),("Knee",False),("Ankle",False)]
workout_types = ["CAR/Mobility","Tendon Training","Elliptical Cardio","Treadmill Cardio","Weight Training"]
health_analysis_charts = "charts/health-analysis/"
protein_consumption_charts = "charts/protein-consumption/"
weight_training_charts = "charts/weight-training/"
file_extensions = ["pdf", "svg"]
spreadsheet = "fitness-log.ods"
chart_month = "August"
chart_date = "2026-09-20"
chart_joints = [("Shoulder",True),("Elbow",True),("Wrist",True),("Hip",True),("Knee",True),("Ankle",True)]
chart_exercises = ["Leg Press", "Hamstring Curls", "Leg Extensions"]
chart_load_intensity_types = [("Average Intensity",True),("Total Intensity",True),("Total Volume",True)]
chart_file_type = "pdf"
chart_modules = [
        # Monthly Chart
        (0,"Flexibility vs Soreness Heatmap","flexibility_vs_soreness_heatmap.py",False,
         {"month_name":chart_month,"output_type":chart_file_type}),
        # One Day Chart
        (1,"Flexibility vs Soreness — Single‑Day Snapshot","flexibility_vs_soreness_single_day_snapshot.py",False,
         {"chart_date":chart_date,"output_type":chart_file_type}),
        # Week Range Chart
        (2,"Flexibility vs Soreness — Single-Joint Snapshot","flexibility_vs_soreness_single_joint_snapshot.py",False,
         {"start_date":"2026-09-13","joint":"shoulder","output_type":chart_file_type}),
        # Monthly Chart
        (3,"Joint Flexibility Tracking","joint_flexibility_tracking.py",False,
         {"joints":chart_joints,"month_name":chart_month,"output_type":chart_file_type}),
         # Monthly Chart
        (4,"Joint Health (Flexibility and Soreness)","joint_health_vs_muscle_soreness.py",False,
         {"joints":chart_joints,"month_name":chart_month,"output_type":chart_file_type}),
        # Monthly Chart
        (5,"Joint Soreness Tracking","joint_soreness_tracking.py",False,
         {"joints":chart_joints,"month_name":chart_month,"output_type":chart_file_type}),
        # Quarterly Chart - HTML Page 
        (6,"Load and Intensity Trends","load_and_intensity_monthly_trends.py",False,
         {"quarter":"3"}),
        # Monthly Chart  
        (7,"Protein Consumption","protein_consumption.py",False,
         {"month_name":chart_month,"output_type":chart_file_type}),
        # No Date Chart
        (8,"Training Load per Exercise","training_load_per_exercise.py",False,
         {"exercises":chart_exercises,"output_type":chart_file_type}),
        # Monthly Chart 
        (9,"Training Load vs Recovery","training_load_vs_recovery.py",False,
         {"month_name":chart_month,"date_annotation":"Y","output_type":chart_file_type}),
        # Monthly Chart
        (10,"Workout Tracking","workout_tracking.py",False,
         {"month_name":chart_month,"chart_type":"heatmap","output_type":chart_file_type})
                                   # heatmap (descending) or tracking (ascending)  
          ]
auxiliary_modules = [
        (0,"Generate Exercise List","generate_exercise_list.py",False),
        (1,"Create ReadME Appendencies","create_readme_appendices.py",False)
]

import calendar

def month_name_to_number(name: str) -> int:
    if len(name) == 3:
        return month_name_abbr_to_number(name)
    else:
        return month_name_full_to_number(name)

def month_name_full_to_number(name: str) -> int:
    # Normalize capitalization
    name = name.lower().capitalize()
    # Convert using lookup list
    return list(calendar.month_name).index(name)

def month_name_abbr_to_number(abbr: str) -> int:
    abbr = abbr.lower().capitalize()
    return list(calendar.month_abbr).index(abbr)

def show_scatter_marker():
    return scatter_markers

def format_joints_list(items):
    l = []
    for item in items:
        if not isinstance(item[0], str):
        # Raise a TypeError with a clear message
            raise TypeError(f"For list element {item}, the first value '{item[0]}' in the tuple must be a string, "
                            f"but got type '{type(item[0])}'.")
        else:
            l.append((item[0].lower().capitalize(),item[1]))
    return l

from datetime import datetime, date, timedelta
import calendar

def first_day_of_month(month_name: str, year: int) -> date:
    # Parse month name (handles both full and abbreviated names)
    month_num = datetime.strptime(month_name, "%b").month if len(month_name) == 3 \
                else datetime.strptime(month_name, "%B").month
    return date(year, month_num, 1)

def last_day_of_month(month_name: str, year: int) -> date:
    # Parse month name
    month_num = datetime.strptime(month_name, "%b").month if len(month_name) == 3 \
                else datetime.strptime(month_name, "%B").month
    # calendar.monthrange returns (weekday_of_first_day, number_of_days_in_month)
    last_day = calendar.monthrange(year, month_num)[1]
    return date(year, month_num, last_day)

def first_day_of_quarter(quarter: int, year: int) -> date:
    if quarter == 1:
        return first_day_of_month("January", year)
    elif quarter == 2:
        return first_day_of_month("April", year)
    elif quarter == 3:
        return first_day_of_month("July", year)
    elif quarter == 4:
        return first_day_of_month("October", year)

def last_day_of_quarter(quarter: int, year: int) -> date:
    if quarter == 1:
        return last_day_of_month("March", year)
    elif quarter == 2:
        return last_day_of_month("June", year)
    elif quarter == 3:
        return last_day_of_month("September", year)
    elif quarter == 4:
        return last_day_of_month("December", year)

from datetime import datetime
from zoneinfo import ZoneInfo

def get_current_et_timestamp():
    now_et = datetime.now(ZoneInfo("America/New_York"))
    return now_et.strftime("%Y-%m-%d %H:%M:%S ET")

def get_weight_training_exercises():
    return [e[0] for e in exercise_elements_list if e[3] == "Weight Training"]


# List generated by generate_exercise_data.py 
exercise_list = [
"Pull Ups",
"Rear Delt Flies",       
"Face Pulls",
"Side Delt Cable Raises",
"Side Delt Raises",      
"Tricep Extensions",
"Tricep Pulldowns",
"Back Extensions",
"Leg Press",
"Leg Extensions",
"Hamstring Curls",
"Calf Raises",
"Hip Thrusts",
"Pectoral Flies",
"Rows",
"Preacher Curls",
"Upright Cable Rows",
"Abdominal Cable Crunches",
"Hip Abduction",
"Hip Adduction",
"Chin Ups",
"Shoulder CARs",
"Hip CARs",
"Knee CARs",
"Ankle CARs",
"Wrist CARs",
"90/90 Hip Rotation Stretch",
"Hip Elliptical",
"Reverse Walking",
"Side Walking (Left and Right)",
"Deep Squat Hold",
"Goblet Squat Hold"    
]

# List generated by generate_exercise_data.py 
exercise_elements_list = [
('Pull Ups', 2.0, '', 'Weight Training', 'Y') ,
('Rear Delt Flies', 2.0, '', 'Weight Training', 'N') ,
('Face Pulls', 2.0, '', 'Weight Training', 'Y') ,
('Side Delt Cable Raises', 2.0, '', 'Weight Training', 'N') ,
('Side Delt Raises', 2.0, '', 'Weight Training', 'Y') ,
('Tricep Extensions', 2.0, '', 'Weight Training', 'N') ,
('Tricep Pulldowns', 2.0, '', 'Weight Training', 'Y') ,
('Back Extensions', 2.0, '', 'Weight Training', 'Y') ,
('Leg Press', 2.0, '', 'Weight Training', 'Y') ,
('Leg Extensions', 2.0, '', 'Weight Training', 'Y') ,
('Hamstring Curls', 2.0, '', 'Weight Training', 'Y') ,
('Calf Raises', 2.0, '', 'Weight Training', 'Y') ,
('Hip Thrusts', 2.0, '', 'Weight Training', 'Y') ,
('Pectoral Flies', 2.0, '', 'Weight Training', 'Y') ,
('Rows', 2.0, '', 'Weight Training', 'Y') ,
('Preacher Curls', 2.0, '', 'Weight Training', 'Y') ,
('Upright Cable Rows', 2.0, '', 'Weight Training', 'Y') ,
('Abdominal Cable Crunches', 2.0, '', 'Weight Training', 'Y') ,
('Hip Abduction', 2.0, '', 'Weight Training', 'Y') ,
('Hip Adduction', 2.0, '', 'Weight Training', 'Y') ,
('Shoulder CARs', 1.0, 5, 'CAR/Mobility', 'Y') ,
('Hip CARs', 1.0, 5, 'CAR/Mobility', 'Y') ,
('Knee CARs', 1.0, 10, 'CAR/Mobility', 'Y') ,
('Ankle CARs', 1.0, 30, 'CAR/Mobility', 'Y') ,
('Wrist CARs', 1.0, 30, 'CAR/Mobility', 'Y') ,
('90/90 Hip Rotation Stretch', 2.0, '94 minutes per hip', 'CAR/Mobility', 'Y') ,
('Assisted Squats', 2.0, 10, 'CAR/Mobility', 'Y') ,
('Lateral Step Ups', 2.0, '', 'CAR/Mobility', 'Y') ,
('Hip Elliptical', 1.0, '15 minutes', 'Elliptical Cardio', 'Y') ,
('Reverse Walking', 1.0, '15 minutes', 'Treadmill Cardio', 'Y') ,
('Side Walking (Left and Right)', 1.0, '5 minutes', 'Treadmill Cardio', 'Y') ,
('Deep Squat Hold', 2.0, '2 minutes', 'Tendon Training', 'Y') ,
('Goblet Squat Hold', 2.0, '1 minute', 'Tendon Training', 'Y')     
]