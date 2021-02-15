import os
from rct229.reports.utils import aggregate_outcomes

def print_rule_report(report):
    outcomes = report['outcomes']
    for outcome in outcomes:
        print("--------------------------------------------------------------------")
        print(f"Rule: {str(outcome['id'])}")
        print(f"Description: {str(outcome['description'])}")
        print(f"RMR context: {str(outcome['rmr_context'])}")
        # print(f"Element context: {str(outcome['element_context'])}")
        # print(f"Applicable: {str(outcome['applicable'])}")
        # print(f"Manual check required: {str(outcome['manual_check_required'])}")
        # print(f"Rule passed: {str(outcome['rule_passed'])}")
        print(f"Rule result: {str(outcome['result'])}")
        print("--------------------------------------------------------------------")


def print_summary_report(report):
    invalid_rmrs = report['invalid_rmrs']
    if invalid_rmrs:
        print("----------------------------------")
        print(f"Invalid RMRs: {str(invalid_rmrs)}")
    else:
        outcomes = report['outcomes']
        summary_dict = aggregate_outcomes(outcomes)


        print("----------------------------------")
        print("Summary")
        print(f"{len(outcomes)} rules, {summary_dict['number_evaluations']} evaluations")
        print(f"{summary_dict['number_passed']} evaluations passed")
        print(f"{summary_dict['number_failed']} evaluations failed")
        print(f"{summary_dict['number_missing_context']} evaluations missing context")
        print(f"{summary_dict['number_not_applicable']} evaluatinos not applicable")
        print(f"{summary_dict['number_manual_check_required']} evaluations requiring manual check")
        print("----------------------------------")
