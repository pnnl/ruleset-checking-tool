from rct229.report_engine.rct_report import RCTReport
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel


class EngineRawSummary(RCTReport):
    def __init__(self):
        super(EngineRawSummary, self).__init__()
        self.ruleset_report_file = f"{self.__class__.__name__}.txt"
        self.num_evaluation = 0

    def generate_rule_report(self, rule_outcome, outcome_dict):
        string_list = []
        string_list.append(
            "--------------------------------------------------------------------\n"
        )
        string_list.append(f"Rule: {str(rule_outcome['id'])}\n")
        string_list.append(f"Description: {str(rule_outcome['description'])}\n")
        string_list.append(
            f"RMD context: {str(rule_outcome['rmd_context'])}\n"
        ) if "rmd_context" in rule_outcome else string_list.append(
            "RMD context: full scope\n"
        )
        string_list.append(f"Rule result: {str(rule_outcome['result'])}\n")
        string_list.append(
            "--------------------------------------------------------------------\n"
        )
        self.num_evaluation = self._rule_outcome_helper(
            rule_outcome["result"], outcome_dict
        )
        return string_list

    def add_rule_to_ruleset_report(self, ruleset_report, rule_report, rule_outcome):
        ruleset_report.extend(rule_report)
        self.ruleset_outcome[rule_outcome] += 1

    def save_ruleset_report(self, ruleset_report, output_dir):
        # add summary to the string
        ruleset_report.append("----------------------------------\n")
        ruleset_report.append("Summary\n")
        ruleset_report.append(f"{self.num_evaluation} evaluations\n")
        ruleset_report.append(
            f"{self.ruleset_outcome[RCTOutcomeLabel.PASS]} evaluations passed\n"
        )
        ruleset_report.append(
            f"{self.ruleset_outcome[RCTOutcomeLabel.FAILED]} evaluations failed\n"
        )
        ruleset_report.append(
            f"{self.ruleset_outcome[RCTOutcomeLabel.NOT_APPLICABLE]} evaluations not applicable\n"
        )
        ruleset_report.append(
            f"{self.ruleset_outcome[RCTOutcomeLabel.UNDETERMINED]} evaluations requiring manual check\n"
        )
        ruleset_report.append("----------------------------------\n")

        with open(output_dir, "w") as output_report:
            output_report.write("".join(ruleset_report))

    def _rule_outcome_helper(self, rule_outcomes, outcomes_dict):
        num_evaluation = 0

        def _count_result(number_evaluation, rule_outcome, outcome_dict):
            if type(rule_outcome) is str:
                return
            else:
                for outcome in rule_outcome:
                    number_evaluation += 1
                    if type(outcome) is dict:
                        if outcome["result"] == RCTOutcomeLabel.FAILED:
                            outcome_dict[RCTOutcomeLabel.FAILED] += 1
                        elif outcome["result"] == RCTOutcomeLabel.PASS:
                            outcome_dict[RCTOutcomeLabel.PASS] += 1
                        elif outcome["result"] == RCTOutcomeLabel.UNDETERMINED:
                            outcome_dict[RCTOutcomeLabel.UNDETERMINED] += 1
                        elif outcome["result"] == RCTOutcomeLabel.NOT_APPLICABLE:
                            outcome_dict[RCTOutcomeLabel.NOT_APPLICABLE] += 1
                    elif type(outcome_dict) is list:
                        number_evaluation -= 1
                        _count_result(number_evaluation, outcome_dict, outcome_dict)
            _count_result(num_evaluation, rule_outcomes, outcomes_dict)

        return num_evaluation
