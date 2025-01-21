from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import USER
from rct229.utils.jsonpath_utils import find_all


class PRM9012019Rule87p01(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 15 (Transformers)."""

    def __init__(self):
        super(PRM9012019Rule87p01, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=False, PROPOSED=True
            ),
            each_rule=PRM9012019Rule87p01.TransformerRule(),
            index_rmd=USER,
            id="15-3",
            description="User RMD transformer id in Proposed RMD",
            ruleset_section_title="Transformer",
            standard_section="Transformers",
            is_primary_rule=False,
            rmd_context="ruleset_model_descriptions/0/transformers",
        )

    def create_data(self, context, data):
        transformers_p = context.PROPOSED
        return {"transformer_ids_p": find_all("$[*].id", transformers_p)}

    class TransformerRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule87p01.TransformerRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=True, BASELINE_0=False, PROPOSED=False
                ),
            )

        def get_calc_vals(self, context, data=None):
            return {
                "user_transformer_id": context.USER["id"],
                "transformer_ids_p": data["transformer_ids_p"],
            }

        def rule_check(self, context, calc_vals=None, data=None):
            return calc_vals["user_transformer_id"] in calc_vals["transformer_ids_p"]
