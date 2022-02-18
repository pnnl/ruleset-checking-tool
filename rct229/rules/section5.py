from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_exactly_by_id
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
# Rule Definitions for Section 5 of 90.1-2019 Appendix G

# ------------------------
# Reusable constants
EXTERIOR_SURFACES_JSONPATH = "$..surfaces[?(@.adjacent_to='EXTERIOR')]"
# ------------------------
class Section5Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule2, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, False, True),
            each_rule=Section5Rule2.BuildingRule(),
            index_rmr="proposed",
            id="5-2",
            description="Orientation is the same in user model and proposed model",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule2.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, False, True),
                required_fields={
                    "$..surfaces[*]": ["azimuth"],
                },
                # TODO: add this to RuleDefinitionBase
                must_match_by_ids=["$..surfaces[*]"],
            )

        def get_calc_vals(self, context, data=None):
            failing_surface_ids = []
            proposed_surfaces = find_all("$..surfaces[*]", context.proposed)
            user_surfaces = find_all("$..surfaces[*]", context.user)

            # This assumes that the surfaces all match
            matched_user_surfaces = match_lists_exactly_by_id(
                proposed_surfaces, user_surfaces
            )
            proposed_user_surface_pairs = zip(proposed_surfaces, matched_user_surfaces)
            for (p_surface, u_surface) in proposed_user_surface_pairs:
                if p_surface["azimuth"] != u_surface["azimuth"]:
                    failing_surface_ids.append(p_surface["id"])

            return {"failing_surface_ids": failing_surface_ids}

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failing_surface_ids"]) == 0


# ------------------------


class Section5Rule3(RuleDefinitionListIndexedBase):
    """Rule 3 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule3.BuildingRule(),
            index_rmr="baseline",
            id="5-3",
            description="The building shall be modeled so that it does not shade itself",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule3.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={
                    "$..surfaces[*]": ["adjacent_to"],
                    EXTERIOR_SURFACES_JSONPATH: ["does_cast_shade"],
                },
            )

        def get_calc_vals(self, context, data=None):
            baseline_surfaces_casting_shade_ids = []
            for surface in find_all(EXTERIOR_SURFACES_JSONPATH, context.baseline):
                if surface["does_cast_shade"]:
                    baseline_surfaces_casting_shade_ids.append(surface["id"])

            return {
                "baseline_surfaces_casting_shade_ids": baseline_surfaces_casting_shade_ids
            }

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["baseline_surfaces_casting_shade_ids"]) == 0


# ------------------------
class Section5Rule28(RuleDefinitionListIndexedBase):
    """Rule 18 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule28, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section5Rule28.BuildingRule(),
            index_rmr="baseline",
            id="5-28",
            description="Subsurface that is not regulated (not part of building envelope) must be modeled with the "
                        "same area, U-factor and SHGC in the baseline as in the proposed design",
            list_path="buildings[*]",
        )

    def create_data(self, context, data=None):
        return {"climate_zone": context.baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule28.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$..surfaces[*]": ["subsurfaces", "adjacent_to"],
                    "$..subsurfaces[*]": ["u-factor", "solar_heat_gain_coefficient", "glazed_area", "opaque_area"]
                },
            )
            self.warning_msg = "Subsurface that is not regulated (not part of building envelope) is not modeled with the same area, U-factor and SHGC in the baseline as in the proposed design"

        def get_calc_vals(self, context, data=None):
            missing_surface_id = []
            failing_subsurface_id = []
            climate_zone = data['climate_zone']
            scc_dictionary_b = get_surface_conditioning_category_dict(climate_zone, context.baseline)
            # Retrieve all surfaces under buildings
            surfaces_b = find_all("$..zones[*].surfaces[*]", context.baseline)
            surfaces_p = find_all("$..zones[*].surfaces[*]", context.proposed)

            surfaces_b_dict = {surface_b["id"]: surface_b for surface_b in surfaces_b}

            for surface_p in surfaces_p:
                surface_b = surfaces_b_dict[surface_p["id"]]

                if surface_b is None:
                    missing_surface_id.append(surface_p["id"])
                    continue

                if scc_dictionary_b[surface_b["id"]] == "UNREGULATED":
                    subsurfaces_b = surface_b["subsurfaces"]
                    subsurfaces_p = surface_p["subsurfaces"]

                    try:
                        matched_subsurfaces = match_lists_exactly_by_id(subsurfaces_b, subsurfaces_p)
                    except:
                        # cannot find exactly match in number of subsurfaces between baseline and proposed
                        return {"error": "Test failed because the number of sub-surfaces for surface id %s "
                                         "does not match between baseline and proposed models" %surface_b["id"]}
                    baseline_subsurfaces_pairs = zip(subsurfaces_b, matched_subsurfaces)
                    for (subsurface_b, subsurface_m) in baseline_subsurfaces_pairs:
                        if subsurface_b["u-factor"] != subsurface_m["u-factor"] or subsurface_b["solar_heat_gain_coefficient"] != subsurface_m["solar_heat_gain_coefficient"] or subsurface_b["glazed_area"] != subsurface_m["glazed_area"] or subsurface_b["opaque_area"] != subsurface_m["opaque_area"]:
                            failing_subsurface_id.append(subsurface_b["id"])

            return {"missing_surface_id": missing_surface_id, "failing_subsurface_id": failing_subsurface_id}

        def rule_check(self, context, calc_vals=None, data=None):
            if "error" in calc_vals:
                return False
            return len(calc_vals["missing_surface_id"] == 0 and calc_vals["failing_subsurface_id"] == 0)





