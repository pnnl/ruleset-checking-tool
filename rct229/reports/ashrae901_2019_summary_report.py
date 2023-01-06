from rct229.report_engine.rct_report import RCTReport


class ASHRAE9012019SummaryReport(RCTReport):
    def __init__(self):
        super(ASHRAE9012019SummaryReport, self).__init__()
        self.title = "ASHRAE STD 229P RULESET CHECKING TOOL"
        self.purpose = "Summary Report"
        self.ruleset = "ASHRAE 90.1-2019 Performance Rating Method (Appendix G)"
        self.schema_version = "0.0.18"
        self.ruleset_report_file = "ashrae901_2019_summary_report.md"

    def initialize_ruleset_report(self):
        summary_title = f"""
        ##{self.title}
        
        
        """
