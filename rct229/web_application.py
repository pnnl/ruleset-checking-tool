import os

import rct229.rulesets as rulesets
import rct229.rulesets as rs
from rct229.reports import reports as rct_report
from rct229.rule_engine.engine import evaluate_all_rules, evaluate_all_rules_rpd
from rct229.rule_engine.rulesets import RuleSet, RuleSetTest
from rct229.ruletest_engine.ruletest_jsons.scripts.excel_to_test_json_utilities import (
    generate_rule_test_dictionary,
)
from rct229.ruletest_engine.run_ruletests import (
    generate_ashrae9012019_software_test_report,
)
from rct229.rulesets.ashrae9012019 import rules_dict
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore
from rct229.utils.assertions import assert_


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
        section_rule_name = rules_dict.get(rule_definition_tuple[0].lower())

        if section_rule_name is None:
            print(f"Rule {rule_definition_tuple[0]} not found in rules_dict")
            continue

        # Parse section name from section{N}rule{N}, then add it to the dictionary count
        section_name = section_rule_name.split("rule")[0].lower()
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
    """
    Run software test and return the saved report directory

    Parameters
    ----------
    ruleset str ruleset key
    section str section id
    saving_dir str directory to save the report

    Returns
    -------
    report_dir str | None the path to the generated report

    """
    if not _setup_workflow(ruleset):
        assert_(False, f"Unrecognized ruleset: {ruleset}")
    report_dir = None
    print(f"software test workflow for section {section}")
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        report_dir = generate_ashrae9012019_software_test_report(
            section, output_dir=saving_dir
        )
    return report_dir


def run_project_evaluation(
    rpds, ruleset, reports=["RAW_OUTPUT"], saving_dir="./", session_id=""
):
    """

    Parameters
    ----------
    rpds: list[dict] list of dictionary
    ruleset: str ruleset key
    reports: list[str] list of strings and each string is the enum value of a report
    saving_dir: directory to save report.
    session_id: a string representing a calculation session

    Returns
    -------
    report list: list of strings contain paths to the report

    """
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
    report = evaluate_all_rules_rpd(rpds, session_id)

    print(f"Saving reports to: {saving_dir}......")
    report_path_list = []
    for report_type in reports:
        report_module = available_report_dict[report_type]()
        report_module.generate(report, saving_dir)
        report_path_list.append(
            os.path.join(saving_dir, report_module.ruleset_report_file)
        )

    return report_path_list


def get_available_reports_by_ruleset(ruleset):
    """
    Get the available report types by ruleset
    Parameters
    ----------
    ruleset str ruleset key

    Returns
    -------
    list of strings

    """
    if not _setup_workflow(ruleset):
        assert_(False, f"Unrecognized ruleset: {ruleset}")
    available_report_modules = rct_report.__getreports__()
    return [key for key, value in available_report_modules]


def get_available_rulesets():
    """
    Get a list of available rulesets
    Returns
    -------

    """
    return rs.__all__


def _setup_workflow(ruleset: str):
    """
    Helper function
    Parameters
    ----------
    ruleset

    Returns
    -------

    """
    setup_flag = False
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        SchemaEnums.update_schema_enum()
        setup_flag = True
    return setup_flag
