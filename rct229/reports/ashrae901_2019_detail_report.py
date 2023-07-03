import json

from rct229.report_engine.rct_report import RCTReport
from rct229.reports.utils import calc_vals_converter
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel


class ASHRAE9012019DetailReport(RCTReport):
    def __init__(self):
        super(ASHRAE9012019DetailReport, self).__init__()
        self.title = "ASHRAE STD 229P RULESET CHECKING TOOL"
        self.purpose = "Project Testing Report"
        self.ruleset = "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)"
        self.schema_version = "0.0.23"
        self.ruleset_report_file = "ashrae901_2019_detail_report.json"

    def initialize_ruleset_report(self):
        report_json = dict()
        report_json["title"] = self.title
        report_json["purpose"] = self.purpose
        report_json["ruleset"] = self.ruleset
        report_json["date_run"] = self.date_run
        report_json["schema_version"] = self.schema_version
        report_json["rules"] = dict()
        return report_json

    def generate_rule_report(self, rule_outcome, outcome_dict):
        # set up the rule meta data
        rule_id = rule_outcome["id"]
        rule_report = dict()
        rule_report["rule_id"] = rule_id
        rule_report["description"] = rule_outcome["description"]
        rule_report["ruleset_section_title"] = rule_outcome["ruleset_section_title"]
        rule_report["primary_rule"] = "Yes" if rule_outcome["primary_rule"] else "No"
        rule_report["standard_section"] = rule_outcome["standard_section"]
        rule_report_list = []
        self._rule_outcome_helper(rule_outcome, rule_report_list, outcome_dict)
        rule_report["evaluations"] = rule_report_list
        return rule_report

    def add_rule_to_ruleset_report(self, ruleset_report, rule_report, rule_outcome):
        # rule_report["rule_evaluation_outcome"] = rule_outcome
        ruleset_report["rules"][rule_report["rule_id"]] = rule_report

    def save_ruleset_report(self, ruleset_report, report_dir):
        with open(report_dir, "w") as output_report:
            output_report.write(json.dumps(ruleset_report, indent=4))

    def _rule_outcome_helper(self, results, eval_list, outcome_dict):
        def output_node(output_result, output_eval_list, output_outcome_dict):
            # in this case, it is the rule checking component
            evaluation_outcome = dict()
            if any(
                [
                    key.startswith("INVALID_") and key.endswith("_CONTEXT")
                    for key in output_result
                ]
            ):
                evaluation_outcome["invalid_msg"] = "".join(
                    [output_result[key] for key in output_result]
                )
                output_outcome_dict[RCTOutcomeLabel.UNDETERMINED] += 1
            else:
                outcome_label = output_result["result"]
                if outcome_label == RCTOutcomeLabel.PASS:
                    output_outcome_dict[RCTOutcomeLabel.PASS] += 1
                if outcome_label == RCTOutcomeLabel.FAILED:
                    output_outcome_dict[RCTOutcomeLabel.FAILED] += 1
                if outcome_label == RCTOutcomeLabel.UNDETERMINED:
                    output_outcome_dict[RCTOutcomeLabel.UNDETERMINED] += 1
                if outcome_label == RCTOutcomeLabel.NOT_APPLICABLE:
                    output_outcome_dict[RCTOutcomeLabel.NOT_APPLICABLE] += 1
                evaluation_outcome["id"] = output_result["id"]
                evaluation_outcome["outcome"] = outcome_label
                evaluation_outcome["messages"] = (
                    output_result["message"]
                    if output_result.get("message") is not None
                    else ""
                )
                evaluation_outcome["calculated_values"] = (
                    calc_vals_converter(output_result["calc_vals"])
                    if output_result.get("calc_vals") is not None
                    else ""
                )
            output_eval_list.append(evaluation_outcome)

        outcome = results["result"]
        if type(outcome) is str:
            output_node(results, eval_list, outcome_dict)
        elif type(outcome) is dict:
            output_node(outcome, eval_list, outcome_dict)
        else:
            for result in outcome:
                self._rule_outcome_helper(result, eval_list, outcome_dict)
