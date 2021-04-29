from rct229.ruletest_engine.ruletest_engine import *

json_dir = os.path.join(os.path.dirname(__file__), 'ruletest_jsons')
envelope_json_path = os.path.join(json_dir, 'transformer_tests.json')

validate_test_json_schema(envelope_json_path)
