import os

import rct229.rulesets as rs
from rct229.reports import reports as rct_report
from rct229.rule_engine.engine import evaluate_all_rules_rpd
from rct229.rule_engine.rulesets import RuleSet
from rct229.ruleset_functions import _setup_workflow
from rct229.ruletest_engine.run_ruletests import (
    generate_ashrae9012019_software_test_report,
)
from rct229.utils.assertions import assert_


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
