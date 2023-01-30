import io
import os

from rct229.rule_engine.engine import evaluate_all_rules, evaluate_rule
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.file import deserialize_rmr_file

SCRIPT_DIR = os.path.dirname(__file__)  # <-- absolute dir the script is in
"""
Test one single rule
requires user_rmr_dir, baseline_rmr_dir, proposed_rmr_dir 
"""


def evaluate_single_rule(user_rmr_dir, baseline_rmr_dir, proposed_rmr_dir, rule):
    rmr_are_valid_json = True
    user_rmr_obj = None
    baseline_rmr_obj = None
    proposed_rmr_obj = None

    if user_rmr_dir:
        user_rmr = io.open(os.path.join(SCRIPT_DIR, user_rmr_dir), "rb")
        try:
            user_rmr_obj = deserialize_rmr_file(user_rmr)
        except:
            rmr_are_valid_json = False

    if baseline_rmr_dir:
        baseline_rmr = io.open(os.path.join(SCRIPT_DIR, baseline_rmr_dir), "rb")
        try:
            baseline_rmr_obj = deserialize_rmr_file(baseline_rmr)
        except:
            rmr_are_valid_json = False

    if proposed_rmr_dir:
        proposed_rmr = io.open(os.path.join(SCRIPT_DIR, proposed_rmr_dir), "rb")
        try:
            proposed_rmr_obj = deserialize_rmr_file(proposed_rmr)
        except:
            rmr_are_valid_json = False

    if not rmr_are_valid_json:
        return {"error": "Json file is invalid"}
    else:
        rmrs = UserBaselineProposedVals(
            user_rmr_obj, baseline_rmr_obj, proposed_rmr_obj
        )
        report = evaluate_rule(rule, rmrs)

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
