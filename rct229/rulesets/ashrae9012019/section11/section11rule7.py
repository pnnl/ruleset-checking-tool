from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_1_1_2_fns import (
    table_g3_1_2_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_components_associated_with_each_swh_bat import (
    get_swh_components_associated_with_each_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_bats_and_swh_use import (
    get_swh_bats_and_swh_use,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_equipment_type import (
    get_swh_equipment_type,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.schema.schema_enums import SchemaEnums


SERVICE_WATER_HEATING_SPACE = SchemaEnums.schema_enums[
    "ServiceWaterHeatingSpaceOptions2019ASHRAE901"
]


class Section11Rule7(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule7, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule7.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-7",
            description="Except in buildings that will have no service water heating loads, the service water heating system type in the baseline building design shall be as specified in Table G3.1.1-2 for each building area type in the proposed design.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a & b",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={"$": ["calendar"], "$.calendar": ["is_leap_year"]},
            data_items={"is_leap_year": (BASELINE_0, "calendar/is_leap_year")},
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section11Rule7.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0=True,
                    PROPOSED=True,
                ),
                index_rmd=BASELINE_0,
                each_rule=Section11Rule7.RMDRule.SWHBATRule(),
            )

        def create_data(self, context, data):
            rmd_p = context.PROPOSED
            rmd_b = context.BASELINE_0

            service_water_heating_uses_p = {
                swh_use["id"]: swh_use.get("use", 0.0)
                for swh_use in find_all(
                    "$.buildings[*].building_segments[*].zones[*].spaces[*].service_water_heating_uses[*]",
                    rmd_p,
                )
            }

            swh_equip_type_b = {
                get_swh_equipment_type(rmd_b, swh_equip_id)
                for swh_equip_id in find_all(
                    "$.service_water_heating_equipment[*]", rmd_b
                )
            }

            return {
                "service_water_heating_uses_p": service_water_heating_uses_p,
                "swh_equip_type_b": swh_equip_type_b,
            }

        def create_context_list(self, context, data=None):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            is_leap_year_b = data["is_leap_year"]

            swh_bats_and_uses_b = get_swh_components_associated_with_each_swh_bat(
                rmd_b, is_leap_year_b
            )
            swh_bats_and_uses_p = get_swh_bats_and_swh_use(rmd_p)

            return [
                produce_ruleset_model_description(
                    USER=False,
                    BASELINE_0={bat_type: SWH_Equipment_Associations},
                    PROPOSED={bat_type: swh_bats_and_uses_p[bat_type]},
                )
                for bat_type, SWH_Equipment_Associations in swh_bats_and_uses_b.items()
            ]

        class SWHBATRule(RuleDefinitionBase):
            def __init__(self):
                super(Section11Rule7.RMDRule.SWHBATRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                )

            def is_applicable(self, context, data=None):
                swh_uses_ids_p = context.PROPOSED
                service_water_heating_uses_p = data["service_water_heating_uses_p"]

                for swh_uses_id_p in swh_uses_ids_p:
                    if (
                        service_water_heating_uses_p[swh_uses_id_p] > 0.0
                        or service_water_heating_uses_p
                        != SERVICE_WATER_HEATING_SPACE.PARKING_GARAGE
                    ):
                        return True
                    else:
                        return False

            def manual_check_required(self, context, calc_vals=None, data=None):
                swh_uses_ids_p = context.PROPOSED
                service_water_heating_uses_p = data["service_water_heating_uses_p"]

                for swh_uses_id_p in swh_uses_ids_p:
                    if service_water_heating_uses_p[swh_uses_id_p] > 0.0:
                        has_swh = True
                    else:
                        has_swh = False

                return has_swh

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                swh_uses_ids_p = context.PROPOSED
                swh_bat = next(iter(swh_uses_ids_p))

                return f"Building area type {swh_bat} has no service water heating use. Confirm that this is correct for this building area type."

            def get_calc_vals(self, context, data=None):
                SWH_Equipment_Association = context.BASELINE_0
                swh_equip_type_b = data["swh_equip_type_b"]

                for (
                    swh_heating_equipment_id
                ) in SWH_Equipment_Association.swh_heating_eq:
                    expected_swh_equip_type = table_g3_1_2_lookup(swh_bat)
                    swh_equip_type_b = swh_equip_type_b[swh_heating_equipment_id]

                return {
                    "expected_swh_equip_type": expected_swh_equip_type,
                    "swh_equip_type_b": swh_equip_type_b,
                }

            def rule_check(self, context, calc_vals=None, data=None):
                swh_equip_type_b = calc_vals["swh_equip_type_b"]
                expected_swh_equip_type = calc_vals["expected_swh_equip_type"]

                return swh_equip_type_b == expected_swh_equip_type
