from enum import Enum
from jsonpath_ng import jsonpath, parse
import json
from os.path import dirname, join



_rmr_schema_path = join(dirname(__file__), '..', 'schema', 'rmr_schema.json')
with open(_rmr_schema_path) as schema_file:
    schema_obj = json.load(schema_file)

# Query for all objects having an enum field
_matches = parse('$..* where enum').find(schema_obj)

_enum_objs = {
    str(match.full_path).split('.')[-1]:
        dict((key, value) for key, value in zip(match.value['enum'], match.value['enum_text']))
    for match in parse('$..* where enum').find(schema_obj)
}

# Export all the enumerations from the schema
schema_enums = { key: Enum(key, enum_dict) for key, enum_dict in _enum_objs.items() }
