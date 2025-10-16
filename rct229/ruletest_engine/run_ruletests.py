from rct229.ruletest_engine.ruletest_engine import *
from rct229.ruletest_engine.ruletest_jsons.ashrae9012019 import *
from rct229.utils.natural_sort import natural_keys

TEST_PATH = "ruletest_jsons"


# ============================================================
# =============== ASHRAE 90.1-2019 TEST RUNNERS ==============
# ============================================================


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
    SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
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


# ============================================================
# =============== ASHRAE 90.1-2022 TEST RUNNERS ==============
# ============================================================


def run_ashrae9012022_tests(section=None):
    """
    Run ruleset by section or all
    If section is None, then this function runs all the rule sections

    Parameters
    ----------
    section: str - it should be the same string in the ASHRAE9012022_TEST_PATH_LIST

    Returns
    -------

    """
    SchemaStore.set_ruleset(RuleSet.ASHRAE9012022_RULESET)
    return [
        run_test_helper(
            _helper_get_all_test_file_by_section(
                RuleSet.ASHRAE9012022_RULESET, test_section
            ),
            RuleSet.ASHRAE9012022_RULESET,
        )
        for test_section in RuleSetTest.ASHRAE9012022_TEST_LIST
        if section is None or test_section == section
    ]


def generate_ashrae9012022_software_test_report(
    section_list=None, output_dir=os.path.dirname(__file__)
):
    """Generate a software test JSON report for ASHRAE 90.1-2022."""
    if section_list is None:
        section_list = RuleSetTest.ASHRAE9012022_TEST_LIST
    return generate_software_test_report("ashrae9012022", section_list, output_dir)


# ============================================================
# ===================== HELPER FUNCTIONS ======================
# ============================================================


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


def run_test_helper(test_list, ruleset_doc):
    # sort the list in a human order
    test_list.sort(key=natural_keys)
    # all will short-circuit the tests - to avoid it, split the code into two lines.
    test_results = [
        run_section_tests(test_json, ruleset_doc) for test_json in test_list
    ]
    return all(test_results)


def _run_tests_by_dir(ruleset, directory):
    """Internal helper to execute all tests within a category directory."""
    json_tests = _helper_get_all_test_file_by_section(ruleset, directory)
    return run_test_helper(json_tests, ruleset)


# ============================================================
# =============== CATEGORY TESTS FOR 2019 =====================
# ============================================================


def run_lighting_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, LIGHTING_DIR)


def run_envelope_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, ENVELOPE_DIR)


def run_boiler_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, HVAC_HOT_WATER_DIR)


def run_chiller_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, HVAC_CHILLED_WATER_DIR)


def run_airside_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, HVAC_AIRSIDE_DIR)


def run_hvac_general_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, HVAC_GENERAL_DIR)


def run_sys_zone_assignment_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, HVAC_BASELINE_DIR)


def run_elevator_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, ELEVATOR_DIR)


def run_performance_calculation_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, PERFORMANCE_CALC_DIR)


def run_service_water_heater_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, SERVICE_HOT_WATER_DIR)


def run_schedule_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, SCHEDULE_DIR)


def run_receptacle_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, RECEPTACLE_DIR)


# ============================================================
# =============== CATEGORY TESTS FOR 2022 =====================
# ============================================================


def run_lighting_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, LIGHTING_DIR)


def run_envelope_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, ENVELOPE_DIR)


def run_boiler_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, HVAC_HOT_WATER_DIR)


def run_chiller_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, HVAC_CHILLED_WATER_DIR)


def run_airside_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, HVAC_AIRSIDE_DIR)


def run_hvac_general_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, HVAC_GENERAL_DIR)


def run_sys_zone_assignment_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, HVAC_BASELINE_DIR)


def run_elevator_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, ELEVATOR_DIR)


def run_performance_calculation_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, PERFORMANCE_CALC_DIR)


def run_service_water_heater_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, SERVICE_HOT_WATER_DIR)


def run_schedule_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, SCHEDULE_DIR)


def run_receptacle_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, RECEPTACLE_DIR)


# ============================================================
# =================== SINGLE TEST RUNNERS ====================
# ============================================================


def run_test_one_ASHRAE9012019_jsontest(test_json):
    """
    Test function developed to facilitate running a single rule test json
    """
    return run_section_tests(test_json, RuleSet.ASHRAE9012019_RULESET)


def run_test_one_ASHRAE9012022_jsontest(test_json):
    """
    Test function developed to facilitate running a single rule test json
    """
    return run_section_tests(test_json, RuleSet.ASHRAE9012022_RULESET)


# ============================================================
# ====================== ENTRY POINT =========================
# ============================================================

if __name__ == "__main__":
    # outcome = run_ashrae9012019_tests(section="section23")

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
    # # run_general_hvac_tests()
    # run_service_water_heater_tests()

    # run_test_one_ASHRAE9012019_jsontest("ashrae9012019/section23/rule_23_8.json")
    # run_test_one_ASHRAE9012022_jsontest("ashrae9012022/ENV/rule_5_43.json")
    # run_ashrae9012019_tests()
    # run_ashrae9012022_tests()
    # output_dir = os.path.dirname(__file__)
    # generate_ashrae9012019_software_test_report(['tester'])
    # generate_ashrae9012019_software_test_report(None, output_dir)
    pass
