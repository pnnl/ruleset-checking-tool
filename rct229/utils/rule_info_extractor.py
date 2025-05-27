import os
import re
import csv

from rct229.utils.natural_sort import natural_keys

# Directory containing the Python files
DIRECTORY_LIST = [
    "../rulesets/ashrae9012019/section1",
    "../rulesets/ashrae9012019/section4",
    "../rulesets/ashrae9012019/section5",
    "../rulesets/ashrae9012019/section6",
    "../rulesets/ashrae9012019/section10",
    "../rulesets/ashrae9012019/section11",
    "../rulesets/ashrae9012019/section12",
    "../rulesets/ashrae9012019/section16",
    "../rulesets/ashrae9012019/section18",
    "../rulesets/ashrae9012019/section19",
    "../rulesets/ashrae9012019/section21",
    "../rulesets/ashrae9012019/section22",
    "../rulesets/ashrae9012019/section23",
]

# Regular expression patterns to match the required information
patterns = {
    "id": re.compile(r'id="([^"]+)"'),
    "description": re.compile(r'description="([^"]+)"'),
    "ruleset_section_title": re.compile(r'ruleset_section_title="([^"]+)"'),
    "standard_section": re.compile(r'standard_section="([^"]+)"'),
    "is_primary_rule": re.compile(r"is_primary_rule=(\w+)"),
}


def extract_info_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

        # Searching for the individual patterns and capturing the required data
        info = {}
        for key, pattern in patterns.items():
            match = pattern.search(content)
            if match:
                info[key] = match.group(1)

        # Ensuring all required keys are present
        if all(key in info for key in patterns.keys()):
            info["description"] = info["description"].replace(
                "\n", " "
            )  # Removing new line characters for the description
            return info

    return None


def main():
    extracted_data = []
    # Traversing through all files in the directory
    for directory in DIRECTORY_LIST:
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                file_path = os.path.join(directory, filename)
                info = extract_info_from_file(file_path)
                if info:
                    extracted_data.append(info)

    # Sorting the extracted data by the id field using natural order
    extracted_data.sort(key=lambda x: natural_keys(x["id"]))

    # Writing the extracted data to a CSV file
    with open("extracted_info.csv", "w", newline="") as csvfile:
        fieldnames = [
            "id",
            "description",
            "ruleset_section_title",
            "standard_section",
            "is_primary_rule",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in extracted_data:
            writer.writerow(data)


if __name__ == "__main__":
    main()
