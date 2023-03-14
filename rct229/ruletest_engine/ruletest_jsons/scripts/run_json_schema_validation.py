from rct229.ruletest_engine.ruletest_engine import *

test_json_name = "chiller_tests1.json"
dir_name = "ashrae9012019"
json_dir = os.path.join(os.path.dirname(__file__), "..", "..", "ruletest_jsons")
test_json_path = os.path.join(json_dir,dir_name, test_json_name)

validate_test_json_schema(test_json_path)
