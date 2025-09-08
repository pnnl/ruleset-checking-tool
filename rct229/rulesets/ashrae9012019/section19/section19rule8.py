from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.compare_standard_val import std_ge
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ

MIN_OA_CFM = 3000 * ureg("cfm")
OCCUPANT_DENSITY_LIMIT = 0.1 * ureg("people/ft2")
DEMAND_CONTROL_VENTILATION_CONTROL = SchemaEnums.schema_enums[
    "DemandControlVentilationControlOptions"
]


class PRM9012019Rule02h13(RuleDefinitionListIndexedBase):
    """Rule 8 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule02h13, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule02h13.BuildingRule(),
            index_rmd=BASELINE_0,
            id="19-8",
            description="Demand control ventilation is modeled in the baseline design in systems with outdoor air capacity greater than 3000 cfm serving areas with an average occupant design capacity greater than 100 people per 1000 ft^2.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.5 Exception #1",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0].buildings[*]",
        )

    class BuildingRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule02h13.BuildingRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule02h13.BuildingRule.HVACRule(),
                index_rmd=BASELINE_0,
                list_path="$.building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            )

        def create_data(self, context, data=None):
            building_b = context.BASELINE_0
            hvac_zone_list_w_area_dict_b = get_hvac_zone_list_w_area_dict(building_b)

            zone_total_occupant_dict_b = {
                zone_b["id"]: sum(
                    find_all("$.spaces[*].number_of_occupants", zone_b),
                    0,
                )
                * ureg("people")
                for zone_b in find_all("$.building_segments[*].zones[*]", building_b)
            }

            return {
                "hvac_zone_list_w_area_dict_b": hvac_zone_list_w_area_dict_b,
                "zone_total_occupant_dict_b": zone_total_occupant_dict_b,
            }

        def list_filter(self, context_item, data=None):
            hvac_b = context_item.BASELINE_0
            hvac_id_b = hvac_b["id"]
            hvac_zone_list_w_area_dict_b = data["hvac_zone_list_w_area_dict_b"]

            return hvac_id_b in hvac_zone_list_w_area_dict_b

        class HVACRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule02h13.BuildingRule.HVACRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    required_fields={
                        "$": ["fan_system"],
                        "fan_system": ["minimum_outdoor_airflow"],
                    },
                    precision={
                        "hvac_min_OA_flow": {"precision": 0.1, "unit": "cfm"},
                        "avg_occ_density": {"precision": 0.1, "unit": "people/ft2"},
                    },
                )

            def get_calc_vals(self, context, data=None):
                hvac_b = context.BASELINE_0
                hvac_zone_list_w_area_dict_b = data["hvac_zone_list_w_area_dict_b"]
                zone_total_occupant_dict_b = data["zone_total_occupant_dict_b"]

                hvac_id_b = hvac_b["id"]
                fan_system_b = hvac_b["fan_system"]
                hvac_min_OA_flow = fan_system_b["minimum_outdoor_airflow"]
                zone_id_list_b = hvac_zone_list_w_area_dict_b[hvac_id_b]["zone_list"]
                hvac_area_b = hvac_zone_list_w_area_dict_b[hvac_id_b]["total_area"]
                demand_control_ventilation_control_b = fan_system_b.get(
                    "demand_control_ventilation_control"
                )

                avg_occ_density = (
                    sum(
                        [
                            zone_total_occupant_dict_b[zone_id_b]
                            for zone_id_b in zone_id_list_b
                        ]
                    )
                    / hvac_area_b
                )

                is_DCV_modeled_b = False
                if (
                    demand_control_ventilation_control_b
                    and demand_control_ventilation_control_b
                    != DEMAND_CONTROL_VENTILATION_CONTROL.NONE
                ):
                    is_DCV_modeled_b = True

                return {
                    "hvac_min_OA_flow": CalcQ("air_flow_rate", hvac_min_OA_flow),
                    "is_DCV_modeled_b": is_DCV_modeled_b,
                    "avg_occ_density": CalcQ("area_occ_density", avg_occ_density),
                }

            def rule_check(self, context, calc_vals=None, data=None):
                hvac_min_OA_flow = calc_vals["hvac_min_OA_flow"]
                avg_occ_density = calc_vals["avg_occ_density"]
                is_DCV_modeled_b = calc_vals["is_DCV_modeled_b"]

                return (
                    (
                        hvac_min_OA_flow > MIN_OA_CFM
                        or self.precision_comparison["hvac_min_OA_flow"](
                            hvac_min_OA_flow,
                            MIN_OA_CFM,
                        )
                    )
                    and avg_occ_density > OCCUPANT_DENSITY_LIMIT
                    and is_DCV_modeled_b
                ) or (
                    (
                        (
                            hvac_min_OA_flow < MIN_OA_CFM
                            or self.precision_comparison["hvac_min_OA_flow"](
                                hvac_min_OA_flow,
                                MIN_OA_CFM,
                            )
                        )
                        or (
                            avg_occ_density < OCCUPANT_DENSITY_LIMIT
                            or self.precision_comparison["avg_occ_density"](
                                avg_occ_density,
                                OCCUPANT_DENSITY_LIMIT,
                            )
                        )
                    )
                    and not is_DCV_modeled_b
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                hvac_min_OA_flow = calc_vals["hvac_min_OA_flow"]
                avg_occ_density = calc_vals["avg_occ_density"]
                is_DCV_modeled_b = calc_vals["is_DCV_modeled_b"]

                return (
                    (std_ge(hvac_min_OA_flow, MIN_OA_CFM))
                    and avg_occ_density > OCCUPANT_DENSITY_LIMIT
                    and is_DCV_modeled_b
                ) or (
                    (
                        hvac_min_OA_flow < MIN_OA_CFM
                        or self.precision_comparison["hvac_min_OA_flow"](
                            hvac_min_OA_flow,
                            MIN_OA_CFM,
                        )
                    )
                    and (std_ge(avg_occ_density, OCCUPANT_DENSITY_LIMIT))
                    and not is_DCV_modeled_b
                )
