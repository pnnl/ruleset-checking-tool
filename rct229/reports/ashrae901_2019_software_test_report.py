import json
from copy import deepcopy
from datetime import datetime

from rct229.report_engine.rct_report import RCTReport


class ASHRAE9012019SoftwareTestReport(RCTReport):
    def __init__(self):
        super(ASHRAE9012019SoftwareTestReport, self).__init__()
        self.title = "ASHRAE STD 229P RULESET CHECKING TOOL"
        self.purpose = "RCT Ruleset Software Testing Report"
        self.ruleset = "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)"
        self.schema_version = "0.0.23"
        self.date_run = str(datetime.now())
        self.ruleset_report_file = "ashrae901_2019_software_testing_report.json"

    def initialize_ruleset_report(self):
        report_json = dict()
        report_json["title"] = self.title
        report_json["purpose"] = self.purpose
        report_json["ruleset"] = self.ruleset
        report_json["date_run"] = self.date_run
        report_json["schema_version"] = self.schema_version
        report_json["rule_tests"] = []

        return report_json

    def generate_rule_report(self, rule_test_dict, outcome_dict):

        # Sum up the outcomes for every rule unit test evaluation in this rule test. The outcome of this is used by
        # the calculate_rule_outcome function to determine the overall actual_rule_unit_test_evaluation_outcome
        for test_evaluation in rule_test_dict["rule_unit_test_evaluation"]:
            result = test_evaluation["result"]
            outcome_dict[result] += 1

        return rule_test_dict

    def add_rule_to_ruleset_report(self, ruleset_report, rule_test_dict, rule_outcome):

        # Record outcome of aggregated pass/fails as determined by calculate_rule_outcome
        rule_test_dict["actual_rule_unit_test_evaluation_outcome"] = rule_outcome

        # Pull out the expected outcome to compare it with the actual outcome
        expected_outcome = rule_test_dict["expected_rule_unit_test_evaluation_outcome"]

        # Record agreement between expected and actual outcome
        rule_test_dict["rule_unit_test_outcome_agreement"] = (
            expected_outcome == rule_outcome
        )

        # Reorder keys to match intended order
        key_order = [
            "rule_id",
            "test_id",
            "test_description",
            "ruleset_section",
            "ruleset_section_title",
            "evaluation_type",
            "rule_unit_test_outcome_agreement",
            "expected_rule_unit_test_evaluation_outcome",
            "actual_rule_unit_test_evaluation_outcome",
            "rule_unit_test_evaluation",
        ]

        # Create new dictionary with proper order of keys
        ordered_rule_test_dict = {key: rule_test_dict[key] for key in key_order}

        # Append ruletest to ruletest report
        ruleset_report["rule_tests"].append(deepcopy(ordered_rule_test_dict))

    def save_ruleset_report(self, ruleset_report, report_dir):
        with open(report_dir, "w") as output_report:
            output_report.write(json.dumps(ruleset_report, indent=4))