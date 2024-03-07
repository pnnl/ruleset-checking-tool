import rct229.rulesets as rulesets
from rct229.rule_engine.engine import evaluate_all_rules
from rct229.rule_engine.rulesets import RuleSet, RuleSetTest
from rct229.reports import reports as rct_report
from rct229.ruletest_engine.ruletest_jsons.scripts.excel_to_test_json_utilities import (
    generate_rule_test_dictionary,
)
from rct229.ruletest_engine.run_ruletests import run_ashrae9012019_tests
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore
from rct229.utils.assertions import assert_
import rct229.rulesets as rs


def count_number_of_rules(ruleset_standard):
    """Returns the number of rules in a standard

     Parameters
     ----------
     ruleset_standard : str
         Name of the code standard you're interested in counting under the rct229/rulesets directory.
         Ex: 'ashrae9012019'

     Returns
    -------
    count_dict: dict
        Python dict with keys for each section in a given standard and their respective count.
        Also contains 'Total' as a key with the sum total rules

    """

    if not _setup_workflow(ruleset_standard):
        assert_(
            False,
            f"Provided ruleset, {ruleset_standard}, does not match the available ones in the RCT. Available: ashrae9012019 ",
        )

    # Collect rule modules as a list of tuples
    available_rule_definitions = rulesets.__getrules__()

    # Dictionary with rule counts
    count_dict = {}

    for rule_definition_tuple in available_rule_definitions:

        # Parse section name from Section{N}Rule{N}, then add it to the dictionary count
        section_name = rule_definition_tuple[0].split("Rule")[0].lower()
        count_dict[section_name] = count_dict.get(section_name, 0) + 1

    # Get total number of rules
    count_dict["total"] = sum(count_dict.values())

    return count_dict


def count_number_of_ruletest_cases(ruleset_standard):
    """Returns the number of rule test cases in a standard

     Parameters
     ----------
     ruleset_standard : str
         Name of the code standard you're interested in counting under the rct229/rulesets directory.
         Ex: 'ashrae9012019'

     Returns
    -------
    count_dict: dict
        Python dict with keys for each section in a given standard and their respective count.
        Also contains 'Total' as a key with the sum total rule tests

    """
    if not _setup_workflow(ruleset_standard):
        assert_(
            False,
            f"Provided ruleset, {ruleset_standard}, does not match the available ones in the RCT. Available: ashrae9012019 ",
        )

    # Aggregate rule test information into a dictionary
    master_ruletest_dict = generate_rule_test_dictionary(ruleset_standard)

    # Dictionary with ruletest counts
    count_dict = {}

    # Iterate through each section and get the number of rule unit tests
    for section_name, section_dict in master_ruletest_dict.items():
        count_dict[section_name] = len(section_dict["Rule_Unit_Test"])

    # Get total rule unit tests
    count_dict["total"] = sum(count_dict.values())

    return count_dict


def run_software_test(ruleset, section=None, saving_dir="./"):
    print(f"software test workflow for section {section}")
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        outcome_list = run_ashrae9012019_tests(section)
        if section is None:
            for idx, outcome in enumerate(outcome_list):
                assert_(
                    outcome,
                    f"{RuleSetTest.ASHRAE9012019_TEST_LIST[idx]} failed in the test",
                )
        else:
            assert_(all(outcome_list), f"{section} failed in the test")
    else:
        assert_(
            False,
            f"ruleset document {ruleset} is not currently supported by the RCT. Please select one from the following: ashrae9012019",
        )
    return saving_dir


def run_project_evaluation(rpds, ruleset, reports=["RAW_OUTPUT"], saving_dir="./"):
    assert_(
        rpds and isinstance(rpds, list),
        "Empty rpds list, please make sure to provide a list of RPDs",
    )
    for rpd in rpds:
        assert_(isinstance(rpd, dict), "Invalid RPD data, must be loaded as JSON.")
    assert_(
        reports and isinstance(reports, list),
        "Empty report list, please make sure to provide a list of reports",
    )

    if not _setup_workflow(ruleset):
        assert_(False, f"Unrecognized ruleset: {ruleset}")

    available_report_modules = rct_report.__getreports__()
    available_report_dict = {key: value for key, value in available_report_modules}
    available_report_str = [key for key, value in available_report_modules]
    for report_type in reports:
        assert_(
            report_type in available_report_dict,
            f"Cannot find matching report type for {report_type}. Available ones are {available_report_str}.",
        )

    print("Test implementation of rule engine for ASHRAE Std 229 RCT.")
    print("")
    report = evaluate_all_rules(rpds)

    print(f"Saving reports to: {saving_dir}......")
    for report_type in reports:
        report_module = available_report_dict[report_type]()
        report_module.generate(report, saving_dir)

    return saving_dir


def get_available_reports_by_ruleset(ruleset):
    if not _setup_workflow(ruleset):
        assert_(False, f"Unrecognized ruleset: {ruleset}")
    available_report_modules = rct_report.__getreports__()
    return [key for key, value in available_report_modules]


def get_available_rulesets():
    return rs.__all__


def _setup_workflow(ruleset: str):
    setup_flag = False
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        SchemaEnums.update_schema_enum()
        setup_flag = True
    return setup_flag
