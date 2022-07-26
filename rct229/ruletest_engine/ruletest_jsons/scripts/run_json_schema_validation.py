from rct229.ruletest_engine.ruletest_engine import *

test_json_name = "envelope_tests.json"

json_dir = os.path.join(os.path.dirname(__file__), "..", "..", "ruletest_jsons")
test_json_path = os.path.join(json_dir, test_json_name)

validate_test_json_schema(test_json_path)
