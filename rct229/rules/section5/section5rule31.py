from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id

MANUAL_CHECK_MSG = "Surface in P-RMR has subsurfaces modeled with different manual shade status. Verify if subsurfaces manual shade status in B-RMR are modeled the same as in P-RMR"


class Section5Rule31(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule31, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section5Rule31.BuildingRule(),
            index_rmr="baseline",
            id="5-31",
            description="Manual fenestration shading devices, such as blinds or shades, shall be modeled or not modeled the same as in the baseline building design.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule31.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                # Make sure surfaces are matched in SurfaceRule
                list_path="$..surfaces[*]",
                each_rule=Section5Rule31.BuildingRule.SurfaceRule(),
                index_rmr="baseline",
            )

        class SurfaceRule(RuleDefinitionListIndexedBase):
            def __init__(self):
                super(Section5Rule31.BuildingRule.SurfaceRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    # Make sure subsurfaces are matched
                    # List_path will be evaluated after manual check
                    each_rule=Section5Rule31.BuildingRule.SurfaceRule.SubsurfaceRule(),
                    index_rmr="baseline",
                    list_path="subsurfaces[*]",
                    manual_check_required_msg=MANUAL_CHECK_MSG,
                )

            def manual_check_required(self, context, calc_vals=None, data=None):
                surface_p = context.proposed
                # raise data error exception if proposed surface has no subsurfaces
                subsurfaces_p = find_all("subsurfaces", surface_p)
                subsurfaces_with_manual_interior_shades_p = find_all(
                    "subsurfaces[?(@.has_manual_interior_shades=True)]", surface_p
                )

                return len(subsurfaces_with_manual_interior_shades_p) != 0 and len(
                    subsurfaces_with_manual_interior_shades_p
                ) != len(subsurfaces_p)

            def create_data(self, context, data=None):
                surface_p = context.proposed
                subsurfaces_with_manual_interior_shades_p = find_all(
                    "subsurfaces[?(@.has_manual_interior_shades=true)]", surface_p
                )
                # None - if no subsurfaces, then the code wont evaluate the subsurface rule
                return {
                    "proposed_subsurface_manual_shade": subsurfaces_with_manual_interior_shades_p[
                        0
                    ][
                        "has_manual_interior_shades"
                    ]
                    if subsurfaces_with_manual_interior_shades_p
                    else None,
                }

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(
                        Section5Rule31.BuildingRule.SurfaceRule.SubsurfaceRule, self
                    ).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                        required_fields={"$": ["has_manual_interior_shades"]},
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.baseline
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
