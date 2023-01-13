import json
import os
from pathlib import Path

from rct229.schema.schema_utils import quantify_rmr

SYSTEM_TYPE_TEST_FILE_PATH = os.path.join(
    Path(os.path.dirname(__file__)).parent.parent,
    "ruletest_engine",
    "ruletest_jsons",
    "system_types",
)


def load_system_test_file(file_name: str):
    with open(os.path.join(SYSTEM_TYPE_TEST_FILE_PATH, file_name)) as f:
        system_test_json = json.load(f)

    assert system_test_json, f"Error loading system testing json file: #{file_name}"
    return quantify_rmr(system_test_json)
