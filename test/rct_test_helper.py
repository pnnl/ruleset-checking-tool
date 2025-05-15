import io
import os

from rct229.rule_engine.engine import evaluate_rule
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.utils.file import deserialize_rpd_file

SCRIPT_DIR = os.path.dirname(__file__)  # <-- absolute dir the script is in
"""
Test one single rule
requires user_rmd_dir, baseline_rmd_dir, proposed_rmd_dir 
"""


def evaluate_single_rule(user_rmd_dir, baseline_rmd_dir, proposed_rmd_dir, rule):
    rmd_are_valid_json = True
    user_rmd_obj = None
    baseline_rmd_obj = None
    proposed_rmd_obj = None

    if user_rmd_dir:
        user_rmd = io.open(os.path.join(SCRIPT_DIR, user_rmd_dir), "rb")
        try:
            user_rmd_obj = deserialize_rpd_file(user_rmd)
        except:
            rmd_are_valid_json = False

    if baseline_rmd_dir:
        baseline_rmd = io.open(os.path.join(SCRIPT_DIR, baseline_rmd_dir), "rb")
        try:
            baseline_rmd_obj = deserialize_rpd_file(baseline_rmd)
        except:
            rmd_are_valid_json = False

    if proposed_rmd_dir:
        proposed_rmd = io.open(os.path.join(SCRIPT_DIR, proposed_rmd_dir), "rb")
        try:
            proposed_rmd_obj = deserialize_rpd_file(proposed_rmd)
        except:
            rmd_are_valid_json = False

    if not rmd_are_valid_json:
        return {"error": "Json file is invalid"}
    else:
        rmds = produce_ruleset_model_description(
            USER=user_rmd_obj, BASELINE_0=baseline_rmd_obj, PROPOSED=proposed_rmd_obj
        )
        report = evaluate_rule(rule, rmds)

        return report


def report_to_result_for_a_rule(report):
    """
    Helper function to extract the pass fail report from the rule test output.
    Parameters
    ----------
    report

    Returns dict contains results id, result and additional failure information
    -------
    """

    # assuming one outcome
    outcome = report["outcomes"][0]
    # assuming only one calc_Vals in the report for a rule
    calc_vals = outcome["result"][0]
    return calc_vals
