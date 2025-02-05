from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.std_comparisons import std_equal

MANUAL_CHECK_MSG = "Surface in P-RMD has subsurfaces modeled with different manual shade status. Verify if subsurfaces manual shade status in B-RMD are modeled the same as in P-RMD"
MANUALLY_SHADED_SUBSURFACES_JSON = (
    "$.subsurfaces[*][?(@.has_manual_interior_shades=true)]"
)


class PRM9012019Rule11q41(RuleDefinitionListIndexedBase):
    """Rule 23 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule11q41, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule11q41.BuildingRule(),
            index_rmd=BASELINE_0,
            id="section5rule23",
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
                list_path="$.building_segments[*].zones[*].surfaces[*]",
                each_rule=PRM9012019Rule11q41.BuildingRule.SurfaceRule(),
                index_rmd=BASELINE_0,
            )

        class SurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(PRM9012019Rule11q41.BuildingRule.SurfaceRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    each_rule=PRM9012019Rule11q41.BuildingRule.SurfaceRule.SubsurfaceRule(),
                    index_rmd=BASELINE_0,
                    list_path="subsurfaces[*]",
                    manual_check_required_msg=MANUAL_CHECK_MSG,
                )

            def manual_check_required(self, context, calc_vals=None, data=None):
                surface_p = context.PROPOSED
                subsurfaces_p = find_all("$.subsurfaces[*]", surface_p)
                subsurfaces_with_manual_interior_shades_p = find_all(
                    MANUALLY_SHADED_SUBSURFACES_JSON, surface_p
                )
                return len(subsurfaces_with_manual_interior_shades_p) != 0 and len(
                    subsurfaces_with_manual_interior_shades_p
                ) != len(subsurfaces_p)

            def create_data(self, context, data=None):
                surface_p = context.PROPOSED
                subsurfaces_with_manual_interior_shades_p = find_all(
                    MANUALLY_SHADED_SUBSURFACES_JSON, surface_p
                )
                return {
                    "proposed_subsurface_manual_shade": subsurfaces_with_manual_interior_shades_p[
                        0
                    ][
                        "has_manual_interior_shades"
                    ]
                    if subsurfaces_with_manual_interior_shades_p
                    else None
                }

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        PRM9012019Rule11q41.BuildingRule.SurfaceRule.SubsurfaceRule,
                        self,
                    ).__init__(
                        rmds_used=produce_ruleset_model_description(
                            USER=False, BASELINE_0=True, PROPOSED=True
                        ),
                        required_fields={"$": ["has_manual_interior_shades"]},
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.BASELINE_0
                    return {
                        "subsurface_p_manual_shade": data[
                            "proposed_subsurface_manual_shade"
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
