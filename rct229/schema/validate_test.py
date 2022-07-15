import json
import os

import pytest

from rct229.schema.validate import validate_rmr

EXAMPLES_PATH = "examples"

# Testing validate_rmr; intended to make sure the referenced schemas are connected
# properly and that the example rmr files are schema valid


def test__validate_rmr__with_baseline_rmr():
    with open(os.path.join(EXAMPLES_PATH, "baseline_rmd.json")) as rmr_file:
        rmr_obj = json.load(rmr_file)
    assert validate_rmr(rmr_obj) == {"passed": True, "error": None}


def test__validate_rmr__with_proposed_rmr():
    with open(os.path.join(EXAMPLES_PATH, "proposed_rmd.json")) as rmr_file:
        rmr_obj = json.load(rmr_file)
    assert validate_rmr(rmr_obj) == {"passed": True, "error": None}


def test__validate_rmr__with_user_rmr():
    with open(os.path.join(EXAMPLES_PATH, "user_rmd.json")) as rmr_file:
        rmr_obj = json.load(rmr_file)
    assert validate_rmr(rmr_obj) == {"passed": True, "error": None}
