import click

from rct229.reports.ashrae901_2019_detail_report import ASHRAE9012019DetailReport
from rct229.reports.ashrae901_2019_summary_report import ASHRAE9012019SummaryReport
from rct229.reports.engine_raw_output import EngineRawOutput
from rct229.reports.engine_raw_summary import EngineRawSummary
from rct229.rule_engine.engine import evaluate_all_rules
from rct229.rule_engine.rulesets import RuleSet, RuleSetTest
from rct229.ruletest_engine.run_ruletests import run_ashrae9012019_tests
from rct229.schema.schema_store import SchemaStore
from rct229.schema.validate import validate_rmr

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
REPORT_MODULE = {
    "RAW_OUTPUT": EngineRawOutput,
    "RAW_SUMMARY": EngineRawSummary,
    "ASHRAE9012019_DETAIL": ASHRAE9012019DetailReport,
    "ASHRAE9012019_SUMMARY": ASHRAE9012019SummaryReport,
}


def print_version():
    click.echo(f"{__name__}, version {__version__}")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(None, "-v", "--version")
def cli():
    """
    ASHRAE 229 - Ruleset Checking Tool
    """


# Software Test Workflow
test_short_help_text = (
    """
    Software test workflow, add sections to do test. \n
    --ruleset or -rs: default is ashrae9012019, available: ashrae9012019\n
    argument (optional): section string, \n
    currently available: section5, section6, section18, section19, section21, section22 and section23"""
)


@cli.command(
    "test", short_help=test_short_help_text, help=test_short_help_text, hidden=True
)
@click.option("--ruleset", "-rs", multiple=False, default="ashrae9012019")
@click.argument("section", type=click.STRING, required=False)
def run_test(ruleset, section=None):
    print(f"software test workflow for section {section}")
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        outcome_list = run_ashrae9012019_tests(section)
        if section is None:
            for idx, outcome in enumerate(outcome_list):
                assert (
                    outcome
                ), f"{RuleSetTest.ASHRAE9012019_TEST_LIST[idx]} failed in the test"
        else:
            assert all(outcome_list), f"{section} failed in the test"
    else:
        print(
            f"ruleset document {ruleset} is not currently supported by the RCT. Please select one from the following: ashrae9012019"
        )


# Evaluate RMR Triplet
short_help_text = """
    Run ruleset checking. arguments are \n
    --rpds or -f: rpd file directory. accept multiple entries, example: -f ../example/user_model.rpd \n
    --ruleset or -rs: ruleset name. Default is ashrae9012019, available options include: ashrae9012019 \n
    --reports or -r: reports. Default is RAW_OUTPUT, accept multiple entries, available options include: RAW_OUTPUT, RAW_SUMMARY, ASHRAE9012019_DETAIL, ASHRAE9012019_SUMMARY. \n
    --reports_directory or -rd: directory to save the output reports. \n
    """
help_text = short_help_text


@cli.command("evaluate", short_help=short_help_text, help=help_text, hidden=True)
@click.option("--rpds", "-f", multiple=True, default=[])
@click.option("--ruleset", "-rs", multiple=False, default="ashrae9012019")
@click.option("--reports", "-r", multiple=True, default=["RAW_OUTPUT"])
@click.option(
    "--reports_directory", "-rd", multiple=False, default="./examples/output/"
)
def evaluate(rpds, ruleset, reports, reports_directory):
    # TODO need to switch this to a if-else for selecting rulesets
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        print("Test implementation of rule engine for ASHRAE Std 229 RCT.")
        print("")
        report = evaluate_all_rules(rpds)
    # have report attached.
    print(f"Saving reports to: {reports_directory}......")
    for report_type in reports:
        report_module = REPORT_MODULE[report_type]()
        report_module.generate(report, reports_directory)


if __name__ == "__main__":
    cli()
