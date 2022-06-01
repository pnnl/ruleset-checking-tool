from rct229.rule_engine.rule_base import RuleDefinitionListIndexedBase, RuleDefinitionBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.ruleset_functions.get_surface_conditioning_category_dict import (get_surface_conditioning_category_dict, SurfaceConditioningCategory as SCC)
from rct229.ruleset_functions.get_zone_conditioning_category_dict import (get_zone_conditioning_category_dict, ZoneConditioningCategory as ZCC)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.std_comparisons import std_equal

TARGET_AIR_LEAKAGE_COEFF = 1.0 * ureg("cfm / foot**2")
TOTAL_AIR_LEAKAGE_COEFF = 0.112


class Section5Rule47(RuleDefinitionListIndexedBase):
    """Rule 47 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule47, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, False),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule47.BuildingRule(),
            index_rmr="baseline",
            id="5-47",
            description="The baseline air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 1 cfm/ft2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4.",
            list_path="ruleset_model_instances[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rmr_proposed = context.proposed
        return {"climate_zone": rmr_proposed["weather"]["climate_zone"]}

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule47.BuildingRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                required_fields={"$..zones[*]": ["surfaces"]},
            )

        def get_calc_vals(self, context, data=None):
            building_p = context.proposed

            scc_dict_p = get_surface_conditioning_category_dict(
                data["climate_zone"], building_p
            )
            zcc_dict_p = get_zone_conditioning_category_dict(
                data["climate_zone"], building_p
            )

            building_total_air_leakage_rate = ZERO.FLOW

            building_total_envelope_area = sum(
                [
                    getattr_(surface, "surface", "area")
                    for surface in find_all("$..surfaces[*]", building_p)
                    if scc_dict_p[surface["id"]] != SCC.UNREGULATED
                ],
                ZERO.AREA,
            )

            target_air_leakage_rate_75pa_p = (
                TARGET_AIR_LEAKAGE_COEFF
            ) * building_total_envelope_area

            for zone in find_all("$..zones[*]", building_p):
                if zcc_dict_p[zone["id"]] in [
                    ZCC.CONDITIONED_RESIDENTIAL,
                    ZCC.CONDITIONED_NON_RESIDENTIAL,
                    ZCC.CONDITIONED_MIXED,
                    ZCC.SEMI_HEATED,
                ]:
                    building_total_air_leakage_rate += getattr_(
                        zone["infiltration"], "infiltration", "infiltration_flow_rate"
                    )

            return {
                "building_total_air_leakage_rate": building_total_air_leakage_rate,
                "target_air_leakage_rate_75pa_b": target_air_leakage_rate_75pa_p,
            }

        def rule_check(self, context, calc_vals=None, data=None):
            building_total_air_leakage_rate = calc_vals["building_total_air_leakage_rate"]
            target_air_leakage_rate_75pa_b = calc_vals["target_air_leakage_rate_75pa_b"]
            return std_equal(target_air_leakage_rate_75pa_b * TOTAL_AIR_LEAKAGE_COEFF, building_total_air_leakage_rate)