from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_primarily_serving_comp_room import (
    get_hvac_systems_primarily_serving_comp_room,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_serving_zone_health_safety_vent_reqs import (
    get_hvac_systems_serving_zone_health_safety_vent_reqs,
)
from rct229.schema.schema_enums import SchemaEnums

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


class PRM9012019Rule20z34(RuleDefinitionListIndexedBase):
    """Rule 29 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule20z34, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule20z34.HVACRule(),
            index_rmd=BASELINE_0,
            id="19-29",
            description="Schedules for HVAC fans in the baseline design model that provide outdoor air for ventilation shall be cycled ON and OFF "
            "to meet heating and cooling loads during unoccupied hours excluding HVAC systems that meet Table G3.1-4 Schedules per the proposed column exceptions #s 2 and 3."
            "#2 HVAC fans shall remain on during occupied and unoccupied hours in spaces that have health- and safety mandated minimum ventilation requirements during unoccupied hours."
            "#3 HVAC fans shall remain on during occupied and unoccupied hours in systems primarily serving computer rooms.",
            ruleset_section_title="HVAC - General",
            standard_section="Table G3.1-4 Schedules proposed building column excluding exceptions #s 2 and 3 and G3.1.2.4.",
            is_primary_rule=True,
            rmd_context="ruleset_model_descriptions/0",
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0

        inapplicable_hvac_sys_list_b = list(
            set(
                get_hvac_systems_primarily_serving_comp_room(rmd_b)
                + get_hvac_systems_serving_zone_health_safety_vent_reqs(rmd_b)
            )
        )

        return {"inapplicable_hvac_sys_list_b": inapplicable_hvac_sys_list_b}

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule20z34.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["fan_system"],
                    "fan_system": [
                        "operation_during_unoccupied",
                    ],
                },
            )

        def is_applicable(self, context, data=None):
            hvac_b = context.BASELINE_0
            hvac_id_b = hvac_b["id"]
            inapplicable_hvac_sys_list_b = data["inapplicable_hvac_sys_list_b"]

            return hvac_id_b not in inapplicable_hvac_sys_list_b

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0

            operation_during_unoccupied_b = hvac_b["fan_system"][
                "operation_during_unoccupied"
            ]

            return {"operation_during_unoccupied_b": operation_during_unoccupied_b}

        def rule_check(self, context, calc_vals=None, data=None):
            operation_during_unoccupied_b = calc_vals["operation_during_unoccupied_b"]

            return operation_during_unoccupied_b == FAN_SYSTEM_OPERATION.CYCLING
