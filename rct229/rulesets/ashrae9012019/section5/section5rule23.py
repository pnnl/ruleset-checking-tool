from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0


class PRM9012019Rule11q41(RuleDefinitionListIndexedBase):
    """Rule 23 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule11q41, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule11q41.BuildingRule(),
            index_rmd=BASELINE_0,
            id="5-23",
            description="Manual fenestration shading devices, such as blinds or shades, shall be modeled or not modeled the same as in the baseline building design.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(a)(4) Building Modeling Requirements for the Proposed design and G3.1-5(d) Building Modeling Requirements for Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule11q41.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                list_path="$.building_segments[*].zones[*].surfaces[*].subsurfaces[*]",
                each_rule=PRM9012019Rule11q41.BuildingRule.SubsurfaceRule(),
                index_rmd=BASELINE_0,
            )

        class SubsurfaceRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule11q41.BuildingRule.SubsurfaceRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={"$": ["has_manual_interior_shades"]},
                )

            def get_calc_vals(self, context, data=None):
                subsurface_b = context.BASELINE_0
                subsurface_p = context.PROPOSED
                return {
                    "subsurface_p_manual_shade": subsurface_p[
                        "has_manual_interior_shades"
                    ],
                    "subsurface_b_manual_shade": subsurface_b[
                        "has_manual_interior_shades"
                    ],
                }

            def rule_check(self, context, calc_vals=None, data=None):
                return (
                    calc_vals["subsurface_p_manual_shade"]
                    == calc_vals["subsurface_b_manual_shade"]
                )
