from rct229.ruletest_engine.ruletest_engine import *
from rct229.utils.natural_sort import natural_keys

TEST_PATH = "ruletest_jsons"

SECTION_5_ENVELOPE_TEST_PATH = "section5"
SECTION_6_LIGHTING_TEST_PATH = "section6"
SECTION_21_BOILER_TEST_PATH = "section21"
SECTION_22_CHILLER_TEST_PATH = "section22"
SECTION_23_AIRSIDE_TEST_PATH = "section23"


def run_transformer_tests():
    """Runs all tests found in the transformer tests JSON.

    Returns
    -------
    None

    Results of transformer test are spit out to console
    """

    transformer_rule_json = "transformer_tests.json"

    return run_section_tests(transformer_rule_json)


def run_lighting_tests():
    """Runs all tests found in the lighting tests JSON.

    Returns
    -------
    None

    Results of lighting test are spit out to console
    """

    json_tests = [
        os.path.join(SECTION_6_LIGHTING_TEST_PATH, pos_json)
        for pos_json in os.listdir(
            os.path.join(
                os.path.dirname(__file__), TEST_PATH, SECTION_6_LIGHTING_TEST_PATH
            )
        )
        if pos_json.endswith(".json")
    ]
    return run_test_helper(json_tests)


def run_envelope_tests():
    """Runs all tests found in the envelope tests JSON.

    Returns
    -------
    None

    Results of envelope stest are spit out to console
    """

    json_tests = [
        os.path.join(SECTION_5_ENVELOPE_TEST_PATH, pos_json)
        for pos_json in os.listdir(
            os.path.join(
                os.path.dirname(__file__), TEST_PATH, SECTION_5_ENVELOPE_TEST_PATH
            )
        )
        if pos_json.endswith(".json")
    ]
    return run_test_helper(json_tests)


def run_boiler_tests():
    """Runs all tests found in the boiler tests JSON

    Returns
    -------
    None

    Results of boiler test are spit out to console
    """
    json_tests = [
        os.path.join(SECTION_21_BOILER_TEST_PATH, pos_json)
        for pos_json in os.listdir(
            os.path.join(
                os.path.dirname(__file__), TEST_PATH, SECTION_21_BOILER_TEST_PATH
            )
        )
        if pos_json.endswith(".json")
    ]
    return run_test_helper(json_tests)


def run_receptacle_tests():
    """Runs all tests found in the receptacle tests JSON

    Returns
    -------
    None

    Results of receptacle test are spit out to console
    """
    receptacle_test_json = "receptacle_tests.json"
    return run_section_tests(receptacle_test_json)


def run_chiller_tests():
    """Runs all tests found in the chiller tests JSON

    Returns
    -------
    None

    Results of chiller test are spit out to console
    """
    json_tests = [
        os.path.join(SECTION_22_CHILLER_TEST_PATH, pos_json)
        for pos_json in os.listdir(
            os.path.join(
                os.path.dirname(__file__), TEST_PATH, SECTION_22_CHILLER_TEST_PATH
            )
        )
        if pos_json.endswith(".json")
    ]
    return run_test_helper(json_tests)


def run_airside_tests():
    """Runs all tests found in the airside tests JSON.

    Returns
    -------
    None

    Results of lighting test are spit out to console
    """

    json_tests = [
        os.path.join(SECTION_23_AIRSIDE_TEST_PATH, pos_json)
        for pos_json in os.listdir(
            os.path.join(
                os.path.dirname(__file__), TEST_PATH, SECTION_23_AIRSIDE_TEST_PATH
            )
        )
        if pos_json.endswith(".json")
    ]
    return run_test_helper(json_tests)


def run_test_helper(test_list):
    # sort the list in a human order
    test_list.sort(key=natural_keys)
    # all will short-circuit the tests - to avoid it, split the code into two lines.
    test_results = [run_section_tests(test_json) for test_json in test_list]
    return all(test_results)


# run_transformer_tests()
# run_lighting_tests()
# run_boiler_tests()
# run_chiller_tests()
# run_envelope_tests()
# run_receptacle_tests()
run_airside_tests()
