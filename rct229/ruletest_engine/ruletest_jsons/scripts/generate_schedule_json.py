import json
import os

import pandas as pd

# ---------------------------------------USER INPUTS---------------------------------------

spreadsheet_name = "schedule_datasets.xlsx"
json_name = "schedule_library.json"
schedule_set_name = "Office"  # TODO: TEMPORARY, should cycle through them later

# --------------------------------------SCRIPT STARTS--------------------------------------

schedule_json_dict = {}  # Dict used to store all 8760 schedules
schedule_types = [
    "Occupancy",
    "Lighting",
    "Equipment",
    "Heating_Setpoint",
    "Cooling_Setpoint",
]

file_dir = os.path.dirname(__file__)

# Define output json file path
json_file_path = os.path.join(file_dir, "resources", json_name)

# Define schedule spreadsheet path
spreadsheet_path = os.path.join(file_dir, "resources", spreadsheet_name)

schedule_df = pd.read_excel(spreadsheet_path, sheet_name=schedule_set_name)

# Dict used to store 24 hour schedules, format: schedule_dict{SCHEDULE_NAME} = [1..24]
schedule_dict = {}

# Iterate column by column through values_df
for schedule_name, column_data in schedule_df.items():
    # Skip Hour column, not relevant
    if schedule_name == "Hour":
        continue

    # List of this schedule's column data
    schedule_value_list = column_data.values

    schedule_dict[schedule_name] = schedule_value_list

# Cycle through each schedule type and stitch together weekdays, Saturday, and Sunday schedules
for schedule_type in schedule_types:

    # Initialize schedule names
    year_schedule_name = f"{schedule_set_name}_{schedule_type}"

    weekday_schedule_name = f"{year_schedule_name}_Weekday"
    saturday_schedule_name = f"{year_schedule_name}_Saturday"
    sunday_schedule_name = f"{year_schedule_name}_Sunday"

    # Initialize the three week day types
    weekday_schedule = schedule_dict[weekday_schedule_name].tolist()
    saturday_schedule = schedule_dict[saturday_schedule_name].tolist()
    sunday_schedule = schedule_dict[sunday_schedule_name].tolist()

    # Combine all week schedules into 7 day schedule
    week_schedule = sunday_schedule + weekday_schedule * 5 + sunday_schedule

    # Year is 52 weeks + 1 day = 8760 hours
    year_schedule = week_schedule * 52 + weekday_schedule

    schedule_json_dict[year_schedule_name] = year_schedule

    # Also add 24 hour schedules
    schedule_json_dict[weekday_schedule_name] = weekday_schedule
    schedule_json_dict[saturday_schedule_name] = saturday_schedule
    schedule_json_dict[sunday_schedule_name] = sunday_schedule

# -------Add monthly fractional values required by rule 12-4 --------

# Define the values for each month
monthly_values = [0.25, 0.5, 0.75, 1, 0.25, 0.5, 0.75, 1, 0.25, 0.5, 0.75, 1]

# Define the number of days in each month (non-leap year)
days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Calculate the number of hours in each month
hours_in_month = [days * 24 for days in days_in_month]

# Create the 8760 array
hourly_fractional_schedule = []

for month, hours in zip(monthly_values, hours_in_month):
    hourly_fractional_schedule.extend([month] * hours)

schedule_json_dict["Monthly_Fractional_Schedule"] = hourly_fractional_schedule

# ------END: Add monthly fractional values required by rule 12-4 --------

# Dump JSON to string for writing
json_string = json.dumps(schedule_json_dict, indent=4)

# Write JSON string to file
with open(json_file_path, "w") as json_file:
    json_file.write(json_string)
    print("JSON complete and written to file: " + json_name)
