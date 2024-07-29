import os
import pytest
from rct229.rule_engine.rulesets import RuleSet
from rct229.ruletest_engine.ruletest_engine import run_section_tests


def test__ruletest_engine__all_pass():

    test_json_name = "test_engine_dict_test_file_all_pass.json"
    ruleset_doc = RuleSet.ASHRAE9012019_RULESET
    test_json_path = os.path.join(os.path.dirname(__file__), "test_files")

    assert run_section_tests(test_json_name, ruleset_doc, test_json_path)


def test__ruletest_engine__incorrect_pass():

    test_json_name = "test_engine_dict_test_file_incorrect_fail.json"
    ruleset_doc = RuleSet.ASHRAE9012019_RULESET
    test_json_path = os.path.join(os.path.dirname(__file__), "test_files")

    assert not run_section_tests(test_json_name, ruleset_doc, test_json_path)


def test__ruletest_engine__incorrect_failure():

    test_json_name = "test_engine_dict_test_file_incorrect_pass.json"
    ruleset_doc = RuleSet.ASHRAE9012019_RULESET
    test_json_path = os.path.join(os.path.dirname(__file__), "test_files")

    assert not run_section_tests(test_json_name, ruleset_doc, test_json_path)


def test__ruletest_engine__incorrect_undetermined():
    test_json_name = "test_engine_dict_test_file_incorrect_undetermined.json"
    ruleset_doc = RuleSet.ASHRAE9012019_RULESET
    test_json_path = os.path.join(os.path.dirname(__file__), "test_files")

    assert not run_section_tests(test_json_name, ruleset_doc, test_json_path)


def test__ruletest_engine__incorrect_not_applicable():
    test_json_name = "test_engine_dict_test_file_incorrect_not_applicable.json"
    ruleset_doc = RuleSet.ASHRAE9012019_RULESET
    test_json_path = os.path.join(os.path.dirname(__file__), "test_files")

    assert not run_section_tests(test_json_name, ruleset_doc, test_json_path)


def test__ruletest_engine__missing_expected_outcome(capfd):
    test_json_name = "test_engine_dict_test_file_missing_expected_outcome.json"
    ruleset_doc = RuleSet.ASHRAE9012019_RULESET
    test_json_path = os.path.join(os.path.dirname(__file__), "test_files")

    assert not run_section_tests(test_json_name, ruleset_doc, test_json_path)

    out, err = capfd.readouterr()
    assert "is not a valid rule outcome. Expected 'pass', 'fail','undetermined'" in out
