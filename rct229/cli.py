import click

from rct229.reports.ashrae901_2019_detail_report import ASHRAE9012019DetailReport
from rct229.reports.engine_raw_output import EngineRawOutput
from rct229.reports.engine_raw_summary import EngineRawSummary
from rct229.rule_engine.engine import evaluate_all_rules
from rct229.utils.file import deserialize_rmr_file

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
REPORT_MODULE = {
    "RAW_OUTPUT": EngineRawOutput,
    "RAW_SUMMARY": EngineRawSummary,
    "ASHRAE9012019_DETAIL": ASHRAE9012019DetailReport,
}


def print_version():
    click.echo(f"{__name__}, version {__version__}")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(None, "-v", "--version")
def cli():
    """
    ASHRAE 229 - Ruleset Checking Tool
    """


# Evaluate RMR Triplet
short_help_text = """
    Test RMD triplet. arguments are user_rmd, baseline_rmd, proposed_rmd
    --reports or -r: reports. Default is RAW_OUTPUT, available options include RAW_OUTPUT, RAW_SUMMARY, ASHRAE9012019_DETAIL, multiple allowed.
    """
help_text = short_help_text


@cli.command("evaluate", short_help=short_help_text, help=help_text, hidden=True)
@click.argument("user_rmd", type=click.File("rb"))
@click.argument("baseline_rmd", type=click.File("rb"))
@click.argument("proposed_rmd", type=click.File("rb"))
@click.option("--reports", "-r", multiple=True, default=["RAW_OUTPUT"])
def evaluate(user_rmd, baseline_rmd, proposed_rmd, reports):
    report = evaluate_rmr_triplet(user_rmd, baseline_rmd, proposed_rmd)
    # have report attached.
    for report_type in reports:
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
