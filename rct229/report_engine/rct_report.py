import os
from datetime import datetime

from rct229 import __version__ as version

# rule outcome evaluation logic
from rct229.rule_engine.rct_outcome_label import RCTOutcomeLabel
from rct229.schema import config


class RCTReport:
    def __init__(self):
        self.title = "Ruleset Checking Tool"
        self.tool = "PNNL Ruleset Checking Tool"
        self.version = version
        self.purpose = "report"
        self.ruleset = "ruleset"
        self.date_run = str(datetime.utcnow())
        self.schema_version = config.schema_version
        self.ruleset_report_file = "report.txt"
        self.ruleset_outcome = {
            RCTOutcomeLabel.PASS: 0,
            RCTOutcomeLabel.FAILED: 0,
            RCTOutcomeLabel.UNDETERMINED: 0,
            RCTOutcomeLabel.NOT_APPLICABLE: 0,
        }

    def generate(self, rct_outcome, report_dir):
        """
        generate rule report. - do not modify/override this function
        This method also orchestrates the high-level workflow for any rule report
        1. initialize_ruleset_report(): initialize a ruleset data structure
        2. generate_rule_report(): generate a report for one rule
        3. calculate_rule_outcome(): calculates the rule outcome
        4. add_rule_to_ruleset_report(): append the rule outcome to the ruleset report
        5. save_ruleset_report(): save the ruleset report to the report_dir

        Parameters
        ----------
        rct_outcome: dict dictionary outcome generated from RCT engine
        report_dir: str report file that saves the report output.

        Returns - Save the output to a folder
        -------

        """
        invalid_msg = rct_outcome["invalid_rmds"]
        # Sort the outcomes by id or rule_id
        if "id" in rct_outcome["outcomes"][0]:
            id_key = "id"
        elif "rule_id" in rct_outcome["outcomes"][0]:
            id_key = "rule_id"
        else:
            raise Exception(
                f"rct_outcome['outcomes'] dictionary has neither a 'rule_id' or 'id' as a key. Cannot be "
                f"sorted"
            )

        outcomes = sorted(
            # The key used below splits the id on "-" and ensures the outcomes are sorted by the first components of the ids, then the second components, and so on
            rct_outcome["outcomes"],
            key=lambda x: [int(y) for y in x[id_key].split("-")],
        )

        if invalid_msg:
            print(f"Invalid RMDs: {str(invalid_msg)}\n")
        else:
            ruleset_report = self.initialize_ruleset_report(rct_outcome)
            for outcome in outcomes:
                # if outcome["primary_rule"]:  #  TODO Do we output ONLY primary rules?
                rule_outcome_dict = {
                    RCTOutcomeLabel.PASS: 0,
                    RCTOutcomeLabel.FAILED: 0,
                    RCTOutcomeLabel.UNDETERMINED: 0,
                    RCTOutcomeLabel.NOT_APPLICABLE: 0,
                }
                rule_report = self.generate_rule_report(outcome, rule_outcome_dict)
                rule_outcome = self.calculate_rule_outcome(rule_outcome_dict)
                self.add_rule_to_ruleset_report(
                    ruleset_report, rule_report, rule_outcome
                )
            report_dir = os.path.join(report_dir, self.ruleset_report_file)
            self.save_ruleset_report(ruleset_report, report_dir)

    def generate_rule_report(self, rule_outcome, outcome_dict):
        """
        Function to generate a rule's report

        Parameters
        ----------
        rule_outcome: json contains a rule's raw report
        outcome_dict: outcome dictionary, default is

        Returns:
        -------
        rule_outcome: a data structure contains the rule outcome

        """
        return rule_outcome

    def initialize_ruleset_report(self, rule_outcome=None):
        """
        Initialize a data structure for generating a ruleset report
        default is list

        Parameters
        ----------
        rule_outcome: json contains a rule's raw report

        Returns: data structure, default is list
        -------

        """
        return []

    def add_rule_to_ruleset_report(self, ruleset_report, rule_report, rule_outcome):
        """
        Add rule to the ruleset report - Subclass must implement this function

        Parameters
        ----------
        ruleset_report: type depends on the initialized ruleset report
        rule_report: type depends on the intialized ruleset re
        rule_outcome: dict, contains counts for four RCT outputs
        -------

        """
        raise NotImplementedError()

    def calculate_rule_outcome(self, outcome_dict):
        """
        Calculate the outcome of a rule - the outcome should always match
        to std 229 requirements.

        Parameters
        ----------
        outcome_dict: dict outcomes dictionary

        Returns: str outcome
        -------

        """
        outcome_label = RCTOutcomeLabel.NOT_APPLICABLE
        if outcome_dict[RCTOutcomeLabel.FAILED] > 0:
            outcome_label = RCTOutcomeLabel.FAILED
        elif outcome_dict[RCTOutcomeLabel.UNDETERMINED] > 0:
            outcome_label = RCTOutcomeLabel.UNDETERMINED
        elif outcome_dict[RCTOutcomeLabel.PASS] > 0:
            outcome_label = RCTOutcomeLabel.PASS
        return outcome_label

    def save_ruleset_report(self, ruleset_report, report_dir):
        """
        Save the ruleset report to a file. Subclass must implement this function

        Parameters
        ----------
        ruleset_report: user-defined data structure (should be consistent with the data defined in initialize_ruleset_report function
        report_dir: report file path.

        Returns NA
        -------

        """
        raise NotImplementedError()
