from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_components_associated_with_each_swh_bat import (
    get_swh_components_associated_with_each_swh_bat
)
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all
from rct229.schema.config import ureg


EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
SWHEfficiencyMetricOptions = SchemaEnums.schema_enums["ServiceWaterHeatingEfficiencyMetricOptions"]
SWHTankOptions = SchemaEnums.schema_enums["ServiceWaterHeatingTankOptions"]


class Section11Rule10(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(Section11Rule10, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section11Rule10.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-10",
            description="The service water heating system type in the baseline building design shall match the minimum efficiency requirements in Section 7.4.2.",
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, a & b",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section11Rule10.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=Section11Rule10.RMDRule.SWHEquipRule(),
                index_rmd=BASELINE_0,
                list_path="$.service_water_heating_equipment[*]",
            )

        def is_applicable(self, context, data=None):
            rmd_b = context.BASELINE_0

            swh_equipment_list_b = find_all(
                "$.service_water_heating_equipment[*]", rmd_b
            )

            return swh_equipment_list_b

        def get_calc_vals(self, context, data=None):
            rmd_b = context.BASELINE_0
            is_leap_year_b = data["is_leap_year"]
            shw_bats_and_equip_dict_b = get_swh_components_associated_with_each_swh_bat(rmd_b, is_leap_year_b)
            return {
                "shw_bats_and_equip_dict_b": shw_bats_and_equip_dict_b,
            }

        class SWHEquipRule(RuleDefinitionBase):
            def __init__(self):
                super(Section11Rule10.RMDRule.SWHEquipRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=False,
                    ),
                    required_fields={
                        "$": ["tank", "efficiency_metric_types", "efficiency_metric_values"],
                        "tank": ["type", "storage_capacity"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                swh_equip_b = context.BASELINE_0
                swh_fuel_type = swh_equip_b.get("heater_fuel_type")
                swh_tank_type = swh_equip_b["tank"]["type"]
                storage_volume_b = swh_equip_b["tank"]["storage_capacity"]
                swh_input_power_b = swh_equip_b.get("input_power")
                swh_capacity_per_volume = swh_input_power_b / storage_volume_b if swh_input_power_b else None

                # Determine swh_type
                INSTANTANEOUS_TYPES = [
                    SWHTankOptions.CONSUMER_INSTANTANEOUS,
                    SWHTankOptions.COMMERCIAL_INSTANTANEOUS,
                    SWHTankOptions.RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS
                ]
                STORAGE_TYPES = [
                    SWHTankOptions.CONSUMER_STORAGE,
                    SWHTankOptions.COMMERCIAL_STORAGE
                ]
                if swh_tank_type in INSTANTANEOUS_TYPES:
                    swh_type = "INSTANTANEOUS"
                elif swh_tank_type in STORAGE_TYPES:
                    if swh_fuel_type == EnergySourceOptions.ELECTRICITY:
                        swh_type = "ELECTRIC_RESISTANCE_STORAGE"
                    elif swh_fuel_type in [EnergySourceOptions.NATURAL_GAS, EnergySourceOptions.PROPANE]:
                        swh_type = "GAS_STORAGE"
                    else:
                        swh_type = "OTHER"
                else:
                    swh_type = "OTHER"

                # Determine draw_pattern_b
                draw_pattern_b = swh_equip_b.get("draw_pattern")
                if not draw_pattern_b:
                    first_hour_rating_b = swh_equip_b.get("first_hour_rating")
                    if first_hour_rating_b is not None:
                        first_hour_rating_gal = (first_hour_rating_b * ureg("L")).to("gal").magnitude
                        if first_hour_rating_gal < 18:
                            draw_pattern_b = "Very small"
                        elif first_hour_rating_gal < 51:
                            draw_pattern_b = "Low"
                        elif first_hour_rating_gal < 75:
                            draw_pattern_b = "Medium"
                        else:
                            draw_pattern_b = "High"

                # draw_pattern_b will be None if the SWH draw pattern is not defined and the first hour rating is not defined

                shw_bats_and_equip_dict_b = data["shw_bats_and_equip_dict_b"]


                pass
                # return {
                #     "tank_type_b": tank_type_b,
                #     "storage_volume_b": CalcQ(storage_volume_b),
                #     "expected_efficiency_b": expected_efficiency_b,
                #     "standby_loss_target_b": standby_loss_target_b,
                #     "modeled_efficiency_b": modeled_efficiency_b,
                #     "modeled_standby_loss_b": modeled_standby_loss_b,
                # }

            def manual_check_required(self, context, calc_vals=None, data=None):
                pass

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                pass

            def rule_check(self, context, calc_vals=None, data=None):
                pass
