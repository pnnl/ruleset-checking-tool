from rct229.rule_engine.rulesets import RuleSet, RuleSetTest
from rct229.ruletest_engine.ruletest_engine import *
from rct229.utils.natural_sort import natural_keys

TEST_PATH = "ruletest_jsons"


def run_ashrae9012019_tests(section=None):
    """
    Run ruleset by section or all
    If section is None, then this function runs all the rule sections

    Parameters
    ----------
    section: str - it should be the same string in the ASHRAE9012019_TEST_PATH_LIST

    Returns
    -------

    """
    return [
        run_test_helper(
            _helper_get_all_test_file_by_section(
                RuleSet.ASHRAE9012019_RULESET, test_section
            ),
            RuleSet.ASHRAE9012019_RULESET,
        )
        for test_section in RuleSetTest.ASHRAE9012019_TEST_LIST
        if section is None or test_section == section
    ]


def _helper_get_all_test_file_by_section(ruleset: str, path: str):
    """
    Helper function to retrieve the list of test files by ruleset and the sections
    Parameters
    ----------
    ruleset: str
    path: str

    Returns list of strings contains the pathes to each of the test json file
    -------

    """
    return [
        os.path.join(ruleset, path, pos_json)
        for pos_json in os.listdir(
            os.path.join(
                os.path.dirname(__file__),
                TEST_PATH,
                ruleset,
                path,
            )
        )
        if pos_json.endswith(".json")
    ]


def run_lighting_tests():
    """Runs all tests found in the lighting tests JSON.
    Returns
    -------
    None
    Results of lighting test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section6"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_envelope_tests():
    """Runs all tests found in the envelope tests JSON.
    Returns
    -------
    None
    Results of envelope stest are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section5"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_boiler_tests():
    """Runs all tests found in the boiler tests JSON
    Returns
    -------
    None
    Results of boiler test are spit out to console
    """
    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section21"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_chiller_tests():
    """Runs all tests found in the chiller tests JSON
    Returns
    -------
    None
    Results of chiller test are spit out to console
    """
    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section22"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_airside_tests():
    """Runs all tests found in the airside tests JSON.
    Returns
    -------
    None
    Results of lighting test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section23"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_test_helper(test_list, ruleset_doc):
    # sort the list in a human order
    test_list.sort(key=natural_keys)
    # all will short-circuit the tests - to avoid it, split the code into two lines.
    test_results = [
        run_section_tests(test_json, ruleset_doc) for test_json in test_list
    ]
    return all(test_results)


def run_test_one_jsontest(test_json):
    return run_section_tests(test_json, RuleSet.ASHRAE9012019_RULESET)


# outcome = run_ashrae9012019_tests(section="section6")

# run_transformer_tests()
# run_lighting_tests()
# run_boiler_tests()
# run_chiller_tests()
# run_envelope_tests()
# run_receptacle_tests()
# run_airside_tests()

# run_test_one_jsontest("ashrae9012019/section5/rule_5_3.json")
