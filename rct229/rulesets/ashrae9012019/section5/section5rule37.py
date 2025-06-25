from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import PROPOSED
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

TARGET_AIR_LEAKAGE_COEFF = 0.6 * ureg("cfm / foot**2")
TOTAL_AIR_LEAKAGE_COEFF = 0.112

MANUAL_CHECK_MSG = "The building total air leakage rate is not equal to the required proposed design air leakage rate at 75Pa with a Conversion Factor of 0.112 as per section G3.1.1.4. and Measured air leakage rate is not entered for all conditioned and semi-heated zones. Verify the proposed air leakage rate is modeled correctly."


class PRM9012019Rule67a77(RuleDefinitionListIndexedBase):
    """Rule 37 of ASHRAE 90.1-2019 Appendix G Section 5 (Envelope)"""

    def __init__(self):
        super(PRM9012019Rule67a77, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=False, PROPOSED=True
            ),
            required_fields={
                "$.ruleset_model_descriptions[*]": ["weather"],
                "weather": ["climate_zone"],
            },
            each_rule=PRM9012019Rule67a77.BuildingRule(),
            index_rmd=PROPOSED,
            id="5-37",
            description="The proposed air leakage rate of the building envelope (I75Pa) at a fixed building pressure differential of 0.3 in. of water shall be 0.6 cfm/ft2 for buildings providing verification in accordance with Section 5.9.1.2. The air leakage rate of the building envelope shall be converted to appropriate units for the simulation program using one of the methods in Section G3.1.1.4. Exceptions: When whole-building air leakage testing, in accordance with Section 5.4.3.1.1, is specified during design and completed after construction, the proposed design air leakage rate of the building envelope shall be as measured.",
            ruleset_section_title="Envelope",
            standard_section="Section G3.1-5(b) Building Envelope Modeling Requirements for the Proposed design",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    def create_data(self, context, data=None):
        rpd_p = context.PROPOSED
        climate_zone = rpd_p["ruleset_model_descriptions"][0]["weather"]["climate_zone"]
        constructions = rpd_p["ruleset_model_descriptions"][0].get("constructions", {})
        return {
            "climate_zone": climate_zone,
            "constructions": constructions,
        }

    class BuildingRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule67a77.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=False, PROPOSED=True
                ),
                required_fields={"$..zones[*]": ["surfaces"]},
                precision={
                    "building_total_air_leakage_rate_b": {
                        "precision": 1,
                        "unit": "cfm",
                    }
                },
                manual_check_required_msg=MANUAL_CHECK_MSG,
            )

        def get_calc_vals(self, context, data=None):
            building_p = context.PROPOSED

            scc_dict_p = get_surface_conditioning_category_dict(
                data["climate_zone"], building_p, data["constructions"]
            )
            zcc_dict_p = get_zone_conditioning_category_dict(
                data["climate_zone"], building_p, data["constructions"]
            )

            building_total_air_leakage_rate = ZERO.FLOW
            building_total_measured_air_leakage_rate = ZERO.FLOW
            empty_measured_air_leakage_rate_flow_flag = False

            building_total_envelope_area = sum(
                [
                    getattr_(surface, "surface", "area")
                    for surface in find_all("$..surfaces[*]", building_p)
                    if scc_dict_p[surface["id"]] != SCC.UNREGULATED
                ],
                ZERO.AREA,
            )

            for zone in find_all("$..zones[*]", building_p):
                if zcc_dict_p[zone["id"]] in [
                    ZCC.CONDITIONED_RESIDENTIAL,
                    ZCC.CONDITIONED_NON_RESIDENTIAL,
                    ZCC.CONDITIONED_MIXED,
                    ZCC.SEMI_HEATED,
                ]:
                    building_total_air_leakage_rate += getattr_(
                        zone["infiltration"], "infiltration", "flow_rate"
                    )

                measured_air_leakage_rate = zone["infiltration"].get(
                    "measured_air_leakage_rate"
                )
                if measured_air_leakage_rate:
                    building_total_measured_air_leakage_rate += (
                        measured_air_leakage_rate
                    )
                else:
                    empty_measured_air_leakage_rate_flow_flag = True

            target_air_leakage_rate_75pa_p = (
                TARGET_AIR_LEAKAGE_COEFF
            ) * building_total_envelope_area

            return {
                "building_total_air_leakage_rate": CalcQ(
                    "air_flow_rate", building_total_air_leakage_rate
                ),
                "building_total_measured_air_leakage_rate": CalcQ(
                    "air_flow_rate", building_total_measured_air_leakage_rate
                ),
                "target_air_leakage_rate_75pa_p": CalcQ(
                    "air_flow_rate", target_air_leakage_rate_75pa_p
                ),
                "empty_measured_air_leakage_rate_flow_flag": empty_measured_air_leakage_rate_flow_flag,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            building_total_air_leakage_rate = calc_vals[
                "building_total_air_leakage_rate"
            ]
            target_air_leakage_rate_75pa_p = calc_vals["target_air_leakage_rate_75pa_p"]
            empty_measured_air_leakage_rate_flow_flag = calc_vals[
                "empty_measured_air_leakage_rate_flow_flag"
            ]

            return (
                not self.precision_comparison["building_total_air_leakage_rate_b"](
                    building_total_air_leakage_rate,
                    TOTAL_AIR_LEAKAGE_COEFF * target_air_leakage_rate_75pa_p,
                )
                and empty_measured_air_leakage_rate_flow_flag
            )

        def rule_check(self, context, calc_vals=None, data=None):
            building_total_air_leakage_rate = calc_vals[
                "building_total_air_leakage_rate"
            ]
            building_total_measured_air_leakage_rate = calc_vals[
                "building_total_measured_air_leakage_rate"
            ]
            target_air_leakage_rate_75pa_p = calc_vals["target_air_leakage_rate_75pa_p"]
            empty_measured_air_leakage_rate_flow_flag = calc_vals[
                "empty_measured_air_leakage_rate_flow_flag"
            ]

            return self.precision_comparison["building_total_air_leakage_rate_b"](
                building_total_air_leakage_rate,
                TOTAL_AIR_LEAKAGE_COEFF * target_air_leakage_rate_75pa_p,
            ) or (
                not empty_measured_air_leakage_rate_flow_flag
                and self.precision_comparison["building_total_air_leakage_rate_b"](
                    building_total_air_leakage_rate,
                    TOTAL_AIR_LEAKAGE_COEFF * building_total_measured_air_leakage_rate,
                )
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            building_total_air_leakage_rate = calc_vals[
                "building_total_air_leakage_rate"
            ]
            building_total_measured_air_leakage_rate = calc_vals[
                "building_total_measured_air_leakage_rate"
            ]
            target_air_leakage_rate_75pa_p = calc_vals["target_air_leakage_rate_75pa_p"]
            empty_measured_air_leakage_rate_flow_flag = calc_vals[
                "empty_measured_air_leakage_rate_flow_flag"
            ]

            return std_equal(
                TOTAL_AIR_LEAKAGE_COEFF * target_air_leakage_rate_75pa_p,
                building_total_air_leakage_rate,
            ) or (
                not std_equal(
                    building_total_air_leakage_rate,
                    TOTAL_AIR_LEAKAGE_COEFF * target_air_leakage_rate_75pa_p,
                )
                and not empty_measured_air_leakage_rate_flow_flag
                and std_equal(
                    TOTAL_AIR_LEAKAGE_COEFF * building_total_measured_air_leakage_rate,
                    building_total_air_leakage_rate,
                )
            )
