from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition

from .rule_base_test import (
    BASE_RULE_ARGS,
    RMDS_WITH_MATCHING_USER_AND_BASELINE,
    DERIVED_RULE_outcome_base,
)


class _PartilaRule(PartialRuleDefinition):
    def __init__(self, data=None):
        super(_PartilaRule, self).__init__(**BASE_RULE_ARGS)

    def get_calc_vals(self, context, data=None):
        return [{"a": 0}, 1]

    def applicability_check(self, context, calc_vals, data):
        return data["outcome"]


PARTIAL_RULE = _PartilaRule()


def test__rule_definition_base__evaluate__with_true_secondary_rule_check():
    assert PARTIAL_RULE.evaluate(
        RMDS_WITH_MATCHING_USER_AND_BASELINE,
        data={"outcome": True},
    ) == {
        **DERIVED_RULE_outcome_base,
        "result": "UNDETERMINED",
        "primary_rule": False,
        "message": "Manual check required message",
    }


def test__rule_definition_base__evaluate__with_false_secondary_rule_check():
    assert PARTIAL_RULE.evaluate(
        RMDS_WITH_MATCHING_USER_AND_BASELINE,
        data={"outcome": False},
    ) == {
        **DERIVED_RULE_outcome_base,
        "result": "NOT_APPLICABLE",
        "primary_rule": False,
        "message": "Not applicable message",
    }
