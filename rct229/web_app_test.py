from rct229.rule_engine.rulesets import RuleSet
from rct229.web_application import count_number_of_primary_rules, run_project_evaluation

print(count_number_of_primary_rules(RuleSet.ASHRAE9012019_RULESET))

import json
import os
from pathlib import Path


def load_rpds_from_file(json_path):
    with open(json_path, "r") as file:
        data = json.load(file)
    if isinstance(data, dict):
        return [data]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError(
            "Invalid JSON format for RPDs: must be a dict or list of dicts."
        )


def sample_run():
    # Change these paths and values as appropriate
    baseline = "baseline_model.json"
    proposed = "proposed_model.json"
    user = "user_model.json"
    ruleset = "ashrae9012019"  # Replace with a valid ruleset key
    reports = ["EngineRawSummary"]  # Replace with valid report enum values
    saving_dir = "./output_reports"
    session_id = "test_session_001"

    # Ensure output directory exists
    Path(saving_dir).mkdir(parents=True, exist_ok=True)

    # Load JSON file
    baseline_path = os.path.join(
        "../examples/chicago_demo", baseline
    )  # assuming test_data/sample_rpd.json exists
    proposed_path = os.path.join(
        "../examples/chicago_demo", proposed
    )  # assuming test_data/sample_rpd.json exists
    user_path = os.path.join(
        "../examples/chicago_demo", user
    )  # assuming test_data/sample_rpd.json exists
    rpds = load_rpds_from_file(baseline_path)
    rpds.extend(load_rpds_from_file(proposed_path))
    rpds.extend(load_rpds_from_file(user_path))

    # Run evaluation
    report_paths = run_project_evaluation(
        rpds=rpds,
        ruleset=ruleset,
        reports=reports,
        saving_dir=saving_dir,
        session_id=session_id,
    )

    # Print report paths
    print("\nGenerated report files:")
    for path in report_paths:
        print(f" - {path}")


# if __name__ == "__main__":
#     test_run()
