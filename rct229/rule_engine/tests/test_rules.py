from rct229.rule_engine.rule_base import RuleDefinitionBase


class MyRuleDefinition(RuleDefinitionBase):
    def __init__(self, user_rmr, baseline_rmr, proposed_rmr):
        self.id = "15-1"
        self.description = "My description"
        self.rmd_context = "transformers"
        super(MyRuleDefinition, self).__init__(user_rmr, baseline_rmr, proposed_rmr)

    def check_applicability(self):
        return True

    def check_manual_check_required(self):
        pass

    def rule_evaluation(self):
        return True


def test_create_rule_definition_class():
    # test to check the number of available rules
    assert issubclass(MyRuleDefinition, RuleDefinitionBase)
