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


def generate_ashrae9012019_software_test_report(
    section_list=None, output_dir=os.path.dirname(__file__)
):
    """
    Generate a software test JSON for ASHRAE 90.1 RCT for a given set of sections If section is None, then this
    function runs all the rule sections

    Parameters
    ----------
    section_list: list

        List of strings representing section lists to run. If None, all are ran per those listed in
        RuleSetTest.ASHRAE9012019_TEST_LIST

    output_dir: str

        Directory in which you want the ashrae901_2019_software_testing_report.json to appear

    """

    # If no section list is defined, rune all ASHRAE90.1 sections
    if section_list is None:
        section_list = RuleSetTest.ASHRAE9012019_TEST_LIST

    return generate_software_test_report("ashrae9012019", section_list, output_dir)


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


def run_hvac_general_tests():
    """Runs all tests found in the hvac general tests JSON.
    Returns
    -------
    None
    Results of lighting test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section19"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_sys_zone_assignment_tests():
    """Runs all tests found in the system zone assignment tests JSON.
    Returns
    -------
    None
    Results of system zone assignments test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section18"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_elevator_tests():
    """Runs all tests found in the elevator tests JSON.
    Returns
    -------
    None
    Results of system zone assignments test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section16"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_performance_calculation_tests():
    """Runs all tests found in the performance calculation tests JSON.
    Returns
    -------
    None
    Results of system zone assignments test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section1"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_service_water_heater_tests():
    """Runs all tests found in the service water heater calculation tests JSON.
    Returns
    -------
    None
    Results of system zone assignments test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section11"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_schedule_tests():
    """Runs all tests found in the schedule tests JSON.
    Returns
    -------
    None
    Results of system zone assignments test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section4"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_general_hvac_tests():
    """Runs all tests found in section 10 tests JSON.
    Returns
    -------
    None
    Results of system zone assignments test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section10"
    )
    return run_test_helper(json_tests, RuleSet.ASHRAE9012019_RULESET)


def run_receptacle_tests():
    """Runs all tests found in the schedule tests JSON.
    Returns
    -------
    None
    Results of system zone assignments test are spit out to console
    """

    json_tests = _helper_get_all_test_file_by_section(
        RuleSet.ASHRAE9012019_RULESET, "section12"
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
    """
    Test function developed to facilitate running a single rule test json
    """
    return run_section_tests(test_json, RuleSet.ASHRAE9012019_RULESET)


# if __name__ == "__main__":
#     outcome = run_ashrae9012019_tests(section="section5")

# run_transformer_tests()
# run_lighting_tests()
# run_boiler_tests()
# run_chiller_tests()
# run_envelope_tests()
# run_receptacle_tests()
# run_airside_tests()
# run_sys_zone_assignment_tests()
# run_hvac_general_tests()
# run_elevator_tests()
# run_performance_calculation_tests()
# run_schedule_tests()
# run_general_hvac_tests()
# run_service_water_heater_tests()


# run_test_one_jsontest("ashrae9012019/section11/rule_11_7.json")
# run_ashrae9012019_tests()
# output_dir = os.path.dirname(__file__)
# generate_ashrae9012019_software_test_report(['tester'])
# generate_ashrae9012019_software_test_report(None, output_dir)
