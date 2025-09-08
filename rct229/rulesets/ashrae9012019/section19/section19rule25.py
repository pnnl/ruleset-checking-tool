import itertools

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_cooling import (
    get_proposed_hvac_modeled_with_virtual_cooling,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_proposed_hvac_modeled_with_virtual_heating import (
    get_proposed_hvac_modeled_with_virtual_heating,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.pint_utils import ZERO, CalcQ

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class PRM9012019Rule10q01(RuleDefinitionListIndexedBase):
    """Rule 25 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule10q01, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=True, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule10q01.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-25",
            description="Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the baseline design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules for the proposed building excluding exception #1 and Section G3.1.2.4.",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_u = context.USER
        rmd_b = context.BASELINE_0
        rmd_p = context.PROPOSED

        HVAC_systems_virtual_list_p = list(
            set(
                get_proposed_hvac_modeled_with_virtual_cooling(rmd_u, rmd_p)
                + get_proposed_hvac_modeled_with_virtual_heating(rmd_u, rmd_p)
            )
        )

        hvac_zone_list_w_area_dict_p = get_hvac_zone_list_w_area_by_rmd_dict(rmd_p)

        zones_virtual_heating_cooling_list_p = list(
            set(
                [
                    zone_id_p
                    for hvac_id_p in HVAC_systems_virtual_list_p
                    for zone_id_p in hvac_zone_list_w_area_dict_p[hvac_id_p][
                        "zone_list"
                    ]
                ]
            )
        )

        inapplicable_hvac_with_virtual_heating_cooling_list_b = list(
            set(
                itertools.chain(
                    *[
                        get_list_hvac_systems_associated_with_zone(rmd_b, zone_id_p)
                        for zone_id_p in zones_virtual_heating_cooling_list_p
                    ]
                )
            )
        )

        return {
            "inapplicable_hvac_with_virtual_heating_cooling_list_b": inapplicable_hvac_with_virtual_heating_cooling_list_b
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule10q01.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "operation_during_occupied",
                        "minimum_outdoor_airflow",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            inapplicable_hvac_with_virtual_heating_cooling_list_b = data[
                "inapplicable_hvac_with_virtual_heating_cooling_list_b"
            ]

            return (
                hvac_id_b not in inapplicable_hvac_with_virtual_heating_cooling_list_b
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0

            operation_during_occupied_b = hvac_b["fan_system"][
                "operation_during_occupied"
            ]
            minimum_outdoor_airflow_b = hvac_b["fan_system"]["minimum_outdoor_airflow"]

            return {
                "operation_during_occupied_b": operation_during_occupied_b,
                "minimum_outdoor_airflow_b": CalcQ(
                    "air_flow_rate", minimum_outdoor_airflow_b
                ),
            }

        def rule_check(self, context, calc_vals=None, data=None):
            operation_during_occupied_b = calc_vals["operation_during_occupied_b"]
            minimum_outdoor_airflow_b = calc_vals["minimum_outdoor_airflow_b"]

            return (
                operation_during_occupied_b == FAN_SYSTEM_OPERATION.CONTINUOUS
                and minimum_outdoor_airflow_b > ZERO.FLOW
            ) or (
                operation_during_occupied_b == FAN_SYSTEM_OPERATION.CYCLING
                and minimum_outdoor_airflow_b == ZERO.FLOW
            )
