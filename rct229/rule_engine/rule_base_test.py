import pytest

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rule_engine.rulesets import RuleSet

# Constants ###############################################
# Note: It is important that these constants are not mutated by any of the tests
# so that the tests can run independently and in any order.
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore

RMR_1 = {
    "transformers": [
        {
            "id": 1,
            "name": "Transformer 1",
            "type": "DRY_TYPE",
            "phase": "SINGLE_PHASE",
            "efficiency": 0.9,
            "capacity": 500.0,
            "peak_load": 500.0,
        },
        {
            "id": 2,
            "name": "Transformer 2",
            "type": "DRY_TYPE",
            "phase": "SINGLE_PHASE",
            "efficiency": 0.9,
            "capacity": 500.0,
            "peak_load": 500.0,
        },
    ]
}


RMR_2 = {
    "transformers": [
        {
            "id": 1,
            "name": "Transformer 1",
            "type": "DRY_TYPE",
            "phase": "SINGLE_PHASE",
            "efficiency": 0.95,
            "capacity": 500.0,
            "peak_load": 500.0,
        }
    ]
}


RMR_EMPTY = {}

SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
SchemaEnums.update_schema_enum()

DERIVED_RULE_OUTCOME_BASE = produce_ruleset_model_instance(
    USER=RMR_1, BASELINE_0=RMR_EMPTY, PROPOSED=RMR_2
)


RMRS_WITH_MATCHING_USER_AND_BASELINE = produce_ruleset_model_instance(
    USER=RMR_1, BASELINE_0=RMR_1, PROPOSED=RMR_EMPTY
)


BASE_RULE_1_OUTCOME_BASE = {
    "id": "1",
    "description": "Basic Rule",
    "rmr_context": "/transformers",
}


BASE_RULE_ARGS = {
    **BASE_RULE_1_OUTCOME_BASE,
    "not_applicable_msg": "Not applicable message",
    "manual_check_required_msg": "Manual check required message",
    "rmrs_used": produce_ruleset_model_instance(
        USER=True, BASELINE_0=True, PROPOSED=False
    ),
}


BASE_RULE_1 = RuleDefinitionBase(**BASE_RULE_ARGS)


class _DerivedRule(RuleDefinitionBase):
    """Rule with is_applicable() always returning False"""

    def __init__(self, data=None):
        super(_DerivedRule, self).__init__(**BASE_RULE_ARGS)

    def is_applicable(self, context, data=None):
        return data != "NA"

    def get_calc_vals(self, context, data=None):
        return [{"a": 0}, 1]

    def manual_check_required(self, context, calc_vals=None, data=None):
        return data == "MANUAL_CHECK_REQUIRED"

    def rule_check(self, context, calc_vals=None, data=None):
        return type(data) is bool and data


DERIVED_RULE = _DerivedRule()

DERIVED_RULE_outcome_base = {**BASE_RULE_1_OUTCOME_BASE, "calc_vals": [{"a": 0}, 1]}

# Tests ###################################################


# Testing RuleDefinitionBase evalute method ------------------
def test__rule_definition_base__evaluate__with_missing_baseline():
    assert BASE_RULE_1.evaluate(DERIVED_RULE_OUTCOME_BASE) == {
        **BASE_RULE_1_OUTCOME_BASE,
        "result": "UNDETERMINED",
        "message": "MISSING_BASELINE_0",
    }


def test__rule_definition_base__evaluate__with_false_is_applicable():
    assert DERIVED_RULE.evaluate(RMRS_WITH_MATCHING_USER_AND_BASELINE, data="NA") == {
        **BASE_RULE_1_OUTCOME_BASE,
        "result": "NOT_APPLICABLE",
        "message": "Not applicable message",
    }


def test__rule_definition_base__evaluate__with_true_manual_check_required():
    assert DERIVED_RULE.evaluate(
        RMRS_WITH_MATCHING_USER_AND_BASELINE, data="MANUAL_CHECK_REQUIRED"
    ) == {
        **DERIVED_RULE_outcome_base,
        "result": "UNDETERMINED",
        "message": "Manual check required message",
    }


def test__rule_definition_base__evaluate__with_true_rule_check():
    assert DERIVED_RULE.evaluate(RMRS_WITH_MATCHING_USER_AND_BASELINE, data=True) == {
        **DERIVED_RULE_outcome_base,
        "result": "PASSED",
    }


def test__rule_definition_base__evaluate__with_true_rule_check():
    assert DERIVED_RULE.evaluate(RMRS_WITH_MATCHING_USER_AND_BASELINE, data=False) == {
        **DERIVED_RULE_outcome_base,
        "result": "FAILED",
    }


# Testing RuleDefinitionBase get_context method ------------------
def test__rule_definition_base__get_context__with_missing_rmrs():
    assert (
        BASE_RULE_1.get_context(
            produce_ruleset_model_instance(
                USER=RMR_1, BASELINE_0=RMR_EMPTY, PROPOSED=RMR_2
            )
        )
        == "MISSING_BASELINE_0"
    )
    assert (
        BASE_RULE_1.get_context(
            produce_ruleset_model_instance(
                USER=RMR_EMPTY, BASELINE_0=RMR_1, PROPOSED=RMR_2
            )
        )
        == "MISSING_USER"
    )
    assert (
        BASE_RULE_1.get_context(
            produce_ruleset_model_instance(
                USER=RMR_EMPTY, BASELINE_0=RMR_EMPTY, PROPOSED=RMR_2
            )
        )
        == "MISSING_USER_BASELINE_0"
    )


def test__rule_definition_base__get_context__with_rmrs_present():
    context = BASE_RULE_1.get_context(
        produce_ruleset_model_instance(USER=RMR_1, BASELINE_0=RMR_2, PROPOSED=RMR_EMPTY)
    )
    assert (
        context.USER == RMR_1["transformers"]
        and context.BASELINE_0 == RMR_2["transformers"]
        and context.PROPOSED == None
    )


# Testing RuleDefinitionBase _missing_fields_str method ------------
def test___missing_fields_str__with_no_missing_fields():
    assert (
        BASE_RULE_1._missing_fields_str(
            jpath="foo",
            required_fields=["one", "two"],
            single_context={"foo": {"id": 0, "one": 1, "two": 2}},
        )
    ) == ""


def test___missing_fields_str__with_missing_fields():
    assert (
        BASE_RULE_1._missing_fields_str(
            jpath="foo",
            required_fields=["one", "three", "four"],
            single_context={"foo": {"id": 0, "one": 1, "two": 2}},
        )
    ) == "id:0 missing:three,four"


# Testing RuleDefinitionBase is_applicable method ------------------
def test__rule_definition_base__is_applicable():
    # The default implementation always returns True
    assert BASE_RULE_1.is_applicable({}) == True


# Testing RuleDefinitionBase get_calc_vals method ------------------
def test__rule_definition_base__get_calc_vals():
    # The default implementation always returns None
    assert BASE_RULE_1.get_calc_vals({}) == None


# Testing RuleDefinitionBase manual_check_required method ------------------
def test__rule_definition_base__manual_check_required():
    # The default implementation always returns False
    assert BASE_RULE_1.manual_check_required({}) == False


# Testing RuleDefinitionBase manual_check_required method ------------------
def test__rule_definition_base__rule_check():
    # The default implementation always returns False
    with pytest.raises(NotImplementedError):
        BASE_RULE_1.rule_check({})
