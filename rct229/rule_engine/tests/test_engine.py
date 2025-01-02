import inspect

import rct229.rulesets as ruleset
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rulesets import RuleSet
from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.schema_store import SchemaStore

SchemaStore.set_ruleset(RuleSet.ASHRAE9012019_RULESET)
SchemaEnums.update_schema_enum()


def test___get_rules___returns_rules():
    available_rules = [rule_tuple[1] for rule_tuple in ruleset.__getrules__()]
    assert all(
        [
            issubclass(available_rule, RuleDefinitionBase)
            for available_rule in available_rules
        ]
    )
