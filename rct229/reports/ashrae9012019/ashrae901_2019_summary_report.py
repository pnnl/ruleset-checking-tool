import re

from pydash import find
from rct229.report_engine.rct_report import RCTReport
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel
from rct229.rulesets.ashrae9012019 import section_dict, section_list


class ASHRAE9012019SummaryReport(RCTReport):
    def __init__(self):
        super(ASHRAE9012019SummaryReport, self).__init__()
        self.title = "ASHRAE STD 229P RULESET CHECKING TOOL"
        self.purpose = "Summary Report"
        self.ruleset = "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)"
        self.ruleset_report_file = f"{self.__class__.__name__}.md"

    def initialize_ruleset_report(self, rule_outcome=None):

        self.ruleset_outcome = {
            name: {
                RCTOutcomeLabel.PASS: 0,
                RCTOutcomeLabel.FAILED: 0,
                RCTOutcomeLabel.UNDETERMINED: 0,
                RCTOutcomeLabel.NOT_APPLICABLE: 0,
            }
            for name in section_list
        }

        rpd_files = rule_outcome["rpd_files"]
        user_match = find(rpd_files, lambda item: item["ruleset_model_type"] == "USER")
        proposed_match = find(
            rpd_files, lambda item: item["ruleset_model_type"] == "PROPOSED"
        )
        baseline_0_match = find(
            rpd_files, lambda item: item["ruleset_model_type"] == "BASELINE_0"
        )
        baseline_90_match = find(
            rpd_files, lambda item: item["ruleset_model_type"] == "BASELINE_90"
        )
        baseline_180_match = find(
            rpd_files, lambda item: item["ruleset_model_type"] == "BASELINE_180"
        )
        baseline_270_match = find(
            rpd_files, lambda item: item["ruleset_model_type"] == "BASELINE_270"
        )

        self.summary_report = f"""
## {self.title}
### {self.purpose} 
##### {self.ruleset}
##### Date: {self.date_run}

### RMD Files
- user: {user_match["file_name"] if user_match else "N/A"}
- proposed: {proposed_match["file_name"] if proposed_match else "N/A"}
- baseline_0: {baseline_0_match["file_name"] if baseline_0_match else "N/A"}
- baseline_90: {baseline_90_match["file_name"] if baseline_90_match else "N/A"}
- baseline_180: {baseline_180_match["file_name"] if baseline_180_match else "N/A"}
- baseline_270: {baseline_270_match["file_name"] if baseline_270_match else "N/A"}

### Summary: All Primary Rules
|                              | All | Performance Calculations | Schedules Setpoints | Envelope | Lighting | HVAC General |  Service Hot Water | Receptacles | Transformers | Elevator | HVAC-HotWaterSide | HVAC - ChilledWaterSide | HVAC-AirSide | HVAC-General| HVAC-Baseline
|:----------------------------:|:---:|:--------:|:--------:|:--------:|:--------:|:-----------:|:------------:|:------------:|:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|:-----------:|
Replace-Rules
Replace-Pass
Replace-Fail
Replace-Not_Applicable
Replace-Undetermined

### Rule Evaluations
        """

    def generate_rule_report(self, rule_outcome, outcome_dict):
        def _parse_result_helper(result):
            if isinstance(result, str):
                outcome_dict[result] += 1
                return outcome_dict
            elif isinstance(result, list):
                for element in result:
                    _parse_result_helper(element)
                if (
                    sum(outcome_dict.values()) == 0
                ):  # if result is empty, fill up with `NOT_APPLICABLE` (for now) # TODO check whether empty result is resolved
                    outcome_dict[RCTOutcomeLabel.NOT_APPLICABLE] = 1
                return outcome_dict
            elif isinstance(result, dict):
                _parse_result_helper(result["result"])

        # count each rule's pass/fail/undetermined/not_applicable
        rule_outcome_result_dict = _parse_result_helper(rule_outcome["result"])

        # sum up overall rule numbers
        # self.ruleset_outcome_count_helper(rule_outcome["id"], rule_outcome_result_dict)

        # determine whether overall outcome is pass/fail/undetermined/not_applicable
        overall_result = self.calculate_rule_outcome(rule_outcome_result_dict)
        self.ruleset_outcome[section_dict[rule_outcome["id"].split("-")[0]]][
            overall_result
        ] += 1
        self.ruleset_outcome["All"][overall_result] += 1

        # calculate pass/fail/undetermined/not applicable rate
        no_of_applicable_component = sum(rule_outcome_result_dict.values())
        multiplier = 100 / no_of_applicable_component
        pass_rate = int(rule_outcome_result_dict[RCTOutcomeLabel.PASS] * multiplier)
        fail_rate = int(rule_outcome_result_dict[RCTOutcomeLabel.FAILED] * multiplier)
        undetermined_rate = int(
            rule_outcome_result_dict[RCTOutcomeLabel.UNDETERMINED] * multiplier
        )
        not_applicable_rate = int(
            rule_outcome_result_dict[RCTOutcomeLabel.NOT_APPLICABLE] * multiplier
        )

        one_rule_report = f"""
  - **Rule Id**: {rule_outcome["id"]}
    - **Description**: {rule_outcome["description"]}
    - **90.1-2019 Section**: {rule_outcome['standard_section']}
    - **Overall Rule Evaluation Outcome**: {overall_result}
    - **Number of applicable components**: {no_of_applicable_component} 
      
      | Pass %: {pass_rate}| Fail %: {fail_rate}| Not applicable %: {not_applicable_rate}| Undetermined %: {undetermined_rate}| 
      |:--------------:|:--------------:|:--------------:|:--------------:|
        """
        return "".join(
            filter(
                None, [self._section_name_helper(rule_outcome["id"]), one_rule_report]
            )
        )

    def add_rule_to_ruleset_report(self, ruleset_report, rule_report, rule_outcome):
        self.summary_report = "".join([self.summary_report, rule_report])

    def save_ruleset_report(self, ruleset_report, report_dir):
        overall_rules_count = {name: 0 for name in section_list}

        for key in self.ruleset_outcome:
            for outcome in [
                RCTOutcomeLabel.PASS,
                RCTOutcomeLabel.FAILED,
                RCTOutcomeLabel.UNDETERMINED,
                RCTOutcomeLabel.NOT_APPLICABLE,
            ]:
                overall_rules_count[key] += self.ruleset_outcome[key][outcome]

        (
            rules_line,
            pass_line,
            fail_line,
            not_applicable_line,
            undetermined_line,
        ) = self._generate_line(self.ruleset_outcome, overall_rules_count)

        self.summary_report = re.sub("Replace-Rules", rules_line, self.summary_report)
        self.summary_report = re.sub("Replace-Pass", pass_line, self.summary_report)
        self.summary_report = re.sub("Replace-Fail", fail_line, self.summary_report)
        self.summary_report = re.sub(
            "Replace-Not_Applicable", not_applicable_line, self.summary_report
        )
        self.summary_report = re.sub(
            "Replace-Undetermined", undetermined_line, self.summary_report
        )

        with open(report_dir, "w", encoding="utf-8") as output_report:
            output_report.write(self.summary_report)

    def _section_name_helper(self, rule_outcome):
        section_no = rule_outcome.split("-")[0]
        if f"Section: {section_dict[section_no]}" not in self.summary_report:
            return f"""
### Section: {section_dict[section_no]}
            """
        else:
            return None

    def _generate_line(self, outcome_data, overall_rules_count):
        rule_line = "|Rules|"
        pass_line = "|Pass|"
        fail_line = "|fail|"
        not_applicable_line = f"|Not Applicable|"
        undetermined_line = f"|Undetermined (manual review)|"

        for section_name, count in overall_rules_count.items():
            rule_line += f"{overall_rules_count[section_name]}|"

        for section in section_list:
            pass_line += f"{outcome_data[section][RCTOutcomeLabel.PASS]}|"
            fail_line += f"{outcome_data[section][RCTOutcomeLabel.FAILED]}|"
            not_applicable_line += (
                f"{outcome_data[section][RCTOutcomeLabel.NOT_APPLICABLE]}|"
            )
            undetermined_line += (
                f"{outcome_data[section][RCTOutcomeLabel.UNDETERMINED]}|"
            )

        return rule_line, pass_line, fail_line, not_applicable_line, undetermined_line
