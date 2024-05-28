from functools import reduce
from pathlib import PurePath

from rct229.ruletest_engine.ruletest_engine import *
from rct229.utils.natural_sort import natural_keys

TEST_PATH = "ruletest_jsons"


def run_ashrae9012019_tests(
    section: str = None, eval_proc_print: bool = False
) -> list[bool]:
    """
    Run ruleset by section or all
    If section is None, then this function runs all the rule sections

    Parameters
    ----------
    section: str - it should be the same string in the ASHRAE9012019_TEST_PATH_LIST
    eval_proc_print: bool - if True, evaluation process will be printed with 10% increments and "Processing Rule" won't be printed.
                          if False, evaluation process will NOT be printed and "Processing Rule" will be printed.

    Returns
    -------

    """

    if eval_proc_print:
        # get all the list of rpd file names
        rpd_by_section_list = [
            _helper_get_all_test_file_by_section(
                RuleSet.ASHRAE9012019_RULESET, test_section
            )
            for test_section in RuleSetTest.ASHRAE9012019_TEST_LIST
            if section is None or test_section == section
        ]
        # flatten the 2D list
        list_of_rpds = reduce(lambda x, y: x + y, rpd_by_section_list)
        list_of_rpds_len = len(list_of_rpds)

        # initialize a variable to track the next progress update
        next_progress = 10

        outcome_by_section = {}
        for idx, rpd in enumerate(list_of_rpds):
            # calculate the percentage of progress
            progress = (idx + 1) / list_of_rpds_len * 100

            # get the section name (e.g., "section5")
            section = PurePath(rpd).parts[1]
            if section not in outcome_by_section:
                outcome_by_section[section] = []

            # test each ruleset and save the bool result
            outcome_by_section[section].append(
                run_test_helper([rpd], RuleSet.ASHRAE9012019_RULESET, eval_proc_print)
            )

            # check if the progress has reached or exceeded the next progress update
            while progress >= next_progress:
                print(f"Evaluation completion: {next_progress}%")
                next_progress += 10

        return [
            all(outcome_by_section[section_name]) for section_name in outcome_by_section
        ]
    else:
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


def run_test_helper(test_list, ruleset_doc, eval_proc_print=False):
    # sort the list in a human order
    test_list.sort(key=natural_keys)
    # all will short-circuit the tests - to avoid it, split the code into two lines.
    test_results = [
        run_section_tests(test_json, ruleset_doc, eval_proc_print)
        for test_json in test_list
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

# run_test_one_jsontest("ashrae9012019/section4/rule_4_2.json")
run_ashrae9012019_tests(eval_proc_print=True)
# output_dir = os.path.dirname(__file__)
# generate_ashrae9012019_software_test_report(['tester'])
# generate_ashrae9012019_software_test_report(None, output_dir)
