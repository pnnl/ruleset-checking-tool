from pathlib import Path
import zipfile
import json

from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_store import SchemaStore
from rct229.schema.schema_enums import SchemaEnums
from rct229.rule_engine.engine import evaluate_all_rules
from rct229.reports import reports as rct_report

INTEGRATED_TEST_DIR = Path(__file__).resolve().parent


def extract_rpd_from_zip(zip_path: Path) -> Path:
    """
    Extract the JSON RPD file from a ZIP archive and return the extracted file path.

    Parameters
    ----------
    zip_path: Path
        Path to the ZIP file containing the RPD JSON.

    Returns
    -------
    Path
        Path to the extracted RPD JSON file.
    """
    extract_dir = zip_path.parent
    extract_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    # Find the first .json file in the extracted directory
    json_files = list(extract_dir.rglob("*.rpd"))
    if not json_files:
        raise FileNotFoundError(f"No RPD file found in archive: {zip_path}")
    return json_files[0]


def evaluate(rpds, ruleset, reports, reports_directory: Path):
    if ruleset == RuleSet.ASHRAE9012019_RULESET:
        SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
        SchemaEnums.update_schema_enum()
        print("Test implementation of rule engine for ASHRAE Std 229 RCT.\n")

    available_report_modules = rct_report.__getreports__()
    available_report_dict = {key: value for key, value in available_report_modules}
    available_report_str = list(available_report_dict.keys())

    for report_type in reports:
        if report_type not in available_report_dict:
            raise ValueError(
                f"Cannot find matching report type for {report_type}. "
                f"Available ones are {available_report_str}."
            )

    report = evaluate_all_rules(rpds)
    print(f"Saving reports to: {reports_directory}...")
    for report_type in reports:
        report_module = available_report_dict[report_type]()
        report_module.generate(report, reports_directory)


def run_sample_evaluation(rpd_file_path: Path, ruleset: str):
    """
    Run a single integration test on a given RPD file (ZIP) and ruleset.
    """
    if rpd_file_path.suffix == ".zip":
        rpd_json_path = extract_rpd_from_zip(rpd_file_path)
    else:
        rpd_json_path = rpd_file_path

    evaluate(
        [str(rpd_json_path)],
        ruleset,
        reports=["ASHRAE9012019DetailReport"],
        reports_directory=rpd_file_path.parent,
    )


def run_all_sample_evaluations():
    """
    Run sample integration tests on predefined RPD files and rulesets.
    """
    sample_tests = [
        {
            "rpd_file_path": INTEGRATED_TEST_DIR / f"Sample {i}" / f"Sample {i}.zip",
            "ruleset": RuleSet.ASHRAE9012019_RULESET,
        }
        for i in range(1, 6)
    ]

    for test in sample_tests:
        run_sample_evaluation(test["rpd_file_path"], test["ruleset"])


def run_sample_number_evaluation(sample_number: int, ruleset: str):
    """
    Evaluate a specific sample RPD file (ZIP) by its sample number.
    """
    rpd_file_path = (
        INTEGRATED_TEST_DIR / f"Sample {sample_number}" / f"Sample {sample_number}.zip"
    )
    run_sample_evaluation(rpd_file_path, ruleset)


