from rct229.schema.schema_enums import SchemaEnums
from rct229.schema.config import ureg
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_F_2_fns import table_f_2_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_7_8_fns import table_7_8_lookup
from rct229.utils.compare_standard_val import std_le
from rct229.utils.std_comparisons import std_equal
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import CalcQ
from rct229.utils.assertions import assert_

EnergySourceOptions = SchemaEnums.schema_enums["EnergySourceOptions"]
SWHEfficiencyMetricOptions = SchemaEnums.schema_enums[
    "ServiceWaterHeatingEfficiencyMetricOptions"
]
SWHTankOptions = SchemaEnums.schema_enums["ServiceWaterHeaterTankOptions"]
DrawPatternOptions = SchemaEnums.schema_enums["DrawPatternOptions"]


CAPACITY_PER_VOLUME_LIMIT = 4000 * ureg("Btu/h/gallon")
INSTANTANEOUS_TYPES = [
    SWHTankOptions.CONSUMER_INSTANTANEOUS,
    SWHTankOptions.COMMERCIAL_INSTANTANEOUS,
    SWHTankOptions.RESIDENTIAL_DUTY_COMMERCIAL_INSTANTANEOUS,
]
STORAGE_TYPES = [SWHTankOptions.CONSUMER_STORAGE, SWHTankOptions.COMMERCIAL_STORAGE]
draw_pattern_enum_to_lookup_str_map = {
    DrawPatternOptions.VERY_SMALL: "Very small",
    DrawPatternOptions.LOW: "Low",
    DrawPatternOptions.MEDIUM: "Medium",
    DrawPatternOptions.HIGH: "High",
}


