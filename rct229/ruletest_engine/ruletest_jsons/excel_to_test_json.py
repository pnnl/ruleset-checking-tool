import pandas as pd
import json
import math

from rct229.ruletest_engine.ruletest_jsons.json_generation_utilities import *

# Pull out TCDs from spreadsheet
master_df = pd.read_excel('test_generation_draft.xlsx', sheet_name='TCDs')

# Name of resulting JSON file
file_name = 'transformer_tests.json'

# Get headers to begin separating dictionary 'keys' from 'values'
headers = master_df.columns

# Get key values
keys = []

# If header has substring 'key', consider it a key
for header in headers:
    if 'key' in header:
        keys.append(header)

# Copy columns from the spreadsheet that correspond to keys
keys_df = master_df[keys].copy()

# Get values (i.e. not key values) from spreadsheet
values_df = master_df.drop(keys, axis=1)

# Begin putting together dictionary for JSON
json_dict = {}


# Iterate column by column through values_df
for (rule_name, columnData) in values_df.iteritems():

    # Array of this rule's column data
    rule_data_array = columnData.values

    # If rule doesnt exist in dictionary
    if rule_name not in json_dict:

        # Iterate through both keys and values
        for row_i in range(rule_data_array.size):

            row_value = rule_data_array[row_i]

            # Skip empty rows
            if not isinstance(row_value, str):
                if math.isnan(row_value):
                    continue

            # Get this rows vector of keys (e.g. ['applicability']['type'][NaN])
            key_vector = [rule_name]

            for key in keys:
                key_value = keys_df[key][row_i]
                if isinstance(key_value, str):
                    key_vector.append(key_value)

            # If the final key is DICT_LIST, parse the row value for the list of hashes
            if key_vector[-1] == 'DICT_LIST':
                row_value =  parse_string_to_dictionary_list(row_value)

                # Remove the DICT_LIST from key_vector
                key_vector.pop()

            # Set nested dictionary
            nested_dict(json_dict, key_vector, row_value)


# Dump JSON to string for writing
json_string = json.dumps(json_dict, indent=4)

# Write JSON string to file
with open(file_name, 'w') as json_file:
    json_file.write(json_string)
    print("JSON complete and written to file: " + file_name)



