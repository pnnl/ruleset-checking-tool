from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import (
    get_opaque_surface_type,
    ROOF,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_exactly_by_id

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


class Section5Rule5(RuleDefinitionListIndexedBase):
    """Rule 5 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule3, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule3.BuildingRule(),
            index_rmr="baseline",
            id="5-5",
            description="Baseline roof assemblies must match the appropriate assembly maximum U-factors in Tables G3.4-1 through G3.4-8.",
            list_path="buildings[*]",
        )

        def create_data(context, data=None):
            return {"climate_zone": context.baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section5Rule3.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={},
            )

            def create_context_list(context, data=None):
                context_list = []
                for surface in find_all("$..surfaces[*]"):
                    if get_opaque_surface_type(surface) == ROOF:
                        UserBaselineProposedVals(None, surface, None)

        def get_calc_vals(self, context, data=None):
            surface_conditioning_category_dict = get_surface_conditioning_category_dict(
                data["climate_zone"], context.baseline
            )
            for surface in find_all(EXTERIOR_SURFACES_JSONPATH, context.baseline):
                if surface["does_cast_shade"]:
                    baseline_surfaces_casting_shade_ids.append(surface["id"])

            return {
                "baseline_surfaces_casting_shade_ids": baseline_surfaces_casting_shade_ids
            }

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["baseline_surfaces_casting_shade_ids"]) == 0


# ------------------------
