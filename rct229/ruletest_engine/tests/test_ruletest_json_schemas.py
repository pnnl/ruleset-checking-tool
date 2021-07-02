from rct229.ruletest_engine.ruletest_engine import *

test_json_dir = os.path.join(os.path.dirname(__file__), "..", "ruletest_jsons")

#envelope_json_path = os.path.join(test_json_dir, "envelope_tests_from_template.json")

def test_run_transformer_json_schema():

    transformer_json_path = os.path.join(test_json_dir, "transformer_tests.json")
    assert validate_test_json_schema(transformer_json_path)

def test_run_lighting_json_schema():

    lighting_json_path = os.path.join(test_json_dir, "lighting_tests.json")
    assert validate_test_json_schema(lighting_json_path)

# def test_run_envelope_json_schema():
#
#     assert validate_test_json_schema(envelope_json_path)
