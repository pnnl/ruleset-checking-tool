import glob
import pprint
from os.path import basename, dirname, join

import yaml

# A dictionary that will contain all the data in this folder
data = {}

# Get a list of the YAML file names in this folder
_yaml_paths = glob.glob(join(dirname(__file__), "*.yaml"))

# Import each YAML file and store the contents in data
for yaml_path in _yaml_paths:
    with open(yaml_path) as file:
        data[basename(yaml_path)[:-5]] = yaml.load(file, Loader=yaml.FullLoader)
