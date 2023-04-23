import itertools

from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_dict,
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
from rct229.utils.assertions import getattr_
from rct229.utils.pint_utils import ZERO

FAN_SYSTEM_OPERATION = schema_enums["FanSystemOperationOptions"]


class Section19Rule25(RuleDefinitionListIndexedBase):
    """Rule 25 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule25, self).__init__(
            rmrs_used=UserBaselineProposedVals(True, True, True),
            each_rule=Section19Rule25.HVACRule(),
            index_rmr="baseline",
            id="19-25",
            description="Schedules for HVAC fans that provide outdoor air for ventilation shall run continuously whenever spaces are occupied in the baseline design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1-4 Schedules for the proposed building excluding exception #1 and Section G3.1.2.4.",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_u = context.user
        rmi_b = context.baseline
        rmi_p = context.proposed

        HVAC_systems_virtual_list_p = list(
            set(
                get_proposed_hvac_modeled_with_virtual_cooling(rmi_u, rmi_p)
                + get_proposed_hvac_modeled_with_virtual_heating(rmi_u, rmi_p)
            )
        )

        zones_virtual_heating_cooling_list_p = list(
            set(
                [
                    zone_id_p
                    for hvac_id_p in HVAC_systems_virtual_list_p
                    for zone_id_p in get_hvac_zone_list_w_area_dict(rmi_p)[hvac_id_p][
                        "zone_list"
                    ]
                ]
            )
        )

        inapplicable_hvac_with_virtual_heating_cooling_list_b = list(
            set(
                list(
                    itertools.chain(
                        *[
                            get_list_hvac_systems_associated_with_zone(rmi_b, zone_id_p)
                            for zone_id_p in zones_virtual_heating_cooling_list_p
                        ]
                    )
                )
            )
        )

        return {
            "inapplicable_hvac_with_virtual_heating_cooling_list_b ": inapplicable_hvac_with_virtual_heating_cooling_list_b
        }

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule25.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(True, True, True),
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.baseline
            hvac_id_b = hvac_b["id"]
            inapplicable_hvac_with_virtual_heating_cooling_list_b = data[
                "inapplicable_hvac_with_virtual_heating_cooling_list_b"
            ]

            return (
                hvac_id_b not in inapplicable_hvac_with_virtual_heating_cooling_list_b
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.baseline

            operation_during_occupied_b = getattr_(
                hvac_b, "HVAC", "fan_system", "operation_during_occupied"
            )
            minimum_outdoor_airflow_b = getattr_(
                hvac_b, "HVAC", "fan_system", "minimum_outdoor_airflow"
            )

            return {
                "operation_during_occupied_b": operation_during_occupied_b,
                "minimum_outdoor_airflow_b": minimum_outdoor_airflow_b,
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
