import click

from rct229.reports.project_report import (
    print_json_report,
    print_rule_report,
    print_summary_report,
)
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
short_help_text = "Test RMR triplet."
help_text = short_help_text


@cli.command("evaluate", short_help=short_help_text, help=help_text, hidden=True)
@click.argument("user_rmr", type=click.File("rb"))
@click.argument("baseline_rmr", type=click.File("rb"))
@click.argument("proposed_rmr", type=click.File("rb"))
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

        report = evaluate_all_rules(user_rmr_obj, baseline_rmr_obj, proposed_rmr_obj)

        # Example - Print a final compliance report
        # [We'll actually most likely save a data file here and report occurs from separate CLI command]
        # print_json_report(report)
        print_rule_report(report)
        print_summary_report(report)

        print("Rules completed.")
        print("")

    # # Validate the rmrs against the schema and other high-level checks
    # user_validation = validate_rmr(user_rmr_obj)
    # if user_validation["passed"] is not True:
    #     print("User RMR is " + user_validation["error"])
    #
    # baseline_validation = validate_rmr(baseline_rmr_obj)
    # if baseline_validation["passed"] is not True:
    #     print("Baseline RMR is " + baseline_validation["error"])
    #
    # proposed_validation = validate_rmr(proposed_rmr_obj)
    # if proposed_validation["passed"] is not True:
    #     print("Proposed RMR is " + proposed_validation["error"])
    #
    # print("")
    #
    # if user_validation["passed"] and baseline_validation["passed"] and proposed_validation["passed"]:
    #     print("Processing rules...")
    #     print("")
    #     evaluate_all_rules(user_rmr_obj, baseline_rmr_obj, proposed_rmr_obj)
    #     print("Rules completed.")
    #     print("")


if __name__ == "__main__":
    cli()
