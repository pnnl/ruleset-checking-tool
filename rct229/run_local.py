from rct229.cli import evaluate_rmr_triplet
from rct229.reports.project_report import print_rule_report, print_summary_report
from rct229.rule_engine.engine import evaluate_all_rules
from rct229.utils.file import deserialize_rmr_file
from rct229.reports.ashrae901_2019_summary_report import ASHRAE9012019SummaryReport


def evaluate_rmr_triplets(user_rmr, baseline_rmr, proposed_rmr, rulesetdoc):
    print("Test implementation of rule engine for ASHRAE Std 229 RCT.")
    print("")

    user_rmr_obj = None
    baseline_rmr_obj = None
    proposed_rmr_obj = None
    rmr_are_valid_json = True
    try:
        user_rmr_obj = deserialize_rmr_file(user_rmr)
    except:
        rmr_are_valid_json = False
        print("User RMR is not a valid JSON file")
    try:
        baseline_rmr_obj = deserialize_rmr_file(baseline_rmr)
    except:
        rmr_are_valid_json = False
        print("Baseline RMR is not a valid JSON file")
    try:
        proposed_rmr_obj = deserialize_rmr_file(proposed_rmr)
    except:
        rmr_are_valid_json = False
        print("Proposed RMR is not a valid JSON file")

    if not rmr_are_valid_json:
        print("")
        return
    else:
        print("Processing rules...")
        print("")

        report = evaluate_all_rules(
            user_rmr_obj, baseline_rmr_obj, proposed_rmr_obj, rulesetdoc
        )

        # Example - Print a final compliance report
        # [We'll actually most likely save a data file here and report occurs from separate CLI command]
        # print_json_report(report)
        print_rule_report(report)
        print_summary_report(report)

        print("Rules completed.")
        print("")


user_rmd = open(
    "C:\\Users\\xuwe123\\Documents\\osstd_eplus_rct\\eplus_sim\\proposed\\proposed_model.rmd"
)
proposed_rmd = open(
    "C:\\Users\\xuwe123\\Documents\\osstd_eplus_rct\\eplus_sim\\proposed\\proposed_model.rmd"
)
baseline_rmd = open(
    "C:\\Users\\xuwe123\\Documents\\osstd_eplus_rct\\eplus_sim\\baseline\\baseline_model.rmd"
)

report = evaluate_rmr_triplet(user_rmd, baseline_rmd, proposed_rmd, "ashrae9012019")
props = {
    "user_rmd": "1",
    "proposed_rmd": "2",
    "baseline_rmd": "3",
}
report_module = ASHRAE9012019SummaryReport(props)
report_module.generate(report, "./examples/output")