def verify_report_alignment():
    """
    Check that each Sample directory contains the expected report and outcomes.
    """
    for sample_dir in INTEGRATED_TEST_DIR.iterdir():
        if sample_dir.is_dir() and sample_dir.name.startswith("Sample"):
            print(f"Verifying report alignment for {sample_dir.name}...")
            report_file = sample_dir / "ASHRAE9012019DetailReport.json"
            expected_outcome_file = sample_dir / "expected_outcomes.json"

            if not report_file.exists():
                print(
                    f"Report file not found for {sample_dir.name}, skipping alignment check."
                )
                continue
            if not expected_outcome_file.exists():
                print(
                    f"Expected outcomes file not found for {sample_dir.name}, skipping alignment check."
                )
                continue

            with report_file.open(
                "r", encoding="utf-8"
            ) as rf, expected_outcome_file.open("r", encoding="utf-8") as ef:
                report_data = json.load(rf)
                expected_data = json.load(ef)

            for rule in report_data.get("rules", []):
                rule_id = rule.get("rule_id")
                if rule_id not in expected_data:
                    raise ValueError(
                        f"Rule ID {rule_id} found in report but not in expected outcomes for {sample_dir.name}."
                    )

                expected_rule_evals = expected_data[rule_id]

                for evaluation in rule.get("evaluations", []):
                    data_group_id = evaluation.get("data_group_id")
                    if data_group_id not in expected_rule_evals:
                        print(
                            f"Data Group ID {data_group_id} (Rule ID {rule_id} found "
                            f"in report but not in expected outcomes for {sample_dir.name})."
                        )
                        continue

                    expected_eval = expected_rule_evals[data_group_id]

                    # Compare outcome
                    if evaluation.get("outcome") != expected_eval.get("outcome"):
                        print(
                            f"Outcome mismatch in {sample_dir.name} (Rule ID: {rule_id}, "
                            f"Data Group ID: {data_group_id})."
                        )

                    # Compare calculated values
                    reported_calc_vals = evaluation.get("calculated_values", "")
                    expected_calc_vals = expected_eval.get("calculated_values", "")

                    # Case: Both empty → OK
                    if (reported_calc_vals == "" or reported_calc_vals == []) and (
                        expected_calc_vals == "" or expected_calc_vals == []
                    ):
                        pass

                    # Case: One empty but not the other → mismatch
                    elif (reported_calc_vals == "" and expected_calc_vals != "") or (
                        expected_calc_vals == "" and reported_calc_vals != ""
                    ):
                        print(
                            f"Calculated values presence mismatch in {sample_dir.name} "
                            f"(Rule ID: {rule_id}, Data Group ID: {data_group_id}). "
                            f"Expected: {expected_calc_vals} | Got: {reported_calc_vals}"
                        )

                    else:
                        # Both should be lists of dicts
                        if not isinstance(reported_calc_vals, list) or not isinstance(
                            expected_calc_vals, list
                        ):
                            print(
                                f"Invalid calculated_values format in {sample_dir.name} "
                                f"(Rule ID: {rule_id}, Data Group ID: {data_group_id})."
                            )
                            continue

                        # Convert lists to dicts keyed by "variable"
                        reported_dict = {
                            cv["variable"]: cv["value"]
                            for cv in reported_calc_vals
                            if "variable" in cv
                        }
                        expected_dict = {
                            cv["variable"]: cv["value"]
                            for cv in expected_calc_vals
                            if "variable" in cv
                        }

                        # Compare only expected variables
                        for variable, expected_value in expected_dict.items():

                            if variable not in reported_dict:
                                print(
                                    f"Missing calculated variable '{variable}' in {sample_dir.name} "
                                    f"(Rule ID: {rule_id}, Data Group ID: {data_group_id}) ."
                                )
                                continue

                            reported_value = reported_dict[variable]
                            if reported_value != expected_value:
                                print(
                                    f"Calculated value mismatch in {sample_dir.name} "
                                    f"(Rule {rule_id}, Data Group {data_group_id}, Variable '{variable}') "
                                    f"Expected: {expected_value} | Got: {reported_value}"
                                )

                    # Compare messages
                    if evaluation.get("messages") != expected_eval.get("messages"):
                        print(
                            f"Messages mismatch in {sample_dir.name} for Rule ID: {rule_id}, "
                            f"Data Group ID: {data_group_id}."
                        )


if __name__ == "__main__":
    # Example usage:
    # run_sample_number_evaluation(1, RuleSet.ASHRAE9012019_RULESET)

    # run_all_sample_evaluations()

    verify_report_alignment()
