import inspect

import rct229.rulesets as ruleset
from rct229.rule_engine.rule_base import RuleDefinitionBase


def test___get_rules___returns_rules():
    available_rules = [rule_tuple[1] for rule_tuple in ruleset.__getrules__("ashare9012019")]
    assert all(
        [
            issubclass(available_rule, RuleDefinitionBase)
            for available_rule in available_rules
        ]
    )
