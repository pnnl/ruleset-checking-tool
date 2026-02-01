import os

from rct229.ruletest_engine.ruletest_engine import (
    run_section_tests,
    generate_software_test_report,
)
from rct229.schema.schema_store import SchemaStore
from rct229.rule_engine.rulesets import RuleSet
from rct229.utils.natural_sort import natural_keys
from rct229.ruletest_engine.ruletest_jsons import get_ruleset_test_sections

TEST_PATH = "ruletest_jsons"
os.environ["RCT_DISABLE_CACHE"] = "1"

# ============================================================
# =============== GENERIC TEST RUNNERS =======================
# ============================================================


def run_ruleset_tests(ruleset: str, section: str | None = None):
    """
    Run all or selected rule test sections for a given ruleset.

    Parameters
    ----------
    ruleset : str
        The ruleset name (e.g., "ashrae9012019" or "ashrae9012022").
    section : str or None
        If provided, only that section is run.

    Returns
    -------
    list[bool]
        True/False results per section.
    """
    SchemaStore.set_ruleset(ruleset)
    all_sections = get_ruleset_test_sections(ruleset)

    return [
        run_test_helper(
            _helper_get_all_test_file_by_section(ruleset, test_section),
            ruleset,
        )
        for test_section in all_sections
        if section is None or test_section == section
    ]


def generate_software_test_report_for_ruleset(
    ruleset: str, section_list=None, output_dir=os.path.dirname(__file__)
):
    """Generate a software test JSON report for the given ruleset."""
    if section_list is None:
        section_list = get_ruleset_test_sections(ruleset)
    return generate_software_test_report(ruleset, section_list, output_dir)


# ============================================================
# =============== RULESET-SPECIFIC WRAPPERS ==================
# ============================================================


def run_ashrae9012019_tests(section=None):
    """Run all or specific ASHRAE 90.1-2019 tests."""
    return run_ruleset_tests("ashrae9012019", section)


def run_ashrae9012022_tests(section=None):
    """Run all or specific ASHRAE 90.1-2022 tests."""
    return run_ruleset_tests("ashrae9012022", section)


def generate_ashrae9012019_software_test_report(
    section_list=None, output_dir=os.path.dirname(__file__)
):
    """Generate ASHRAE 90.1-2019 software test report."""
    return generate_software_test_report_for_ruleset(
        "ashrae9012019", section_list, output_dir
    )


def generate_ashrae9012022_software_test_report(
    section_list=None, output_dir=os.path.dirname(__file__)
):
    """Generate ASHRAE 90.1-2022 software test report."""
    return generate_software_test_report_for_ruleset(
        "ashrae9012022", section_list, output_dir
    )


# ============================================================
# ===================== HELPER FUNCTIONS =====================
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
# =============== CATEGORY TESTS FOR 2019 ====================
# ============================================================


def run_lighting_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "LTG")


def run_envelope_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "ENV")


def run_boiler_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "HVAC-HW")


def run_chiller_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "HVAC-CHW")


def run_airside_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "HVAC-SPEC")


def run_hvac_general_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "HVAC-GEN")


def run_sys_zone_assignment_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "HVAC-SYS")


def run_elevator_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "ELV")


def run_performance_calculation_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "CALC")


def run_service_water_heater_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "SHW")


def run_schedule_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "SCH")


def run_receptacle_tests_2019():
    return _run_tests_by_dir(RuleSet.ASHRAE9012019_RULESET, "REC")


# ============================================================
# =============== CATEGORY TESTS FOR 2022 ====================
# ============================================================


def run_lighting_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "LTG")


def run_envelope_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "ENV")


def run_boiler_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "HVAC-HW")


def run_chiller_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "HVAC-CHW")


def run_airside_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "HVAC-SPEC")


def run_hvac_general_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "HVAC-GEN")


def run_sys_zone_assignment_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "HVAC-SYS")


def run_elevator_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "ELV")


def run_performance_calculation_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "CALC")


def run_service_water_heater_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "SHW")


def run_schedule_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "SCH")


def run_receptacle_tests_2022():
    return _run_tests_by_dir(RuleSet.ASHRAE9012022_RULESET, "REC")


# ============================================================
# =================== SINGLE TEST RUNNERS ====================
# ============================================================


def run_test_one_jsontest_2019(test_json):
    """
    Test function developed to facilitate running a single rule test json
    """
    return run_section_tests(test_json, RuleSet.ASHRAE9012019_RULESET)


def run_test_one_jsontest_2022(test_json):
    """
    Test function developed to facilitate running a single rule test json
    """
    return run_section_tests(test_json, RuleSet.ASHRAE9012022_RULESET)


# ============================================================
# ====================== ENTRY POINT =========================
# ============================================================

if __name__ == "__main__":
    # outcome = run_ashrae9012019_tests(section="section23")
    #
    # run_lighting_tests_2019()
    # run_boiler_tests_2019()
    # run_chiller_tests_2019()
    # run_envelope_tests_2019()
    # run_receptacle_tests_2019()
    # run_airside_tests_2019()
    # run_sys_zone_assignment_tests_2019()
    # run_hvac_general_tests_2019()
    # run_elevator_tests_2019()
    # run_performance_calculation_tests_2019()
    # run_schedule_tests_2019()
    # run_service_water_heater_tests_2019()
    #
    # run_lighting_tests_2022()
    # run_boiler_tests_2022()
    # run_chiller_tests_2022()
    # run_envelope_tests_2022()
    # run_receptacle_tests_2022()
    # run_airside_tests_2022()
    # run_sys_zone_assignment_tests_2022()
    # run_hvac_general_tests_2022()
    # run_elevator_tests_2022()
    # run_performance_calculation_tests_2022()
    # run_schedule_tests_2022()
    # run_service_water_heater_tests_2022()
    #
    # run_test_one_jsontest_2019("ashrae9012019/ENV/rule_5_43.json")
    # run_test_one_jsontest_2022("ashrae9012022/ENV/rule_5_43.json")
    # run_ashrae9012019_tests()
    # run_ashrae9012022_tests()
    # output_dir = os.path.dirname(__file__)
    # generate_ashrae9012019_software_test_report(['tester'])
    # generate_ashrae9012019_software_test_report(None, output_dir)
    pass
