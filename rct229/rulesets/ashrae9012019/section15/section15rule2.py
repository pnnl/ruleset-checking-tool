from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description


class Section15Rule2(RuleDefinitionBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(Section15Rule2, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            id="15-2",
            description="Number of transformers modeled in User RMD and Proposed RMD are the same",
            ruleset_section_title="Transformer",
            standard_section="Transformers",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0/transformers",
        )

    def is_applicable(self, context, data=None):
        return len(context.USER) > 0

    def get_calc_vals(self, context, data=None):
        return {
            "num_user_transformers": len(context.USER),
            "num_proposed_transformers": len(context.PROPOSED),
        }

    def rule_check(self, context, calc_vals=None, data=None):
        return (
            calc_vals["num_user_transformers"] == calc_vals["num_proposed_transformers"]
        )
