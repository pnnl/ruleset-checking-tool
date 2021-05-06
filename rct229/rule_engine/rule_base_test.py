import pytest

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals

rmr_1 = {
    "transformers": [
        {
            "name": "Transformer 1",
            "type": "DRY_TYPE",
            "phase": "SINGLE_PHASE",
            "efficiency": 0.9,
            "capacity": 500.0,
            "peak_load": 500.0,
        },
        {
            "name": "Transformer 2",
            "type": "DRY_TYPE",
            "phase": "SINGLE_PHASE",
            "efficiency": 0.9,
            "capacity": 500.0,
            "peak_load": 500.0,
        },
    ]
}

rmr_2 = {
    "transformers": [
        {
            "name": "Transformer 1",
            "type": "DRY_TYPE",
            "phase": "SINGLE_PHASE",
            "efficiency": 0.95,
            "capacity": 500.0,
            "peak_load": 500.0,
        }
    ]
}

rmr_empty = {}

# Testing RuleDefinitionBase #########################

base_rule_1 = RuleDefinitionBase(
    rmr_context="transformers", rmrs_used=UserBaselineProposedVals(True, True, False)
)

# Testing RuleDefinitionBase get_context method ------------------
def test__rule_definition_base_get_context__with_missing_rmrs():
    assert (
        base_rule_1.get_context(UserBaselineProposedVals(rmr_1, rmr_empty, rmr_2))
        == "MISSING_BASELINE"
    )
    assert (
        base_rule_1.get_context(UserBaselineProposedVals(rmr_empty, rmr_1, rmr_2))
        == "MISSING_USER"
    )
    assert (
        base_rule_1.get_context(UserBaselineProposedVals(rmr_empty, rmr_empty, rmr_2))
        == "MISSING_USER_BASELINE"
    )


def test__rule_definition_base_get_context__with_rmrs_present():
    context = base_rule_1.get_context(UserBaselineProposedVals(rmr_1, rmr_2, rmr_empty))
    assert (
        context.user == rmr_1["transformers"]
        and context.baseline == rmr_2["transformers"]
        and context.proposed == None
    )
