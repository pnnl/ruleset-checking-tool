from pathlib import Path
import zipfile

from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_store import SchemaStore
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import RCTException
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
        raise RCTException(f"No RPD file found in archive: {zip_path}")
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
            raise RCTException(
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


if __name__ == "__main__":
    # Example usage:
    run_sample_number_evaluation(1, RuleSet.ASHRAE9012019_RULESET)

    # run_all_sample_evaluations()

    # verify_report_alignment()
