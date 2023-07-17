import re

from rct229.report_engine.rct_report import RCTReport
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel


class ASHRAE9012019SummaryReport(RCTReport):
    def __init__(self, input_dict):
        super(ASHRAE9012019SummaryReport, self).__init__()
        self.title = "ASHRAE STD 229P RULESET CHECKING TOOL"
        self.purpose = "Summary Report"
        self.ruleset = "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)"
        self.schema_version = "0.0.23"
        self.ruleset_report_file = "ashrae901_2019_summary_report.md"
        self.user_rmd = input_dict["user_rmd"]
        self.proposed_rmd = input_dict["proposed_rmd"]
        self.baseline_rmd = input_dict["baseline_rmd"]

    def initialize_ruleset_report(self):
        self.section_list = [
            "All",
            "Envelope",
            "Lighting",
            "Receptacles",
            "Transformers",
            "HVAC-General",
            "HVAC-HotWaterSide",
            "HVAC-ChilledWaterSide",
            "HVAC-AirSide",
        ]
        self.section_dict = {
            "5": "Envelope",
            "6": "Lighting",
            "12": "Receptacles",
            "15": "Transformers",
            "19": "HVAC-General",
            "21": "HVAC-HotWaterSide",
            "22": "HVAC-ChilledWaterSide",
            "23": "HVAC-AirSide",
        }
        self.ruleset_outcome = {
            name: {
                RCTOutcomeLabel.PASS: 0,
                RCTOutcomeLabel.FAILED: 0,
                RCTOutcomeLabel.UNDETERMINED: 0,
                RCTOutcomeLabel.NOT_APPLICABLE: 0,
            }
            for name in self.section_list
        }
        self.summary_report = f"""
## {self.title}
### {self.purpose} 
##### {self.ruleset}
##### Date: {self.date_run}

### RMD Files
- user: {self.user_rmd.split('/')[-1]}
- proposed: {self.proposed_rmd.split('/')[-1]}
- baseline: {self.baseline_rmd.split('/')[-1]}

### Summary: All Primary Rules
|                              | All | Envelope | Lighting | Receptacles | Transformers | HVAC-HotWaterSide | HVAC - ChilledWaterSide | HVAC-AirSide | HVAC-General|
|:----------------------------:|:---:|:--------:|:--------:|:-----------:|:------------:|:--------------:|:--------------:|:--------------:|:--------------:|
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
        self.ruleset_outcome[self.section_dict[rule_outcome["id"].split("-")[0]]][
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
        overall_rules_count = {name: 0 for name in self.section_list}

        for key in self.ruleset_outcome.keys():
            for outcome in [
                RCTOutcomeLabel.PASS,
                RCTOutcomeLabel.FAILED,
                RCTOutcomeLabel.UNDETERMINED,
                RCTOutcomeLabel.NOT_APPLICABLE,
            ]:
                overall_rules_count[key] += self.ruleset_outcome[key][outcome]

        rules_line = f"|Rules|{overall_rules_count['All']}|{overall_rules_count['Envelope']}|{overall_rules_count['Lighting']}|{overall_rules_count['Receptacles']}|{overall_rules_count['Transformers']}|{overall_rules_count['HVAC-WaterSide']}|{overall_rules_count['HVAC-Chiller']}|"
        pass_line = f"|Pass|{self.ruleset_outcome['All'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['HVAC-Chiller'][RCTOutcomeLabel.PASS]}|"
        fail_line = f"|Fail|{self.ruleset_outcome['All'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['HVAC-Chiller'][RCTOutcomeLabel.FAILED]}|"
        not_applicable_line = f"|Not Applicable|{self.ruleset_outcome['All'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['HVAC-Chiller'][RCTOutcomeLabel.NOT_APPLICABLE]}|"
        undetermined_line = f"|Undetermined (manual review)|{self.ruleset_outcome['All'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['HVAC-Chiller'][RCTOutcomeLabel.UNDETERMINED]}|"

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
        if f"Section: {self.section_dict[section_no]}" not in self.summary_report:
            return f"""
### Section: {self.section_dict[section_no]}
            """
        else:
            return None
