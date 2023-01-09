import click

from rct229.reports.ashrae901_2019_detail_report import ASHRAE9012019DetailReport
from rct229.reports.ashrae901_2019_summary_report import ASHRAE9012019SummaryReport
from rct229.reports.engine_raw_output import EngineRawOutput
from rct229.reports.engine_raw_summary import EngineRawSummary
from rct229.rule_engine.engine import evaluate_all_rules
from rct229.ruletest_engine.run_ruletests import (
    run_boiler_tests,
    run_chiller_tests,
    run_envelope_tests,
    run_lighting_tests,
)
from rct229.schema.validate import validate_rmr
from rct229.utils.file import deserialize_rmr_file

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
    "Software test workflow, add sections to do test. argument (optional): section string, "
    "currently available: section5, section6, section 21, section 22 "
)


@cli.command(
    "test", short_help=test_short_help_text, help=test_short_help_text, hidden=True
)
@click.argument("section", type=click.STRING, required=False)
def run_test(section=None):
    if section:
        print(f"software test workflow for section {section}")
        if section == "section5":
            assert run_envelope_tests(), "Failed section 5 tests"
        elif section == "section6":
            assert run_lighting_tests(), "Failed section 6 tests"
        # elif section == "section15":
        #    assert run_transformer_tests(), "Failed section 15 tests"
        elif section == "section21":
            assert run_boiler_tests(), "Failed section 21 tests"
        elif section == "section22":
            assert run_chiller_tests(), "Failed section 22 tests"
    else:
        print(f"software test workflow for all tests")
        # assert run_transformer_tests(), "Failed section 15 tests"
        assert run_lighting_tests(), "Failed section 6 tests"
        assert run_envelope_tests(), "Failed section 5 tests"
        assert run_boiler_tests(), "Failed section 21 tests"
        assert run_chiller_tests(), "Failed section 22 tests"


# Evaluate RMR Triplet
short_help_text = """
    Test RMD triplet. arguments are user_rmd, baseline_rmd, proposed_rmd
    --reports or -r: reports. Default is RAW_OUTPUT, available options include RAW_OUTPUT, RAW_SUMMARY, ASHRAE9012019_DETAIL, multiple allowed.
    """
help_text = short_help_text


@cli.command("evaluate", short_help=short_help_text, help=help_text, hidden=True)
@click.argument("user_rmd", type=click.File("r"))
@click.argument("baseline_rmd", type=click.File("r"))
@click.argument("proposed_rmd", type=click.File("r"))
@click.option("--reports", "-r", multiple=True, default=["RAW_OUTPUT"])
def evaluate(user_rmd, baseline_rmd, proposed_rmd, reports):
    report = evaluate_rmr_triplet(user_rmd, baseline_rmd, proposed_rmd)
    # have report attached.

    props = {
        "user_rmd": user_rmd.name,
        "proposed_rmd": proposed_rmd.name,
        "baseline_rmd": baseline_rmd.name,
    }
    for report_type in reports:
        if report_type == "ASHRAE9012019_SUMMARY":
            report_module = REPORT_MODULE[report_type](props)
        else:
            report_module = REPORT_MODULE[report_type]()
        report_module.generate(report, "./examples/output/")


def evaluate_rmr_triplet(user_rmr, baseline_rmr, proposed_rmr):
    print("Test implementation of rule engine for ASHRAE Std 229 RCT.")
    print("")

    user_rmr_obj = None
    baseline_rmr_obj = None
    proposed_rmr_obj = None
    rmr_are_valid_json = True
    try:
        user_rmr_obj = deserialize_rmr_file(user_rmr)
    except:
        rmr_are_valid_json = False
        print("User RMR is not a valid JSON file")
    try:
        baseline_rmr_obj = deserialize_rmr_file(baseline_rmr)
    except:
        rmr_are_valid_json = False
        print("Baseline RMR is not a valid JSON file")
    try:
        proposed_rmr_obj = deserialize_rmr_file(proposed_rmr)
    except:
        rmr_are_valid_json = False
        print("Proposed RMR is not a valid JSON file")

    if not rmr_are_valid_json:
        print("")
        return
    else:
        print("Processing rules...")
        print("")

        return evaluate_all_rules(user_rmr_obj, baseline_rmr_obj, proposed_rmr_obj)


if __name__ == "__main__":
    cli()
