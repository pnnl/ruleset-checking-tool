import glob
import json
import pprint
from os.path import basename, dirname, join

# A dictionary that will contain all the data in this folder
data = {}

# Get a list of the JSON file names in this folder
_json_paths = glob.glob(join(dirname(__file__), "*.json"))

# Import each JSON file and store the contents in data
for json_path in _json_paths:
    with open(json_path) as file:
        data[basename(json_path)[:-5]] = json.load(file)
