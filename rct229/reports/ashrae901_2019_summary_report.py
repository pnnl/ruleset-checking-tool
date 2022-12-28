import re

from rct229.report_engine.rct_report import RCTReport
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel


class ASHRAE9012019SummaryReport(RCTReport):
    def __init__(self):
        super(ASHRAE9012019SummaryReport, self).__init__()
        self.title = "ASHRAE STD 229P RULESET CHECKING TOOL"
        self.purpose = "Summary Report"
        self.ruleset = "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)"
        self.schema_version = "0.0.23"
        self.ruleset_report_file = "ashrae901_2019_summary_report.md"

    def initialize_ruleset_report(self):
        self.section_list = [
            "All",
            "Envelope",
            "Lighting",
            "Receptacles",
            "Transformers",
            "HVAC-General",
            "HVAC-AirSide",
            "HVAC-WaterSide",
        ]
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
##### Schema version: {self.schema_version}

### RMD Files
- user: {'TO BE UPDATED!!'}
- proposed: {'TO BE UPDATED!!'}
- baseline: {'TO BE UPDATED!!'}

### Summary: All Rules
|                              | All | Envelope | Lighting | Receptacles | Transformers | HVAC-General | HVAC-AirSide | HVAC-WaterSide |
|:----------------------------:|:---:|:--------:|:--------:|:-----------:|:------------:|:------------:|:------------:|:--------------:|
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
                return result
            elif isinstance(result, list):
                return _parse_result_helper(result[0])
            elif isinstance(result, dict):
                if isinstance(result["result"], str):
                    return result["result"]
                elif isinstance(result["result"], list):
                    try:
                        return _parse_result_helper(result["result"][0])
                    except IndexError:
                        return "UNDETERMINED"  # if 'result' is empty, return undetermined for now
                elif isinstance(result["result"], dict):
                    return _parse_result_helper(result["result"])

        rule_outcome_result = _parse_result_helper(rule_outcome["result"])

        self.ruleset_outcome_count_helper(rule_outcome["id"], rule_outcome_result)

        pass_rate = 0
        fail_rate = 0
        undetermined_rate = 0
        not_applicable_rate = 0
        if rule_outcome_result == RCTOutcomeLabel.PASS:
            pass_rate = 100
        elif rule_outcome_result == RCTOutcomeLabel.FAILED:
            fail_rate = 100
        elif rule_outcome_result == RCTOutcomeLabel.UNDETERMINED:
            undetermined_rate = 100
        elif rule_outcome_result == RCTOutcomeLabel.NOT_APPLICABLE:
            not_applicable_rate = 100

        one_rule_report = f"""
  - **Rule Id**: {rule_outcome["id"]}
    - **Description**: {rule_outcome["description"]}
    - **90.1-2019 Section**: {'TO BE UPDATED!!'}
    - **Overall Rule Evaluation Outcome**: {rule_outcome_result}
    - **Number of applicable components**: {'TO BE UPDATED!!'} 
      | Pass %: {pass_rate} | Fail %: {fail_rate} | Not applicable %: {undetermined_rate} | Undetermined %: {not_applicable_rate} | 
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

        rules_line = f"| Rules |{overall_rules_count['All']}|{overall_rules_count['Envelope']}|{overall_rules_count['Lighting']}|{overall_rules_count['Receptacles']}|{overall_rules_count['Transformers']}|{overall_rules_count['HVAC-General']}|{overall_rules_count['HVAC-AirSide']}|{overall_rules_count['HVAC-WaterSide']}|"
        pass_line = f"| Pass |{self.ruleset_outcome['All'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['HVAC-General'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['HVAC-AirSide'][RCTOutcomeLabel.PASS]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.PASS]}|"
        fail_line = f"| Fail |{self.ruleset_outcome['All'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['HVAC-General'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['HVAC-AirSide'][RCTOutcomeLabel.FAILED]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.FAILED]}|"
        not_applicable_line = f"| Not Applicable |{self.ruleset_outcome['All'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['HVAC-General'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['HVAC-AirSide'][RCTOutcomeLabel.NOT_APPLICABLE]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.NOT_APPLICABLE]}|"
        undetermined_line = f"| Undetermined (manual review) |{self.ruleset_outcome['All'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Envelope'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Lighting'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Receptacles'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['Transformers'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['HVAC-General'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['HVAC-AirSide'][RCTOutcomeLabel.UNDETERMINED]}|{self.ruleset_outcome['HVAC-WaterSide'][RCTOutcomeLabel.UNDETERMINED]}|"

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
        if section_no == "5" and "Section: Envelope" not in self.summary_report:
            return """
#### Section: Envelope
        """
        elif section_no == "6" and "Section: Lighting" not in self.summary_report:
            return """
#### Section: Lighting
        """
        elif section_no == "12" and "Section: Receptacle" not in self.summary_report:
            return """
#### Section: Receptacle
        """
        elif section_no == "15" and "Section: Transformers" not in self.summary_report:
            return """
#### Section: Transformers
        """
        elif (
            section_no in ["21", "22"]
            and "Section: HVAC-WaterSide" not in self.summary_report
        ):
            return """
#### Section: HVAC-WaterSide
        """
        elif (
            section_no == "23" and "Section: Air-side system" not in self.summary_report
        ):
            return """
#### Section: HVAC-AirSide
        """
        else:
            return None

    def ruleset_outcome_count_helper(self, rule_outcome, rule_outcome_result):
        section_no = rule_outcome.split("-")[0]

        def _ruleset_outcome_count_helper(section_name, rule_outcome_result):
            if rule_outcome_result == RCTOutcomeLabel.PASS:
                self.ruleset_outcome[section_name][RCTOutcomeLabel.PASS] += 1
                self.ruleset_outcome["All"][RCTOutcomeLabel.PASS] += 1
            elif rule_outcome_result == RCTOutcomeLabel.FAILED:
                self.ruleset_outcome[section_name][RCTOutcomeLabel.FAILED] += 1
                self.ruleset_outcome["All"][RCTOutcomeLabel.FAILED] += 1
            elif rule_outcome_result == RCTOutcomeLabel.UNDETERMINED:
                self.ruleset_outcome[section_name][RCTOutcomeLabel.UNDETERMINED] += 1
                self.ruleset_outcome["All"][RCTOutcomeLabel.UNDETERMINED] += 1
            elif rule_outcome_result == RCTOutcomeLabel.NOT_APPLICABLE:
                self.ruleset_outcome[section_name][RCTOutcomeLabel.NOT_APPLICABLE] += 1
                self.ruleset_outcome["All"][RCTOutcomeLabel.NOT_APPLICABLE] += 1

        if section_no == "5":
            _ruleset_outcome_count_helper("Envelope", rule_outcome_result)
        elif section_no == "6":
            _ruleset_outcome_count_helper("Lighting", rule_outcome_result)
        elif section_no == "12":
            _ruleset_outcome_count_helper("Receptacles", rule_outcome_result)
        elif section_no == "15":
            _ruleset_outcome_count_helper("Transformers", rule_outcome_result)
        elif section_no in ["21", "22"]:
            _ruleset_outcome_count_helper("HVAC-WaterSide", rule_outcome_result)
        elif section_no == "23":
            _ruleset_outcome_count_helper("HVAC-AirSide", rule_outcome_result)
