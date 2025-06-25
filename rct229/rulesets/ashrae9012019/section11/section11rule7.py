from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_1_1_2_fns import (
    table_g3_1_2_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_bats_and_swh_use import (
    get_swh_bats_and_swh_use,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_components_associated_with_each_swh_bat import (
    get_swh_components_associated_with_each_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_type import (
    get_swh_equipment_type,
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

SERVICE_WATER_HEATING_SPACE = SchemaEnums.schema_enums[
    "ServiceWaterHeatingAreaOptions2019ASHRAE901"
]


class PRM9012019Rule49y39(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule49y39, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=PRM9012019Rule49y39.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-7",
            description="Except in buildings that will have no service water heating loads, the service water heating system type in the baseline building design shall be as specified in Table G3.1.1-2 for each building area type in the proposed design.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a & b",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule49y39.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=True,
                ),
                index_rmd=BASELINE_0,
                each_rule=PRM9012019Rule49y39.RMDRule.SWHBATRule(),
            )

        def create_data(self, context, data):
            rmd_p = context.PROPOSED
            rmd_b = context.BASELINE_0

            service_water_heating_uses_p = {
                swh_use["id"]: swh_use.get("use", 0.0)
                for swh_use in find_all(
                    "$.service_water_heating_uses[*]",
                    rmd_p,
                )
            }

            swh_equip_type_b = {
                swh_equip_id: get_swh_equipment_type(rmd_b, swh_equip_id)
                for swh_equip_id in find_all(
                    "$.service_water_heating_equipment[*].id", rmd_b
                )
            }

            return {
                "service_water_heating_uses_p": service_water_heating_uses_p,
                "swh_equip_type_b": swh_equip_type_b,
            }

        def create_context_list(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED

            swh_bats_and_equip_association_b = (
                get_swh_components_associated_with_each_swh_bat(rmd_b)
            )
            swh_bats_and_uses_p = get_swh_bats_and_swh_use(rmd_p)

            building_area_type_SWH_equip_dict = {}
            building_area_type_and_uses = {}
            for (
                bat_type,
                SWH_Equipment_Associations,
            ) in swh_bats_and_equip_association_b.items():
                building_area_type_SWH_equip_dict[bat_type] = {}
                building_area_type_SWH_equip_dict[bat_type]["id"] = bat_type
                building_area_type_SWH_equip_dict[bat_type][
                    "SWH_Equipment_Associations"
                ] = SWH_Equipment_Associations

                building_area_type_and_uses[bat_type] = {}
                building_area_type_and_uses[bat_type]["id"] = bat_type
                building_area_type_and_uses[bat_type][
                    "swh_bats_and_uses_p"
                ] = swh_bats_and_uses_p[bat_type]

            return [
                produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=building_area_type_SWH_equip_dict[bat_type],
                    PROPOSED=building_area_type_and_uses[bat_type],
                )
                for bat_type, SWH_Equipment_Associations in swh_bats_and_equip_association_b.items()
            ]

        class SWHBATRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule49y39.RMDRule.SWHBATRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                )

            def is_applicable(self, context, data=None):
                building_area_type_and_uses_p = context.PROPOSED
                service_water_heating_uses_p = data["service_water_heating_uses_p"]
                swh_bat_p = building_area_type_and_uses_p["id"]

                return swh_bat_p != SERVICE_WATER_HEATING_SPACE.PARKING_GARAGE or all(
                    service_water_heating_uses_p[swh_uses_id_p] > 0.0
                    for swh_uses_id_p in building_area_type_and_uses_p[
                        "swh_bats_and_uses_p"
                    ]
                )

            def get_calc_vals(self, context, data=None):
                building_area_type_SWH_equip_b = context.BASELINE_0
                swh_equip_type_b = data["swh_equip_type_b"]
                swh_bat_b = building_area_type_SWH_equip_b["id"]

                expected_swh_equip_type_list = []
                swh_equip_type_list_b = []
                for swh_heating_equipment_id in building_area_type_SWH_equip_b[
                    "SWH_Equipment_Associations"
                ].swh_heating_eq:
                    expected_swh_equip_type_list.append(
                        table_g3_1_2_lookup(swh_bat_b)["baseline_heating_method"]
                    )

                    if (
                        swh_equip_type_b[swh_heating_equipment_id]
                        == "PROPANE_INSTANTANEOUS"
                    ):
                        swh_equip_type_list_b.append("GAS_INSTANTANEOUS_WATER_HEATER")
                    elif (
                        swh_equip_type_b[swh_heating_equipment_id] == "PROPANE_STORAGE"
                    ):
                        swh_equip_type_list_b.append("GAS_STORAGE_WATER_HEATER")
                    else:
                        swh_equip_type_list_b.append(
                            swh_equip_type_b[swh_heating_equipment_id]
                        )

                return {
                    "expected_swh_equip_type_list": expected_swh_equip_type_list,
                    "swh_equip_type_list_b": swh_equip_type_list_b,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                building_area_type_and_uses_p = context.PROPOSED
                service_water_heating_uses_p = data["service_water_heating_uses_p"]

                return any(
                    [
                        service_water_heating_uses_p[swh_uses_id_p] <= 0.0
                        for swh_uses_id_p in building_area_type_and_uses_p[
                            "swh_bats_and_uses_p"
                        ]
                    ]
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                swh_uses_ids_p = context.PROPOSED
                swh_bat_p = swh_uses_ids_p["id"]

                return f"Building area type {swh_bat_p} has no service water heating use. Confirm that this is correct for this building area type."

            def rule_check(self, context, calc_vals=None, data=None):
                expected_swh_equip_type_list = calc_vals["expected_swh_equip_type_list"]
                swh_equip_type_list_b = calc_vals["swh_equip_type_list_b"]

                return expected_swh_equip_type_list == swh_equip_type_list_b
