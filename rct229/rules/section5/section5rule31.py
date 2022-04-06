from rct229.rule_engine.rule_base import RuleDefinitionListIndexedBase, RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.assertions import getattr_, assert_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_by_id


MANUAL_CHECK_MSG = "SURFACE IN P-RMR HAS SUBSURFACES MODELED WITH DIFFERENT MANUAL SHADE STATUS. VERIFY IF SUBSURFACES MANUAL SHADE STATUS IN B-RMR ARE MODELED THE SAME AS IN P-RMR"

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
                list_path="surfaces[*]",
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
                    index_rmr="baseline"
                )

            def is_applicable(self, context, data=None):
                surface_b = context.baseline
                surface_p = context.proposed
                # Both are none, not applicable.
                # The logic indicates either or both surface_b and surface_p have subsurfaces to be applicable
                # But XOR could fails the test (b != p) - the equality is not checked in this rule
                # b != p will be captured by data error exception in this test.
                return (surface_b.get("subsurfaces") is None) and (surface_p.get("subsurfaces") is None)

            def manual_check_required(self, context, calc_vals=None, data=None):
                surface_p = context.proposed
                # raise data error exception if proposed surface has no subsurfaces
                subsurfaces_p = assert_(surface_p.get("subsurfaces"), f"No subsurfaces found in the proposed surface {surface_p['id']}")
                num_shades = 0
                for subsurface in subsurfaces_p:
                    # raise missing key exception if the subsurface has no has_manual_interior_shades
                    if getattr_(subsurface, "subsurface", "has_manual_interior_shades"):
                        num_shades += 1

                data = {"manual_check": num_shades != 0 and num_shades != len(subsurfaces_p)}
                data["message"] = MANUAL_CHECK_MSG if data["manual_check"] else ""
                return data["manual_check"]

            def create_data(self, context, data=None):
                # context.proposed must have subsurfaces when running this function
                surface_p = context.proposed
                subsurface_p = context.proposed["subsurfaces"][0]
                # Raise missing key exception if the subsurface has no has_manual_interior_shades key
                return {**data, "proposed_subsurface_manual_shade": getattr_(subsurface_p, "subsurface", "has_manual_interior_shades")}

            def create_context_list(self, context, data=None):
                surface_b = context.baseline
                # raise data error exception if baseline surface has no subsurfaces.
                subsurfaces_b = assert_(surface_b.get("subsurfaces"), f"No subsurfaces found in the baseline surface {surface_b['id']}")
                return [
                    UserBaselineProposedVals(None, subsurface_b, None)
                    for subsurface_b in subsurfaces_b
                ]

            class SubsurfaceRule(RuleDefinitionBase):
                def __init__(self):
                    super(Section5Rule31.BuildingRule.SurfaceRule.SubsurfaceRule, self).__init__(
                        rmrs_used=UserBaselineProposedVals(False, True, False),
                        required_fields={
                            "$": ["has_manual_interior_shades"]
                        }
                    )

                def get_calc_vals(self, context, data=None):
                    subsurface_b = context.baseline
                    return {
                        "subsurface_p_manual_shade": data["proposed_subsurface_manual_shade"],
                        "subsurface_b_manual_shade": subsurface_b["has_manual_interior_shades"]
                    }

                def rule_check(self, context, calc_vals=None, data=None):
                    return calc_vals["subsurface_p_manual_shade"] == calc_vals["subsurface_b_manual_shade"]












