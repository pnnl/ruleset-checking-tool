from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_2_fns import (
    HeatPumpEquipmentType,
    RatingCondition,
    table_g3_5_2_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_4_fns import table_g3_5_4_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_5_fns import (
    GasHeatingEquipmentType,
    table_g3_5_5_lookup,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.utils.assertions import assert_
from rct229.utils.pint_utils import CalcQ
from rct229.utils.utility_functions import find_exactly_one_zone

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_3A,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_9,
]

SINGLE_EFF_SYS_TYPES = [
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_3A,
    HVAC_SYS.SYS_9,
]

MOST_CONSERVATIVE_HEATPUMP_SAMPLE = 134999
MOST_CONSERVATIVE_FURNACE_SAMPLE = 224999
HEATPUMP_CAPACITY_LOW_THRESHOLD = 65000
FURNACE_CAPACITY_LOW_THREHSOLD = 225000

MOST_CONSERVATIVE_MSG = "Check if the modeled baseline heating efficiency was established correctly based upon equipment capacity and type. The modeled efficiency matches the capacity bracket in Appendix G efficiency tables with the highest efficiency (i.e., most conservative efficiency has been modeled)."
UNDEFINED_LOW_TEMP_MSG = "The efficiency at Tdb 47F was modeled correctly; however the outcome is undetermined because the modeled efficiency at Tdb 17F was not defined. It is often the case that the Tdb 17F efficiency is captured in the model via the performance curves as opposed to an explicit efficiency value entry. If there is no explicit option to enter an efficiency value at Tdb 17F check that appropriate performance curves were modeled."
MOST_CONSERVATIVE_HP_HIGH_TEMP_MSG = "Check if the modeled baseline heating efficiency was established correctly based upon equipment capacity and type. The modeled efficiency at Tdb 47F was modeled with an efficiency per the capacity bracket in Appendix G efficiency tables with the highest efficiency (i.e., most conservative efficiency has been modeled). It is often the case that the Tdb 17F efficiency is captured in the model via the performance curves as opposed to an explicit efficiency value entry. If there is no explicit option to enter an efficiency value at Tdb 17F check that appropriate performance curves were modeled."


class PRM9012019Rule10p28(RuleDefinitionListIndexedBase):
    """Rule 14 of ASHRAE 90.1-2019 Appendix G Section 10 (HVAC General)"""

    def __init__(self):
        super(PRM9012019Rule10p28, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule10p28.HVACRule(),
            index_rmd=BASELINE_0,
            id="10-14",
            description=(
                "Baseline shall be modeled with the heating HVAC system efficiency per Tables G3.5.1-G3.5.6 (applies only to the heating efficiency of baseline furnaces and heat pumps). Where multiple HVAC zones or residential spaces are combined into a single thermal block the heating efficiencies (for baseline HVAC System Types 3 and 4) shall be based on the equipment capacity of the thermal block divided by the number of HVAC zones or residential spaces."
            ),
            ruleset_section_title="HVAC General",
            standard_section="Section G3.1.2.1 Equipment Efficiencies",
            is_primary_rule=True,
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmd_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_types_list = [
            hvac_type
            for hvac_type in baseline_system_types_dict
            if len(baseline_system_types_dict[hvac_type]) > 0
        ]
        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_types_list
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        baseline_system_zones_served_dict = {
            hvac_id: [
                find_exactly_one_zone(rmd_b, zone_id)
                for zone_id in hvac_data["zone_list"]
            ]
            for hvac_id, hvac_data in get_hvac_zone_list_w_area_by_rmd_dict(
                rmd_b
            ).items()
        }

        return {
            "baseline_system_types_dict": {
                system_type: [system_id for system_id in system_list]
                for system_type, system_list in baseline_system_types_dict.items()
                if system_type in APPLICABLE_SYS_TYPES and system_list
            },
            "baseline_system_zones_served_dict": baseline_system_zones_served_dict,
        }

    def list_filter(self, context_item, data):
        hvac_b = context_item.BASELINE_0
        baseline_system_types_dict = data["baseline_system_types_dict"]
        applicable_hvac_sys_ids = [
            hvac_id
            for sys_list in baseline_system_types_dict.values()
            for hvac_id in sys_list
        ]

        return hvac_b["id"] in applicable_hvac_sys_ids

    class HVACRule(RuleDefinitionBase):
        def __init__(self):
            super(PRM9012019Rule10p28.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["heating_system"],
                    "heating_system": [
                        "efficiency_metric_types",
                        "efficiency_metric_values",
                    ],
                },
                precision={
                    "modeled_high_temp_eff_b": {
                        "precision": 0.1,
                        "unit": "",
                    },
                    "modeled_low_temp_eff_b": {
                        "precision": 0.1,
                        "unit": "",
                    },
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            heating_system_b = hvac_b["heating_system"]
            baseline_system_types_dict_b = data["baseline_system_types_dict"]
            hvac_zone_list_w_area_dict_b = data["baseline_system_zones_served_dict"]
            zone_list_b = hvac_zone_list_w_area_dict_b[hvac_b["id"]]
            is_zone_agg_factor_undefined_and_needed = False

            hvac_system_type_b = next(
                (
                    system_type
                    for system_type, hvac_b_ids in baseline_system_types_dict_b.items()
                    if hvac_b["id"] in hvac_b_ids
                ),
                None,
            )

            if hvac_system_type_b in SINGLE_EFF_SYS_TYPES:
                total_capacity_b = heating_system_b.get("rated_capacity")

                if total_capacity_b is None:
                    total_capacity_b = heating_system_b.get("design_capacity")

            else:  # HVAC_SYS.SYS_4, cooling system required per 'is_baseline_system_4.py'
                cooling_system_b = hvac_b["cooling_system"]
                total_capacity_b = cooling_system_b.get("rated_total_cool_capacity")

                if total_capacity_b is None:
                    total_capacity_b = cooling_system_b.get(
                        "design_total_cool_capacity"
                    )

            if total_capacity_b is not None:
                total_capacity_mag_b = total_capacity_b.to("Btu/h").magnitude
            else:
                total_capacity_mag_b = None

            if total_capacity_b is not None and hvac_system_type_b in [
                HVAC_SYS.SYS_3,
                HVAC_SYS.SYS_3A,
                HVAC_SYS.SYS_4,
            ]:
                hvac_zone_aggregation_factor = zone_list_b[0].get("aggregation_factor")
                if hvac_zone_aggregation_factor is not None:
                    total_capacity_b = total_capacity_b / hvac_zone_aggregation_factor
                    total_capacity_mag_b = (
                        total_capacity_mag_b / hvac_zone_aggregation_factor
                    )

                elif (
                    hvac_zone_aggregation_factor is None
                    and hvac_system_type_b in [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A]
                    and total_capacity_mag_b >= FURNACE_CAPACITY_LOW_THREHSOLD
                ):
                    is_zone_agg_factor_undefined_and_needed = True

                elif (
                    hvac_zone_aggregation_factor is None
                    and hvac_system_type_b == HVAC_SYS.SYS_4
                    and total_capacity_mag_b >= HEATPUMP_CAPACITY_LOW_THRESHOLD
                ):
                    is_zone_agg_factor_undefined_and_needed = True

            if hvac_system_type_b == HVAC_SYS.SYS_2:
                expected_baseline_eff_data = [table_g3_5_4_lookup(hvac_system_type_b)]

            elif hvac_system_type_b in [HVAC_SYS.SYS_3, HVAC_SYS.SYS_3A]:
                if total_capacity_b is None:
                    expected_baseline_eff_data = table_g3_5_5_lookup(
                        GasHeatingEquipmentType.WARM_AIR_FURNACE_GAS_FIRED,
                        MOST_CONSERVATIVE_FURNACE_SAMPLE,
                    )
                else:
                    expected_baseline_eff_data = table_g3_5_5_lookup(
                        GasHeatingEquipmentType.WARM_AIR_FURNACE_GAS_FIRED,
                        total_capacity_mag_b,
                    )

            elif hvac_system_type_b == HVAC_SYS.SYS_9:
                if total_capacity_b is None:
                    expected_baseline_eff_data = table_g3_5_5_lookup(
                        GasHeatingEquipmentType.WARM_AIR_UNIT_HEATER_GAS_FIRED,
                        MOST_CONSERVATIVE_FURNACE_SAMPLE,
                    )
                else:
                    expected_baseline_eff_data = table_g3_5_5_lookup(
                        GasHeatingEquipmentType.WARM_AIR_UNIT_HEATER_GAS_FIRED,
                        total_capacity_mag_b,
                    )

            else:  # HVAC_SYS.SYS_4
                if total_capacity_b is None:
                    expected_baseline_eff_data = [
                        table_g3_5_2_lookup(
                            HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
                            RatingCondition.HIGH_TEMP,
                            MOST_CONSERVATIVE_HEATPUMP_SAMPLE,
                        ),
                        table_g3_5_2_lookup(
                            HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
                            RatingCondition.LOW_TEMP,
                            MOST_CONSERVATIVE_HEATPUMP_SAMPLE,
                        ),
                    ]

                elif total_capacity_mag_b < HEATPUMP_CAPACITY_LOW_THRESHOLD:
                    expected_baseline_eff_data = [
                        table_g3_5_2_lookup(
                            HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
                            RatingCondition.SINGLE_PACKAGE,
                            total_capacity_mag_b,
                        ),
                        # LOW-TEMP EFFICIENCY IS NOT USED FOR THE LOWEST CAPACITY RANGE FOR SYSTEM 4
                        # IT IS ONLY NEEDED FOR CONSISTENT DATA FORMAT
                        table_g3_5_2_lookup(
                            HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
                            RatingCondition.SINGLE_PACKAGE,
                            total_capacity_mag_b,
                        ),
                    ]

                else:
                    expected_baseline_eff_data = [
                        table_g3_5_2_lookup(
                            HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
                            RatingCondition.HIGH_TEMP,
                            total_capacity_mag_b,
                        ),
                        table_g3_5_2_lookup(
                            HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_HEATING,
                            RatingCondition.LOW_TEMP,
                            total_capacity_mag_b,
                        ),
                    ]

            modeled_effs_b = list(
                zip(
                    heating_system_b["efficiency_metric_values"],
                    heating_system_b["efficiency_metric_types"],
                )
            )

            if hvac_system_type_b in SINGLE_EFF_SYS_TYPES:
                expected_high_temp_eff_b = None
                expected_low_temp_eff_b = None
                modeled_high_temp_eff_b = None
                modeled_low_temp_eff_b = None

                expected_effs_b = [
                    (
                        expected_baseline_eff["minimum_efficiency"],
                        expected_baseline_eff["efficiency_metric"],
                    )
                    for expected_baseline_eff in expected_baseline_eff_data
                ]

                # Filter modeled efficiencies to only include those with the expected efficiency metrics
                modeled_effs_b = [
                    modeled_eff_b
                    for expected_eff_b in expected_effs_b
                    for modeled_eff_b in modeled_effs_b
                    if modeled_eff_b[1] == expected_eff_b[1]
                ]

                assert_(
                    len(modeled_effs_b) > 0,
                    "No modeled efficiencies were found with the expected efficiency metrics",
                )

                # Filter expected efficiencies to only include those with the modeled efficiency metrics
                expected_effs_b = [
                    expected_eff_b
                    for expected_eff_b in expected_effs_b
                    if expected_eff_b[1] in [eff[1] for eff in modeled_effs_b]
                ]

            else:
                expected_effs_b = []
                expected_high_temp_eff_b = expected_baseline_eff_data[0][
                    "minimum_efficiency"
                ]
                expected_high_temp_eff_metric_b = expected_baseline_eff_data[0][
                    "efficiency_metric"
                ]
                expected_low_temp_eff_b = expected_baseline_eff_data[1][
                    "minimum_efficiency"
                ]
                expected_low_temp_eff_metric_b = expected_baseline_eff_data[1][
                    "efficiency_metric"
                ]

                modeled_high_temp_eff_b = next(
                    (
                        eff
                        for eff, metric in modeled_effs_b
                        if metric == expected_high_temp_eff_metric_b
                    ),
                    None,
                )
                modeled_low_temp_eff_b = next(
                    (
                        eff
                        for eff, metric in modeled_effs_b
                        if metric == expected_low_temp_eff_metric_b
                    ),
                    None,
                )

            return {
                "hvac_system_type_b": hvac_system_type_b,
                "total_capacity_b": CalcQ("capacity", total_capacity_b),
                "is_zone_agg_factor_undefined_and_needed": is_zone_agg_factor_undefined_and_needed,
                "expected_effs_b": expected_effs_b,
                "modeled_effs_b": modeled_effs_b,
                "expected_high_temp_eff_b": expected_high_temp_eff_b,
                "modeled_high_temp_eff_b": modeled_high_temp_eff_b,
                "expected_low_temp_eff_b": expected_low_temp_eff_b,
                "modeled_low_temp_eff_b": modeled_low_temp_eff_b,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            hvac_system_type_b = calc_vals["hvac_system_type_b"]
            expected_effs_b = calc_vals["expected_effs_b"]
            expected_high_temp_eff_b = calc_vals["expected_high_temp_eff_b"]
            expected_low_temp_eff_b = calc_vals["expected_low_temp_eff_b"]
            modeled_effs_b = calc_vals["modeled_effs_b"]
            modeled_high_temp_eff_b = calc_vals["modeled_high_temp_eff_b"]
            modeled_low_temp_eff_b = calc_vals["modeled_low_temp_eff_b"]
            total_capacity_b = calc_vals["total_capacity_b"]
            is_zone_agg_factor_undefined_and_needed = calc_vals[
                "is_zone_agg_factor_undefined_and_needed"
            ]

            # Case 3, 4, 7 and 10 all satisfied here
            if (
                len(modeled_effs_b) > 0
                and len(expected_effs_b) > 0
                and all(
                    modeled_eff_b[0] == expected_eff_b[0]
                    for modeled_eff_b, expected_eff_b in zip(
                        modeled_effs_b, expected_effs_b
                    )
                )
                and total_capacity_b is None
                or is_zone_agg_factor_undefined_and_needed
            ):
                return True

            # Case 8 and 11 satisfied here
            if (
                hvac_system_type_b == HVAC_SYS.SYS_4
                and modeled_high_temp_eff_b is not None
                and self.precision_comparison["modeled_high_temp_eff_b"](
                    modeled_high_temp_eff_b.magnitude, expected_high_temp_eff_b
                )
                and modeled_low_temp_eff_b is not None
                and self.precision_comparison["modeled_low_temp_eff_b"](
                    modeled_low_temp_eff_b.magnitude, expected_low_temp_eff_b
                )
                and total_capacity_b is None
                or is_zone_agg_factor_undefined_and_needed
            ):
                return True

            # Case 6
            if (
                hvac_system_type_b == HVAC_SYS.SYS_4
                and modeled_high_temp_eff_b is not None
                and self.precision_comparison["modeled_high_temp_eff_b"](
                    modeled_high_temp_eff_b.magnitude, expected_high_temp_eff_b
                )
                and modeled_low_temp_eff_b is None
                and total_capacity_b is not None
                and not is_zone_agg_factor_undefined_and_needed
            ):
                return True

            # Case 9 and 12 satisfied here
            if (
                hvac_system_type_b == HVAC_SYS.SYS_4
                and modeled_high_temp_eff_b is not None
                and self.precision_comparison["modeled_high_temp_eff_b"](
                    modeled_high_temp_eff_b.magnitude, expected_high_temp_eff_b
                )
                and modeled_low_temp_eff_b is None
                and total_capacity_b is None
                or is_zone_agg_factor_undefined_and_needed
            ):
                return True

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            hvac_system_type_b = calc_vals["hvac_system_type_b"]
            expected_effs_b = calc_vals["expected_effs_b"]
            expected_high_temp_eff_b = calc_vals["expected_high_temp_eff_b"]
            modeled_effs_b = calc_vals["modeled_effs_b"]
            modeled_high_temp_eff_b = calc_vals["modeled_high_temp_eff_b"]
            modeled_low_temp_eff_b = calc_vals["modeled_low_temp_eff_b"]
            total_capacity_b = calc_vals["total_capacity_b"]
            is_zone_agg_factor_undefined_and_needed = calc_vals[
                "is_zone_agg_factor_undefined_and_needed"
            ]

            # IF OUTCOME IS UNDETERMINED AND THESE CONDITIONS ARE TRUE, THE MOST CONSERVATIVE EFFICIENCY WAS MODELED
            # Cases 3, 4, 7, 10
            if (
                len(modeled_effs_b) > 0
                and len(expected_effs_b) > 0
                and all(
                    modeled_eff_b[0] == expected_eff_b[0]
                    for modeled_eff_b, expected_eff_b in zip(
                        modeled_effs_b, expected_effs_b
                    )
                )
            ):
                return MOST_CONSERVATIVE_MSG

            # Case 6
            elif (
                hvac_system_type_b == HVAC_SYS.SYS_4
                and (
                    modeled_high_temp_eff_b is None
                    or self.precision_comparison["modeled_high_temp_eff_b"](
                        modeled_high_temp_eff_b.magnitude, expected_high_temp_eff_b
                    )
                )
                and modeled_low_temp_eff_b is None
                and total_capacity_b is not None
                and not is_zone_agg_factor_undefined_and_needed
            ):
                return UNDEFINED_LOW_TEMP_MSG

            # IF OUTCOME IS UNDETERMINED AND THESE CONDITIONS ARE TRUE, THE MOST CONSERVATIVE HIGH-TEMP EFFICIENCY WAS MODELED
            # Cases 8, 9, 11, 12
            elif (
                hvac_system_type_b == HVAC_SYS.SYS_4
                and modeled_high_temp_eff_b is not None
                and self.precision_comparison["modeled_high_temp_eff_b"](
                    modeled_high_temp_eff_b.magnitude, expected_high_temp_eff_b
                )
                and total_capacity_b is None
            ):
                return MOST_CONSERVATIVE_HP_HIGH_TEMP_MSG

        def rule_check(self, context, calc_vals=None, data=None):
            hvac_system_type_b = calc_vals["hvac_system_type_b"]
            total_capacity_b = calc_vals["total_capacity_b"]
            is_zone_agg_factor_undefined_and_needed = calc_vals[
                "is_zone_agg_factor_undefined_and_needed"
            ]

            if hvac_system_type_b in SINGLE_EFF_SYS_TYPES:
                expected_effs_b = calc_vals["expected_effs_b"]
                modeled_effs_b = calc_vals["modeled_effs_b"]

                # Case 1 and 2 both satisfied here
                return (
                    all(
                        modeled_eff_b == expected_eff_b
                        for modeled_eff_b, expected_eff_b in zip(
                            modeled_effs_b, expected_effs_b
                        )
                    )
                    and total_capacity_b is not None
                    and not is_zone_agg_factor_undefined_and_needed
                )

            else:  # HVAC_SYS.SYS_4
                expected_high_temp_eff_b = calc_vals["expected_high_temp_eff_b"]
                modeled_high_temp_eff_b = calc_vals["modeled_high_temp_eff_b"]
                expected_low_temp_eff_b = calc_vals["expected_low_temp_eff_b"]
                modeled_low_temp_eff_b = calc_vals["modeled_low_temp_eff_b"]

                # Case 5
                return (
                    modeled_high_temp_eff_b is not None
                    and self.precision_comparison["modeled_high_temp_eff_b"](
                        modeled_high_temp_eff_b.magnitude, expected_high_temp_eff_b
                    )
                    and self.precision_comparison["modeled_low_temp_eff_b"](
                        modeled_low_temp_eff_b.magnitude, expected_low_temp_eff_b
                    )
                    and total_capacity_b is not None
                    and not is_zone_agg_factor_undefined_and_needed
                )
