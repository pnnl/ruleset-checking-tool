from rct229.data.schema_enums import schema_enums
from rct229.data_fns.table_G3_4_fns import table_G34_lookup
from rct229.rule_engine.rule_base import (
    RuleDefinitionBase,
    RuleDefinitionListIndexedBase,
)
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_opaque_surface_type import (
    BELOW_GRADE_WALL,
    get_opaque_surface_type,
)
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.match_lists import match_lists_exactly_by_id
from rct229.schema.config import ureg

# Rule Definitions for Section 5 of 90.1-2019 Appendix G
CONSTANT = schema_enums["InfiltrationMethodType"].CONSTANT.name

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

class Section5Rule8(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule8, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule8.BuildingRule(),
            index_rmr="baseline",
            list_path="buildings[*]",
            id="5-8",
            description="Baseline below-grade walls shall match the appropriate assembly maximum C-factors in Table G3.4-1 through G3.4-8.",
        )

    def create_data(self, context, data=None):
        return {"climate_zone": context.baseline["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule8.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={"$..zones[*]": ["surfaces"]},
            )

        def get_calc_vals(self, context, data=None):
            # Climate zone should have only one in RMR
            climate_zone = data["climate_zone"]
            # Becasue list_path is building, the scope of the context.baseline here is building
            scc_dictionary_b = get_surface_conditioning_category_dict(
                climate_zone, context.baseline
            )
            # Retrieve all surfaces under the building
            surfaces_b = find_all("$..zones[*].surfaces[*]", context.baseline)
            # build-in manual check flag.
            calc_val = {}
            failing_surface_c_factor_ids = []
            mix_surface_c_factor_ids = []

            for surface_b in surfaces_b:
                if get_opaque_surface_type(surface_b) == BELOW_GRADE_WALL:
                    # construction info
                    surface_construction_b = surface_b["construction"]
                    scc_b = scc_dictionary_b[surface_b["id"]]
                    # QNS a good number to estimate?
                    target_c_factor = None
                    # TODO All these need to change to enum later
                    if scc_b in [
                        "EXTERIOR RESIDENTIAL",
                        "EXTERIOR NON-RESIDENTIAL",
                        "SEMI-EXTERIOR",
                    ]:
                        target = table_G34_lookup(climate_zone, scc_b, BELOW_GRADE_WALL)
                        target_c_factor = target["c_factor"]

                    elif scc_b == "EXTERIOR MIXED":
                        target = table_G34_lookup(
                            climate_zone, "EXTERIOR RESIDENTIAL", BELOW_GRADE_WALL
                        )
                        target_c_factor_res = target["c_factor"]

                        target = table_G34_lookup(
                            climate_zone, "EXTERIOR NON-RESIDENTIAL", BELOW_GRADE_WALL
                        )
                        target_c_factor_nonres = target["c_factor"]

                        if target_c_factor_res != target_c_factor_nonres:
                            mix_surface_c_factor_ids.append(surface_b["id"])
                        else:
                            target_c_factor = target_c_factor_res
                    # convert values to IP unit to compare with standard.
                    model_c_factor_magnitude = round(
                        surface_construction_b["c_factor"]
                        .to("Btu_h / square_foot / delta_degF")
                        .magnitude,
                        2,
                    )
                    target_c_factor_magnitude = target_c_factor.magnitude
                    if model_c_factor_magnitude != target_c_factor_magnitude:
                        failing_surface_c_factor_ids.append(surface_b["id"])

            return {
                "failed_c_factor_surface_id": failing_surface_c_factor_ids,
                "mix_surface_c_factor_ids": mix_surface_c_factor_ids,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            """
            Return True or False if the results shall depends on manual check
            Parameters
            ----------
            context
            calc_vals
            data

            Returns
            -------
            """
            return len(calc_vals["mix_surface_c_factor_ids"]) > 0

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failed_c_factor_surface_id"]) == 0


# ------------------------

class Section5Rule44(RuleDefinitionListIndexedBase):
    """Rule 44 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule44, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            each_rule=Section5Rule44.BuildingRule(),
            index_rmr="baseline",
            id="5-44",
            description="The infiltration modeling method in the baseline includes adjustment for weather and building operation.",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule44.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, False),
                required_fields={"$..infiltration": ["modeling_method"]},
            )

        def get_calc_vals(self, context, data=None):
            baseline_infiltration = find_all("$..infiltration", context.baseline)
            failing_infiltration_ids = [
                b_infiltration["id"]
                for b_infiltration in baseline_infiltration
                if b_infiltration["modeling_method"] != CONSTANT
            ]
            return {"failing_infiltration_ids": failing_infiltration_ids}

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["failing_infiltration_ids"]) == 0


# ------------------------


class Section5Rule46(RuleDefinitionListIndexedBase):
    """Rule 44 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule46, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            each_rule=Section5Rule46.BuildingRule(),
            index_rmr="proposed",
            id="5-46",
            description="The infiltration shall be modeled using the same methodology and adjustments for weather and building operation in both the proposed design and the baseline building design.",
            rmr_context="buildings",
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule46.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                required_fields={
                    "$..infiltration": ["algorithm_name", "modeling_method"]
                },
            )

        def get_calc_vals(self, context, data=None):
            infiltration_fail_id = []
            missing_zone_id = []
            baseline_zones = find_all("$..zones[*]", context.baseline)
            proposed_zones = find_all("$..zones[*]", context.proposed)

            b_zone_dict = {b_zone["id"]: b_zone for b_zone in baseline_zones}

            for p_zone in proposed_zones:
                # Get matching baseline zone
                b_zone = b_zone_dict.get(p_zone["id"])

                if b_zone is None:
                    missing_zone_id.append(p_zone["id"])
                    # skip the infiltration check
                    continue
                p_zone_infiltration = p_zone["infiltration"]
                # b_zone could be NONE - add a check.
                b_zone_infiltration = b_zone["infiltration"]

                if (
                    p_zone_infiltration["algorithm_name"]
                    != b_zone_infiltration["algorithm_name"]
                    or p_zone_infiltration["modeling_method"]
                    != b_zone_infiltration["modeling_method"]
                ):
                    infiltration_fail_id.append(p_zone["id"])

            return {
              "infiltration_fail_id": infiltration_fail_id,
              "missing_zone_id": missing_zone_id,
            }

        def rule_check(self, context, calc_vals, data=None):
            return len(calc_vals["infiltration_fail_id"]) == 0 and len(
                calc_vals["missing_zone_id"] == 0
            )