class PRM9012019Rule76q85(RuleDefinitionListIndexedBase):
    """Rule 10 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule76q85, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule76q85.RMDRule(),
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
            super(PRM9012019Rule76q85.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                each_rule=PRM9012019Rule76q85.RMDRule.SWHEquipRule(),
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
                super(PRM9012019Rule76q85.RMDRule.SWHEquipRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False,
                        BASELINE_0=True,
                        PROPOSED=False,
                    ),
                    required_fields={
                        "$": [
                            "tank",
                            "input_power",
                            "efficiency_metric_types",
                            "efficiency_metric_values",
                        ],
                        "tank": ["type", "storage_capacity"],
                    },
                    precision={
                        "swh_efficiency_b": {
                            "precision": 0.01,
                            "unit": "",
                        },
                        "swh_efficiency_uef_b": {
                            "precision": 0.0001,
                            "unit": "",
                        },
                        "swh_standby_loss_fraction_b": {
                            "precision": 0.01,
                            "unit": "",
                        },
                        "swh_standby_loss_energy_b": {
                            "precision": 1,
                            "unit": "Btu/h",
                        },
                    },
                )

            def get_calc_vals(self, context, data=None):
                swh_equip_b = context.BASELINE_0
                swh_tank_type_b = swh_equip_b["tank"]["type"]
                swh_tank_storage_volume_b = swh_equip_b["tank"]["storage_capacity"]
                swh_input_power_b = swh_equip_b["input_power"]
                swh_efficiency_b = dict(
                    zip(
                        swh_equip_b["efficiency_metric_types"],
                        swh_equip_b["efficiency_metric_values"],
                    )
                )
                swh_input_power_per_volume_b = (
                    swh_input_power_b / swh_tank_storage_volume_b
                )
                swh_fuel_type_b = swh_equip_b.get("heater_fuel_type")
                swh_setpoint_temperature_b = swh_equip_b.get("setpoint_temperature")

                # Determine draw_pattern_b
                draw_pattern_b = draw_pattern_enum_to_lookup_str_map.get(
                    swh_equip_b.get("draw_pattern")
                )
                if not draw_pattern_b:
                    first_hour_rating_b = swh_equip_b.get("first_hour_rating")
                    if first_hour_rating_b is not None:
                        if first_hour_rating_b < 18 * ureg("gallon"):
                            draw_pattern_b = draw_pattern_enum_to_lookup_str_map[
                                DrawPatternOptions.VERY_SMALL
                            ]
                        elif first_hour_rating_b < 51 * ureg("gallon"):
                            draw_pattern_b = draw_pattern_enum_to_lookup_str_map[
                                DrawPatternOptions.LOW
                            ]
                        elif first_hour_rating_b < 75 * ureg("gallon"):
                            draw_pattern_b = draw_pattern_enum_to_lookup_str_map[
                                DrawPatternOptions.MEDIUM
                            ]
                        else:
                            draw_pattern_b = draw_pattern_enum_to_lookup_str_map[
                                DrawPatternOptions.HIGH
                            ]
                # Overwrite draw pattern to empty string if the input power is greater than 105,000 Btu/h
                draw_pattern_b = (
                    "" if swh_input_power_b > 105000 * ureg("Btu/h") else draw_pattern_b
                )
                # Note: draw_pattern_b will be None if the SWH draw pattern is not defined and the first hour rating is not defined

                # efficiency_data data type should be None | List. If it is list, the maximum length is limited to 2 due to the dataset design.
                efficiency_data = None
                expected_efficiency_b = None
                expected_efficiency_metric_b = None
                standby_loss_target_b = None
                standby_loss_target_metric_b = None
                modeled_efficiency_b = None
                modeled_standby_loss_b = None
                standby_loss_is_estimated_b = False

                # Get Electric Storage Water Heater Efficiency Data
                if (
                    swh_fuel_type_b == EnergySourceOptions.ELECTRICITY
                    and swh_tank_type_b in STORAGE_TYPES
                ):
                    if swh_input_power_b < 12 * ureg("kW"):
                        # Lookup the expected efficiency from Appendix F-2
                        assert_(
                            draw_pattern_b is not None,
                            "Draw pattern must be defined for table F-2 lookup",
                        )
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
                elif (
                    swh_fuel_type_b
                    in [
                        EnergySourceOptions.NATURAL_GAS,
                        EnergySourceOptions.PROPANE,
                    ]
                    and swh_tank_type_b in STORAGE_TYPES
                ):
                    if swh_input_power_b <= 75000 * ureg("Btu/h"):
                        # Lookup the expected efficiency from Appendix F-2
                        assert_(
                            draw_pattern_b is not None,
                            "Draw pattern must be defined for table F-2 lookup",
                        )
                        efficiency_data = table_f_2_lookup(
                            "Gas storage water heater",
                            swh_tank_storage_volume_b,
                            draw_pattern_b,
                        )
                    else:
                        # Lookup the expected efficiency from Table 7.8
                        assert_(
                            draw_pattern_b is not None,
                            "Draw pattern must be defined for table 7-8 lookup",
                        )
                        if 75000 * ureg("Btu/h") < swh_input_power_b <= 105000 * ureg(
                            "Btu/h"
                        ) and (
                            (
                                swh_setpoint_temperature_b is not None
                                and swh_setpoint_temperature_b > 180 * ureg("degF")
                            )
                            or swh_tank_storage_volume_b > 120 * ureg("gallon")
                        ):
                            # Override the input power to follow Table 7-8 footnote d
                            efficiency_data = table_7_8_lookup(
                                "Gas storage water heater", 105001 * ureg("Btu/h"), ""
                            )
                        else:
                            efficiency_data = table_7_8_lookup(
                                "Gas storage water heater",
                                swh_input_power_b,
                                draw_pattern_b,
                            )
                        # Note: If the input power is greater than 105,000 Btu/h, there will be a thermal efficiency and standby loss target

                if efficiency_data:
                    to_remove = None
                    for efficiency in efficiency_data:
                        if "STANDBY" in efficiency["metric"]:
                            standby_loss_target_metric_b = efficiency["metric"]

                            # Always compute the target from the equation
                            standby_loss_target_b = eval(
                                efficiency["equation"],
                                {"__builtins__": None},
                                {
                                    "v": swh_tank_storage_volume_b.to(
                                        "gallon"
                                    ).magnitude,
                                    "q": swh_input_power_b.to("Btu/h").magnitude,
                                },
                            )

                            standby_loss_is_estimated_b = False  # Default

                            if (
                                standby_loss_target_metric_b
                                == SWHEfficiencyMetricOptions.STANDBY_LOSS_ENERGY
                            ):
                                modeled_standby_loss_b = swh_efficiency_b.get(
                                    SWHEfficiencyMetricOptions.STANDBY_LOSS_ENERGY
                                )
                                if modeled_standby_loss_b is None:
                                    modeled_standby_loss_fraction_b = swh_efficiency_b.get(
                                        SWHEfficiencyMetricOptions.STANDBY_LOSS_FRACTION
                                    )
                                    if modeled_standby_loss_fraction_b is not None:
                                        modeled_standby_loss_b = (
                                            modeled_standby_loss_fraction_b
                                            * 8.25
                                            * swh_tank_storage_volume_b.to(
                                                "gallon"
                                            ).magnitude
                                            * 70
                                        )
                                        standby_loss_is_estimated_b = True
                                    else:
                                        modeled_standby_loss_b = None
                            else:
                                modeled_standby_loss_b = swh_efficiency_b.get(
                                    standby_loss_target_metric_b
                                )

                            to_remove = efficiency
                            break

                    if to_remove is not None:
                        efficiency_data.remove(to_remove)

                    if len(efficiency_data) == 1:
                        expected_efficiency_metric_b = efficiency_data[0]["metric"]
                        expected_efficiency_b = eval(
                            efficiency_data[0]["equation"],
                            {"__builtins__": None},
                            {
                                "v": swh_tank_storage_volume_b.to("gallon").magnitude,
                                "q": swh_input_power_b.to("Btu/h").magnitude,
                            },
                        )
                        modeled_efficiency_b = swh_efficiency_b.get(
                            expected_efficiency_metric_b
                        )

                return {
                    "swh_fuel_type_b": swh_fuel_type_b,
                    "swh_tank_type_b": swh_tank_type_b,
                    "swh_input_power_b": swh_input_power_b,
                    "swh_tank_storage_volume_b": CalcQ(
                        "tank_volume", swh_tank_storage_volume_b
                    ),
                    "swh_setpoint_temperature_b": swh_setpoint_temperature_b,
                    "modeled_efficiency_b": modeled_efficiency_b,
                    "modeled_standby_loss_b": modeled_standby_loss_b,
                    "swh_input_power_per_volume_b": CalcQ(
                        "power_per_volume", swh_input_power_per_volume_b
                    ),
                    "expected_efficiency_b": expected_efficiency_b,
                    "expected_efficiency_metric_b": expected_efficiency_metric_b,
                    "standby_loss_target_b": standby_loss_target_b,
                    "standby_loss_target_metric_b": standby_loss_target_metric_b,
                    "standby_loss_is_estimated_b": standby_loss_is_estimated_b,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                swh_fuel_type_b = calc_vals["swh_fuel_type_b"]
                swh_tank_type_b = calc_vals["swh_tank_type_b"]
                swh_input_power_per_volume_b = calc_vals["swh_input_power_per_volume_b"]
                swh_tank_storage_volume_b = calc_vals["swh_tank_storage_volume_b"]
                modeled_efficiency_b = calc_vals["modeled_efficiency_b"]
                modeled_standby_loss_b = calc_vals["modeled_standby_loss_b"]
                expected_efficiency_metric_b = calc_vals["expected_efficiency_metric_b"]
                standby_loss_target_metric_b = calc_vals["standby_loss_target_metric_b"]
                standby_loss_is_estimated_b = calc_vals["standby_loss_is_estimated_b"]

                invalid_fuel_type = swh_fuel_type_b not in [
                    EnergySourceOptions.ELECTRICITY,
                    EnergySourceOptions.NATURAL_GAS,
                    EnergySourceOptions.PROPANE,
                ]
                return (
                    # The baseline water heater is of an Instantaneous type
                    swh_tank_type_b in INSTANTANEOUS_TYPES
                    and not invalid_fuel_type
                    # Input power per volume is greater than the capacity per volume limit
                    or swh_input_power_per_volume_b > CAPACITY_PER_VOLUME_LIMIT
                    and not invalid_fuel_type
                    # Electric resistance storage water heater with a storage volume in the range that produces an unreliable efficiency lookup
                    or (
                        swh_fuel_type_b == EnergySourceOptions.ELECTRICITY
                        and swh_tank_type_b in STORAGE_TYPES
                        and 55 * ureg("gallon")
                        < swh_tank_storage_volume_b
                        <= 100 * ureg("gallon")
                    )
                    # Lookup values do not match any of the table entries
                    or (
                        expected_efficiency_metric_b is None
                        and standby_loss_target_metric_b is None
                        and not invalid_fuel_type
                    )
                    # Efficiency metric for the SWHEquip does not match the expected metric when only one of efficiency/SL is required
                    or (
                        modeled_efficiency_b is None
                        and modeled_standby_loss_b is None
                        and not invalid_fuel_type
                    )
                    # Either efficiency metric for the SWHEquip does not match the expected values when both of efficiency/SL are required
                    or (
                        expected_efficiency_metric_b
                        and standby_loss_target_metric_b
                        and (
                            modeled_efficiency_b is None
                            or modeled_standby_loss_b is None
                        )
                        and not invalid_fuel_type
                    )
                    # The standby loss energy was required but not provided. Instead, standby loss fraction was provided
                    or standby_loss_is_estimated_b
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                swh_fuel_type_b = calc_vals["swh_fuel_type_b"]
                swh_tank_type_b = calc_vals["swh_tank_type_b"]
                swh_input_power_b = calc_vals["swh_input_power_b"]
                swh_tank_storage_volume_b = calc_vals["swh_tank_storage_volume_b"]
                swh_input_power_per_volume_b = calc_vals["swh_input_power_per_volume_b"]
                modeled_efficiency_b = calc_vals["modeled_efficiency_b"]
                modeled_standby_loss_b = calc_vals["modeled_standby_loss_b"]
                expected_efficiency_metric_b = calc_vals["expected_efficiency_metric_b"]
                standby_loss_target_b = calc_vals["standby_loss_target_b"]
                standby_loss_target_metric_b = calc_vals["standby_loss_target_metric_b"]
                standby_loss_is_estimated_b = calc_vals["standby_loss_is_estimated_b"]

                manual_check_msg = []

                if (
                    standby_loss_is_estimated_b
                    and modeled_standby_loss_b
                    and standby_loss_target_b
                    and modeled_standby_loss_b <= standby_loss_target_b
                ):
                    manual_check_msg.append(
                        "No standby loss was given. We have calculated an approximate standby loss using the given Standby Loss Fraction given the formula: Standby_Loss = Standby_Loss_Fraction * 8.25 * volume * 70. This calculated loss is less than or equal to the expected loss. Rule passes if assessor determines that this equation is appropriate for this project."
                    )

                elif standby_loss_is_estimated_b and modeled_standby_loss_b:
                    manual_check_msg.append(
                        "No standby loss was given. We have calculated an approximate standby loss using the given Standby Loss Fraction given the formula: Standby_Loss = Standby_Loss_Fraction * 8.25 * volume * 70. This calculated loss is greater than the expected loss. Rule fails unless the assessor determines that the standby loss is appropriate for this project."
                    )

                if swh_tank_type_b in INSTANTANEOUS_TYPES:
                    manual_check_msg.append(
                        "The baseline water heater is of an Instantaneous type. All service water heaters in the baseline should be storage water heaters, according to Table G3.1 #11 Baseline Building Performance column and Table G3.1.1-2. Consequently, the efficiency of the modeled water heater was not assessed."
                    )

                if swh_input_power_per_volume_b > CAPACITY_PER_VOLUME_LIMIT:
                    manual_check_msg.append(
                        "Capacity per volume exceeds the limit of 4000 (Btu/hr)/gallon given for storage water heaters in ASHRAE 90.1 Table 7.8."
                    )

                if (
                    swh_fuel_type_b == EnergySourceOptions.ELECTRICITY
                    and swh_tank_type_b in STORAGE_TYPES
                    and 55 * ureg("gallon")
                    < swh_tank_storage_volume_b
                    <= 100 * ureg("gallon")
                ):
                    manual_check_msg.append(
                        "The storage tank is between 55 and 100 gallons with a capacity <= 12kW (40945 btu/hr). The minimum efficiency requirements in 90.1 Section 7.4.2 point to 10 CFR 430 which provides a heat pump efficiency for water heaters in this capacity range which is not consistent with the efficiency of an electric resistance storage water heater which is the only electric SWH system type associated with the baseline for ASHRAE 90.1 Appendix G. Consequently, this rule was not able to be assessed for this service water heater. Note that the specific requirements of 10 CFR 430 can be found in ASHRAE 90.1 Appendix F Table F-2."
                    )

                elif (
                    swh_fuel_type_b == EnergySourceOptions.ELECTRICITY
                    and swh_tank_type_b in STORAGE_TYPES
                    and swh_input_power_b <= 12 * ureg("kW")
                    and (
                        swh_tank_storage_volume_b > 100 * ureg("gallon")
                        or swh_tank_storage_volume_b < 20 * ureg("gallon")
                    )
                ):
                    manual_check_msg.append(
                        "The storage tank volume falls outside the supported range based on the size categories in ASHRAE 90.1 Table 7.8 and in 10 CFR 430. Consequently, this rule was not assessed for this service water heater. Note that the specific requirements of 10 CFR 430 can be found in ASHRAE 90.1 Appendix F Table F-2."
                    )

                elif (
                    swh_fuel_type_b
                    in [
                        EnergySourceOptions.NATURAL_GAS,
                        EnergySourceOptions.PROPANE,
                    ]
                    and swh_tank_type_b in STORAGE_TYPES
                    and swh_input_power_b <= 75000 * ureg("Btu/h")
                    and (
                        swh_tank_storage_volume_b > 100 * ureg("gallon")
                        or swh_tank_storage_volume_b < 20 * ureg("gallon")
                    )
                ):
                    manual_check_msg.append(
                        "The storage tank volume falls outside the supported range based on the size categories in ASHRAE 90.1 Table 7.8 and in 10 CFR 430. Consequently, this rule was not assessed for this service water heater. Note that the specific requirements of 10 CFR 430 can be found in ASHRAE 90.1 Appendix F Table F-2."
                    )

                elif (
                    expected_efficiency_metric_b is None
                    and standby_loss_target_metric_b is None
                ):
                    manual_check_msg.append(
                        "The expected efficiency for this water heater could not be determined based on the provided details."
                    )

                if (
                    expected_efficiency_metric_b is not None
                    and modeled_efficiency_b is None
                ):
                    manual_check_msg.append(
                        f"Based on the provided details, {expected_efficiency_metric_b} is an expected efficiency metric for this water heater, however it was not provided. Note that the specific requirements of 10 CFR 430 can be found in ASHRAE 90.1 Appendix F Table F-2."
                    )

                if (
                    standby_loss_target_metric_b is not None
                    and modeled_standby_loss_b is None
                ):
                    manual_check_msg.append(
                        f"Based on the provided details, {standby_loss_target_metric_b} is an expected efficiency metric for this water heater, however it was not provided. Note that the specific requirements of 10 CFR 430 can be found in ASHRAE 90.1 Appendix F Table F-2."
                    )

                return "\n".join(manual_check_msg)

            def rule_check(self, context, calc_vals=None, data=None):
                swh_fuel_type_b = calc_vals["swh_fuel_type_b"]
                swh_tank_type_b = calc_vals["swh_tank_type_b"]
                modeled_efficiency_b = calc_vals["modeled_efficiency_b"]
                modeled_standby_loss_b = calc_vals["modeled_standby_loss_b"]
                expected_efficiency_b = calc_vals["expected_efficiency_b"]
                expected_efficiency_metric_b = calc_vals["expected_efficiency_metric_b"]
                standby_loss_target_b = calc_vals["standby_loss_target_b"]
                standby_loss_target_metric_b = calc_vals["standby_loss_target_metric_b"]

                invalid_fuel_type = swh_fuel_type_b not in [
                    EnergySourceOptions.ELECTRICITY,
                    EnergySourceOptions.NATURAL_GAS,
                    EnergySourceOptions.PROPANE,
                ]
                if invalid_fuel_type:
                    return False

                precision_entry = (
                    "swh_efficiency_b"
                    if expected_efficiency_metric_b
                    == SWHEfficiencyMetricOptions.THERMAL_EFFICIENCY
                    else "swh_efficiency_uef_b"
                )
                standby_loss_complies = (
                    (standby_loss_target_b is None)
                    or (
                        (
                            standby_loss_target_metric_b
                            == SWHEfficiencyMetricOptions.STANDBY_LOSS_FRACTION
                            and self.precision_comparison[
                                "swh_standby_loss_fraction_b"
                            ](modeled_standby_loss_b, standby_loss_target_b)
                        )
                        or (
                            standby_loss_target_b is not None
                            and modeled_standby_loss_b < standby_loss_target_b
                        )
                    )
                    or (
                        (
                            standby_loss_target_metric_b
                            == SWHEfficiencyMetricOptions.STANDBY_LOSS_ENERGY
                            and self.precision_comparison["swh_standby_loss_energy_b"](
                                # Schema specifies units as Watts
                                modeled_standby_loss_b * ureg("W"),
                                # Lookup table calculation results in Btu/h
                                standby_loss_target_b * ureg("Btu/h"),
                            )
                        )
                        or (
                            standby_loss_target_b is not None
                            and modeled_standby_loss_b * ureg("W")
                            < standby_loss_target_b * ureg("Btu/h")
                        )
                    )
                )

                return (
                    swh_tank_type_b in STORAGE_TYPES
                    and (
                        expected_efficiency_b is None
                        or self.precision_comparison[precision_entry](
                            modeled_efficiency_b, expected_efficiency_b
                        )
                    )
                    and standby_loss_complies
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                swh_fuel_type_b = calc_vals["swh_fuel_type_b"]
                swh_tank_type_b = calc_vals["swh_tank_type_b"]

                if (
                    swh_tank_type_b not in STORAGE_TYPES + INSTANTANEOUS_TYPES
                    or swh_fuel_type_b
                    not in [
                        EnergySourceOptions.ELECTRICITY,
                        EnergySourceOptions.NATURAL_GAS,
                        EnergySourceOptions.PROPANE,
                    ]
                ):
                    return f"Fuel type: {swh_fuel_type_b} is not a valid fuel type for a service water heating baseline system. According to ASHRAE 90.1 Table G3.1.1-2 service water heating equipment shall be either electric resistance or natural gas. According to ASHRAE 90.1 Table G3.1 #11 h, in cases where natural gas is specified as the baseline system, but there is no natural gas available on site, a propane system may be modeled."
                else:
                    return "The modeled efficiency or standby loss for the water heater does not match the expected values."

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                swh_tank_type_b = calc_vals["swh_tank_type_b"]
                modeled_efficiency_b = calc_vals["modeled_efficiency_b"]
                modeled_standby_loss_b = calc_vals["modeled_standby_loss_b"]
                expected_efficiency_b = calc_vals["expected_efficiency_b"]
                standby_loss_target_b = calc_vals["standby_loss_target_b"]

                standby_loss_complies = (
                    (standby_loss_target_b is None)
                    or (std_equal(modeled_standby_loss_b, standby_loss_target_b))
                    or (
                        standby_loss_target_b is not None
                        and std_le(
                            val=modeled_standby_loss_b, std_val=standby_loss_target_b
                        )
                    )
                )
                return (
                    swh_tank_type_b in STORAGE_TYPES
                    and (
                        expected_efficiency_b is None
                        or std_equal(modeled_efficiency_b, expected_efficiency_b)
                    )
                    and standby_loss_complies
                )
