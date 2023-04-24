from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_serving_zone_health_safety_vent_reqs import (
    get_hvac_systems_serving_zone_health_safety_vent_reqs,
)

FAN_SYSTEM_OPERATION = schema_enums["FanSystemOperationOptions"]


class Section19Rule28(RuleDefinitionListIndexedBase):
    """Rule 28 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule28, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, False, True),
            each_rule=Section19Rule28.HVACRule(),
            index_rmr="proposed",
            id="19-28",
            description="Schedules for HVAC fans in the baseline design model that provide outdoor air for ventilation shall be cycled ON and OFF "
            "to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules per the proposed column exceptions #s 2 and 3."
            "#2 HVAC fans shall remain on during occupied and unoccupied hours in spaces that have health- and safety mandated minimum ventilation requirements during unoccupied hours."
            "#3 HVAC fans shall remain on during occupied and unoccupied hours in systems primarily serving computer rooms.",
            ruleset_section_title="HVAC - General",
            standard_section="Table G3.1-4 Schedules for the proposed building excluding exceptions #s 2 and 3 and Section G3.1.2.4.",
            is_primary_rule=True,
            rmr_context="ruleset_model_instances/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmi_p = context.proposed

        inapplicable_hvac_sys_list_p = list(
            set(
                get_hvac_systems_primarily_serving_comp_room(rmi_p)
                + get_hvac_systems_serving_zone_health_safety_vent_reqs(rmi_p)
            )
        )

        return {"inapplicable_hvac_sys_list_p": inapplicable_hvac_sys_list_p}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(Section19Rule28.HVACRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, False, True),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "operation_during_occupied",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_p = context.proposed
            hvac_id_p = hvac_p["id"]
            inapplicable_hvac_sys_list_p = data["inapplicable_hvac_sys_list_p"]

            return hvac_id_p not in inapplicable_hvac_sys_list_p

        def get_calc_vals(self, context, data=None):
            hvac_p = context.proposed

            operation_during_unoccupied_p = hvac_p["fan_system"][
                "operation_during_unoccupied"
            ]

            return {"operation_during_unoccupied_p": operation_during_unoccupied_p}

        def rule_check(self, context, calc_vals=None, data=None):
            operation_during_unoccupied_p = calc_vals["operation_during_unoccupied_p"]

            return operation_during_unoccupied_p == FAN_SYSTEM_OPERATION.CYCLING
