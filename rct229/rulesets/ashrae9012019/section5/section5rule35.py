from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    SurfaceConditioningCategory as SCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_surface_conditioning_category_dict import (
    get_surface_conditioning_category_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    ZoneConditioningCategory as ZCC,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_zone_conditioning_category_dict import (
    get_zone_conditioning_category_dict,
)
from rct229.schema.config import ureg
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.std_comparisons import std_equal

TARGET_AIR_LEAKAGE_COEFF = 1.0 * ureg("cfm / foot**2")
TOTAL_AIR_LEAKAGE_FACTOR = 0.112


class Section5Rule35(RuleDefinitionListIndexedBase):
    """Rule 35 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(Section5Rule35, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            required_fields={
                "$": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=Section5Rule35.BuildingRule(),
            index_rmr=BASELINE_0,
            id="5-35",
            description="The baseline air leakage rate of the building envelope (I_75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 1 cfm/ft2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(h) Building Envelope Modeling Requirements for the Baseline building",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
            data_items={"climate_zone": (BASELINE_0, "weather/climate_zone")},
        )

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(Section5Rule35.BuildingRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={"$.building_segments[*].zones[*]": ["surfaces"]},
            )

        def get_calc_vals(self, context, data=None):
            building_b = context.BASELINE_0

            scc_dict_b = get_surface_conditioning_category_dict(
                data["climate_zone"], building_b
            )
            zcc_dict_b = get_zone_conditioning_category_dict(
                data["climate_zone"], building_b
            )

            building_total_air_leakage_rate = ZERO.FLOW

            building_total_envelope_area = sum(
                [
                    getattr_(surface, "surface", "area")
                    for surface in find_all(
                        "$.building_segments[*].zones[*].surfaces[*]", building_b
                    )
                    if scc_dict_b[surface["id"]] != SCC.UNREGULATED
                ],
                ZERO.AREA,
            )

            target_air_leakage_rate_75pa_b = (
                TARGET_AIR_LEAKAGE_COEFF
            ) * building_total_envelope_area

            for zone in find_all("$.building_segments[*].zones[*]", building_b):
                if zcc_dict_b[zone["id"]] in [
                    ZCC.CONDITIONED_RESIDENTIAL,
                    ZCC.CONDITIONED_NON_RESIDENTIAL,
                    ZCC.CONDITIONED_MIXED,
                    ZCC.SEMI_HEATED,
                ]:
                    building_total_air_leakage_rate += getattr_(
                        zone["infiltration"], "infiltration", "flow_rate"
                    )

            return {
                "building_total_air_leakage_rate": CalcQ(
                    "volumetric_flow_rate", building_total_air_leakage_rate
                ),
                "target_air_leakage_rate_75pa_b": CalcQ(
                    "volumetric_flow_rate", target_air_leakage_rate_75pa_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            building_total_air_leakage_rate = calc_vals[
                "building_total_air_leakage_rate"
            ]
            target_air_leakage_rate_75pa_b = calc_vals["target_air_leakage_rate_75pa_b"]
            return std_equal(
                target_air_leakage_rate_75pa_b * TOTAL_AIR_LEAKAGE_FACTOR,
                building_total_air_leakage_rate,
            )
