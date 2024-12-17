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

                table_7_8 = [
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (0*ureg("kW"), True),
                        "Capacity max. (threshold, inclusive?)": (12*ureg("kW"), False),
                        "Draw Pattern": "",
                        "Efficiency (value/equation, metric)": (lambda v_m: 0.3 + 27 / v_m, SWHEfficiencyMetricOptions.STANDBY_LOSS_FRACTION),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (75000*ureg("Btu/h"), False),
                        "Capacity max. (threshold, inclusive?)": (105000*ureg("Btu/h"), True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.2674 - (0.0009 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (75000 * ureg("Btu/h"), False),
                        "Capacity max. (threshold, inclusive?)": (105000 * ureg("Btu/h"), True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.5362 - (0.0012 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (75000 * ureg("Btu/h"), False),
                        "Capacity max. (threshold, inclusive?)": (105000 * ureg("Btu/h"), True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.6002 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (75000 * ureg("Btu/h"), False),
                        "Capacity max. (threshold, inclusive?)": (105000 * ureg("Btu/h"), True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.6597 - (0.0009 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (105000 * ureg("Btu/h"), False),
                        "Capacity max. (threshold, inclusive?)": (9999999 * ureg("Btu/h"), True),
                        "Draw Pattern": "",
                        "Efficiency (value/equation, metric)": (
                            lambda q, v: q / 800 + 110 * v ** 0.5, SWHEfficiencyMetricOptions.STANDBY_LOSS_ENERGY
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (105000 * ureg("Btu/h"), False),
                        "Capacity max. (threshold, inclusive?)": (9999999 * ureg("Btu/h"), True),
                        "Draw Pattern": "",
                        "Efficiency (value/equation, metric)": (0.80, SWHEfficiencyMetricOptions.THERMAL_EFFICIENCY),
                    }
                ]
                table_f_2 = [
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.3456 - (0.0020 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.5982 - (0.0019 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.6483 - (0.0017 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.6920 - (0.0013 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.6470 - (0.0006 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.7689 - (0.0005 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.7897 - (0.0004 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Gas storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.8072 - (0.0003 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.8808 - (0.0008 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.9254 - (0.0003 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.9307 - (0.0002 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (20*ureg("gal"), True),
                        "Capacity max. (threshold, inclusive?)": (55*ureg("gal"), True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 0.9349 - (0.0001 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "Very small",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 1.9236 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "Low",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 2.0440 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "Medium",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 2.1171 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    },
                    {
                        "Equipment Type": "Electric storage water heater",
                        "Capacity min. (threshold, inclusive?)": (55*ureg("gal"), False),
                        "Capacity max. (threshold, inclusive?)": (100*ureg("gal"), True),
                        "Draw Pattern": "High",
                        "Efficiency (value/equation, metric)": (
                            lambda v_r: 2.2418 - (0.0011 * v_r), SWHEfficiencyMetricOptions.UNIFORM_ENERGY_FACTOR
                        ),
                    }
                ]

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
