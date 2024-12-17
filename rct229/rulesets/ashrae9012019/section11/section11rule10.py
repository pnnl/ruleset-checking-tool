from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.config import ureg
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_F_2_fns import (
    table_f_2_lookup
)
from rct229.rulesets.ashrae9012019.data_fns.table_7_8_fns import (
    table_7_8_lookup
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.assertions import assert_

EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
SWHEfficiencyMetricOptions = SchemaEnums.schema_enums["ServiceWaterHeatingEfficiencyMetricOptions"]
SWHTankOptions = SchemaEnums.schema_enums["ServiceWaterHeatingTankOptions"]


CAPACITY_PER_VOLUME_LIMIT = 4000*ureg("Btu/h/gallon")
INSTANTANEOUS_TYPES = [
    SWHTankOptions.CONSUMER_INSTANTANEOUS,
    SWHTankOptions.COMMERCIAL_INSTANTANEOUS,
    SWHTankOptions.RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS
]
STORAGE_TYPES = [
    SWHTankOptions.CONSUMER_STORAGE,
    SWHTankOptions.COMMERCIAL_STORAGE
]


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

        class SWHEquipRule(RuleDefinitionBase):
            def __init__(self):
                super(Section11Rule10.RMDRule.SWHEquipRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=False,
                    ),
                    required_fields={
                        "$": ["tank", "input_power", "efficiency_metric_types", "efficiency_metric_values"],
                        "tank": ["type", "storage_capacity"],
                    },
                )

            def get_calc_vals(self, context, data=None):
                swh_equip_b = context.BASELINE_0
                swh_tank_type_b = swh_equip_b["tank"]["type"]
                swh_tank_storage_volume_b = swh_equip_b["tank"]["storage_capacity"]*ureg("L")
                swh_input_power_b = swh_equip_b["input_power"]*ureg("W")
                swh_efficiency_b = dict(zip(swh_equip_b["efficiency_metric_types"], swh_equip_b["efficiency_metric_values"]))
                swh_input_power_per_volume_b = swh_input_power_b / swh_tank_storage_volume_b

                swh_fuel_type_b = swh_equip_b.get("heater_fuel_type")

                # Determine swh_type
                if swh_tank_type_b in INSTANTANEOUS_TYPES:
                    swh_type = "INSTANTANEOUS"
                elif swh_tank_type_b in STORAGE_TYPES:
                    if swh_fuel_type_b == EnergySourceOptions.ELECTRICITY:
                        swh_type = "ELECTRIC_RESISTANCE_STORAGE"
                    elif swh_fuel_type_b in [EnergySourceOptions.NATURAL_GAS, EnergySourceOptions.PROPANE]:
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
                        first_hour_rating_gal = first_hour_rating_b*ureg("L").to("gal").magnitude
                        if first_hour_rating_gal < 18:
                            draw_pattern_b = "Very small"
                        elif first_hour_rating_gal < 51:
                            draw_pattern_b = "Low"
                        elif first_hour_rating_gal < 75:
                            draw_pattern_b = "Medium"
                        else:
                            draw_pattern_b = "High"
                # Overwrite draw pattern to empty string if the input power is greater than 105,000 Btu/h
                draw_pattern_b = "" if swh_input_power_b > 105000*ureg("Btu/h") else draw_pattern_b
                # draw_pattern_b will be None if the SWH draw pattern is not defined and the first hour rating is not defined
                # this will cause efficiency_data to be empty if the draw_pattern is required for the lookup

                efficiency_data = None
                expected_efficiency_b = None
                expected_efficiency_metric_b = None
                standby_loss_target_b = None
                standby_loss_target_metric_b = None
                modeled_efficiency_b = None
                modeled_standby_loss_b = None

                # Get Electric Storage Water Heater Efficiency Data
                if swh_type == "ELECTRIC_RESISTANCE_STORAGE":
                    if swh_input_power_b < 12*ureg("kW"):
                        # Lookup the expected efficiency from Appendix F-2
                        assert_(draw_pattern_b is not None, "Draw pattern must be defined for table F-2 lookup")
                        efficiency_data = table_f_2_lookup(
                            "Electric storage water heater",
                            swh_tank_storage_volume_b,
                            draw_pattern_b,
                        )
                    else:
                        # Lookup the expected efficiency from Table 7.8
                        # Note: Draw pattern is not used in this lookup
                        efficiency_data = table_7_8_lookup(
                            "Electric storage water heater",
                            swh_input_power_b,
                        )

                # Get Gas Storage Water Heater Efficiency Data
                elif swh_type == "GAS_STORAGE":
                    if swh_input_power_b <= 75000*ureg("Btu/h"):
                        # Lookup the expected efficiency from Appendix F-2
                        assert_(draw_pattern_b is not None, "Draw pattern must be defined for table F-2 lookup")
                        efficiency_data = table_f_2_lookup(
                            "Gas storage water heater",
                            swh_tank_storage_volume_b,
                            draw_pattern_b
                        )
                    else:
                        # Lookup the expected efficiency from Table 7.8
                        assert_(draw_pattern_b is not None, "Draw pattern must be defined for table 7-8 lookup")
                        efficiency_data = table_7_8_lookup(
                            "Gas storage water heater",
                            swh_input_power_b,
                            draw_pattern_b
                        )
                        # Note: If the input power is greater than 105,000 Btu/h, there will be a thermal efficiency and standby loss target

                if efficiency_data:
                    to_remove = None
                    for efficiency in efficiency_data:
                        if "STANDBY" in efficiency["metric"]:
                            standby_loss_target_b = eval(efficiency["equation"], {"__builtins__": None}, {"v": swh_tank_storage_volume_b.to("gallon").magnitude, "q": swh_input_power_b.to("Btu/h").magnitude})
                            standby_loss_target_metric_b = efficiency["metric"]
                            modeled_standby_loss_b = swh_efficiency_b.get(standby_loss_target_metric_b)
                            to_remove = efficiency
                            break

                    if to_remove is not None:
                        efficiency_data.remove(to_remove)

                    if len(efficiency_data) == 1:
                        expected_efficiency_metric_b = efficiency_data[0]["metric"]
                        expected_efficiency_b = eval(efficiency_data[0]["equation"], {"__builtins__": None}, {"v": swh_tank_storage_volume_b.to("gallon").magnitude, "q": swh_input_power_b.to("Btu/h").magnitude})
                        modeled_efficiency_b = swh_efficiency_b.get(expected_efficiency_metric_b)

                return {
                    "swh_tank_type_b": swh_tank_type_b,
                    "swh_tank_storage_volume_b": CalcQ("volume", swh_tank_storage_volume_b),
                    "modeled_efficiency_b": modeled_efficiency_b,
                    "modeled_standby_loss_b": modeled_standby_loss_b,
                    "swh_input_power_per_volume_b": CalcQ("power/volume", swh_input_power_per_volume_b),
                    "expected_efficiency_b": expected_efficiency_b,
                    "expected_efficiency_metric_b": expected_efficiency_metric_b,
                    "standby_loss_target_b": standby_loss_target_b,
                    "standby_loss_target_metric_b": standby_loss_target_metric_b,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                swh_tank_type_b = calc_vals["swh_tank_type_b"]
                swh_input_power_per_volume_b = calc_vals["swh_input_power_per_volume_b"]
                swh_tank_storage_volume_b = calc_vals["swh_tank_storage_volume_b"]
                modeled_efficiency_b = calc_vals["modeled_efficiency_b"]
                modeled_standby_loss_b = calc_vals["modeled_standby_loss_b"]
                expected_efficiency_metric_b = calc_vals["expected_efficiency_metric_b"]
                standby_loss_target_b = calc_vals["standby_loss_target_b"]

                return (
                        # Input power per volume is greater than the capacity per volume limit
                        swh_input_power_per_volume_b > CAPACITY_PER_VOLUME_LIMIT
                        # Electric resistance storage water heater with a storage volume in the range that produces an unreliable efficiency lookup
                        or (swh_tank_type_b == "ELECTRIC_RESISTANCE_STORAGE" and 55*ureg("gallon") < swh_tank_storage_volume_b <= 100*ureg("gallon"))
                        # Lookup values do not match any of the table entries
                        or (expected_efficiency_metric_b is None and standby_loss_target_b is None)
                        # Efficiency metric for the SWHEquip does not match the expected metric when only one of efficiency/SL is required
                        or (modeled_efficiency_b is None and modeled_standby_loss_b is None)
                        # Either efficiency metric for the SWHEquip does not match the expected values when both of efficiency/SL are required
                        or (expected_efficiency_metric_b and standby_loss_target_b and (modeled_efficiency_b is None or modeled_standby_loss_b is None))
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                pass

            def rule_check(self, context, calc_vals=None, data=None):
                pass
