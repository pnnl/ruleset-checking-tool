import json

from rct229.report_engine.rct_report import RCTReport
from rct229.reports.utils import calc_vals_converter
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel


class EngineRawOutput(RCTReport):
    def __init__(self):
        super(EngineRawOutput, self).__init__()
        self.ruleset_report_file = f"{self.__class__.__name__}.json"

    def generate_rule_report(self, rule_outcome, outcome_dict):
        def rule_report_helper(rule_outcomes, outcomes_dict):
            if type(rule_outcomes) is dict:
                if any(
                    [
                        key.startswith("INVALID_") and key.endswith("_CONTEXT")
                        for key in rule_outcomes
                    ]
                ):
                    outcomes_dict[RCTOutcomeLabel.UNDETERMINED] += 1
                elif type(rule_outcomes["result"]) is list:
                    rule_report_helper(rule_outcomes["result"], outcomes_dict)
                elif type(rule_outcomes["result"]) is str:
                    rule_outcome_str = rule_outcomes["result"]
                    if rule_outcome_str.startswith("MISSING_"):
                        outcomes_dict[RCTOutcomeLabel.UNDETERMINED] += 1
                    else:
                        outcomes_dict[rule_outcome_str] += 1
                    if "calc_vals" in rule_outcomes:
                        rule_outcomes["calc_vals"] = calc_vals_converter(
                            rule_outcomes["calc_vals"]
                        )
            else:
                for result in rule_outcomes:
                    rule_report_helper(result, outcome_dict)

        rule_report_helper(rule_outcome, outcome_dict)
        return rule_outcome

    def add_rule_to_ruleset_report(self, ruleset_report, rule_report, rule_outcome):
        rule_report["rule_evaluation_outcome"] = rule_outcome
        ruleset_report.append(rule_report)

    def save_ruleset_report(self, ruleset_report, report_dir):
        with open(report_dir, "w") as output_report:
            output_report.write(json.dumps(ruleset_report, indent=4))
