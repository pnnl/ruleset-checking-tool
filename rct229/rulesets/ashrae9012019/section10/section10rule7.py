from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_1_fns import table_g3_5_1_lookup
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_2_fns import (
    HeatPumpEquipmentType,
    RatingCondition,
    table_g3_5_2_lookup,
)
from rct229.rulesets.ashrae9012019.data_fns.table_G3_5_4_fns import (
    table_g3_5_4_lookup,
    EquipmentType,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_systems_5_6_serving_multiple_floors import (
    get_hvac_systems_5_6_serving_multiple_floors,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_zone_list_w_area_dict import (
    get_hvac_zone_list_w_area_by_rmd_dict,
)
from rct229.utils.assertions import assert_
from rct229.utils.pint_utils import CalcQ
from rct229.utils.std_comparisons import std_equal
from rct229.utils.utility_functions import find_exactly_one_zone

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_1B,
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_3B,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_5B,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_6B,
]

CAPACITY_LOW_THRESHOLD = 65000
TYPE_TO_ENUM_STRING_MAP = {
    HVAC_SYS.SYS_1: EquipmentType.PTAC_COOLING,
    HVAC_SYS.SYS_1B: EquipmentType.PTAC_COOLING,
    HVAC_SYS.SYS_2: EquipmentType.PTHP_COOLING,
}


class PRM9012019Rule34l50(RuleDefinitionListIndexedBase):
    """Rule 7 of ASHRAE 90.1-2019 Appendix G Section 10 (HVAC General)"""

    def __init__(self):
        super(PRM9012019Rule34l50, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule34l50.HVACRule(),
            index_rmd=BASELINE_0,
            id="10-7",
            description=(
                "Baseline shall be modeled with the COPnfcooling HVAC system efficiency per Tables G3.5.1-G3.5.6.  Where multiple HVAC zones or residential spaces are combined into a single thermal block the cooling efficiencies (for baseline HVAC System Types 3 and 4) shall be based on the equipment capacity of the thermal block divided by the number of HVAC zones or residential spaces."
            ),
            ruleset_section_title="HVAC General",
            standard_section="Section Table G3.5.1-G3.5.6 Performance Rating Method Minimum Efficiency Requirements",
            is_primary_rule=True,
            list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            rmd_context="ruleset_model_descriptions/0",
        )

    def is_applicable(self, context, data=None):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        baseline_sys_5_6_serve_more_than_one_flr_list = (
            get_hvac_systems_5_6_serving_multiple_floors(rmd_b)
        )
        # create a list containing all HVAC systems that are modeled in the rmd_b
        available_types_list_excl_5_6_multifloor = [
            system_type
            for system_type, system_ids in baseline_system_types_dict.items()
            if any(
                system_id not in baseline_sys_5_6_serve_more_than_one_flr_list
                for system_id in system_ids
            )
        ]

        return any(
            [
                available_type in APPLICABLE_SYS_TYPES
                for available_type in available_types_list_excl_5_6_multifloor
            ]
        )

    def create_data(self, context, data):
        rmd_b = context.BASELINE_0
        baseline_system_types_dict = get_baseline_system_types(rmd_b)
        baseline_sys_5_6_serve_more_than_one_flr_list = (
            get_hvac_systems_5_6_serving_multiple_floors(rmd_b)
        )
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
                system_type: [
                    system_id
                    for system_id in system_list
                    if system_id not in baseline_sys_5_6_serve_more_than_one_flr_list
                ]
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
            super(PRM9012019Rule34l50.HVACRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                required_fields={
                    "$": ["cooling_system"],
                    "cooling_system": [
                        "efficiency_metric_types",
                        "efficiency_metric_values",
                    ],
                },
            )

        def get_calc_vals(self, context, data=None):
            hvac_b = context.BASELINE_0
            cooling_system_b = hvac_b["cooling_system"]
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

            total_cool_capacity_b = cooling_system_b.get("rated_total_cool_capacity")
            if total_cool_capacity_b is None:
                total_cool_capacity_b = cooling_system_b.get(
                    "design_total_cool_capacity"
                )

            if total_cool_capacity_b is not None:
                total_cool_capacity_mag_b = total_cool_capacity_b.to("Btu/h").magnitude
            else:
                total_cool_capacity_mag_b = None

            if total_cool_capacity_b is not None and hvac_system_type_b in [
                HVAC_SYS.SYS_3,
                HVAC_SYS.SYS_3B,
                HVAC_SYS.SYS_4,
            ]:
                assert len(zone_list_b) == 1
                hvac_zone_aggregation_factor = zone_list_b[0].get("aggregation_factor")
                if hvac_zone_aggregation_factor is not None:
                    total_cool_capacity_mag_b = (
                        total_cool_capacity_mag_b / hvac_zone_aggregation_factor
                    )
                elif total_cool_capacity_mag_b >= CAPACITY_LOW_THRESHOLD:
                    is_zone_agg_factor_undefined_and_needed = True

            if hvac_system_type_b in [HVAC_SYS.SYS_1, HVAC_SYS.SYS_1B, HVAC_SYS.SYS_2]:
                expected_baseline_eff_data = table_g3_5_4_lookup(
                    TYPE_TO_ENUM_STRING_MAP[hvac_system_type_b]
                )
                most_conservative_eff_b = expected_baseline_eff_data[
                    "minimum_efficiency"
                ]

            elif total_cool_capacity_b is not None and hvac_system_type_b in [
                HVAC_SYS.SYS_3,
                HVAC_SYS.SYS_3B,
                HVAC_SYS.SYS_5,
                HVAC_SYS.SYS_5B,
                HVAC_SYS.SYS_6,
                HVAC_SYS.SYS_6B,
            ]:
                expected_baseline_eff_data = table_g3_5_1_lookup(
                    total_cool_capacity_mag_b
                )
                most_conservative_eff_b = expected_baseline_eff_data[
                    "most_conservative_efficiency"
                ]

            elif total_cool_capacity_b is not None:  # HVAC_SYS.SYS_4
                assert_(
                    hvac_system_type_b == HVAC_SYS.SYS_4,
                    f"System type {hvac_system_type_b} does not match any of the applicable system types: 1, 1B, 2, 3, 3B, 4, 5, 5B, 6, 6B",
                )
                expected_baseline_eff_data = table_g3_5_2_lookup(
                    HeatPumpEquipmentType.HEAT_PUMP_AIR_COOLED_COOLING,
                    RatingCondition.SINGLE_PACKAGE,
                    total_cool_capacity_mag_b,
                )
                most_conservative_eff_b = expected_baseline_eff_data[
                    "most_conservative_efficiency"
                ]

            else:  # total_cool_capacity_b is None and outcome is undetermined
                expected_baseline_eff_data = {
                    "minimum_efficiency": None,
                    "efficiency_metric": None,
                }
                most_conservative_eff_b = None

            expected_eff_b = expected_baseline_eff_data["minimum_efficiency"]
            expected_eff_metric_b = expected_baseline_eff_data["efficiency_metric"]
            modeled_efficiency_values = cooling_system_b["efficiency_metric_values"]
            modeled_efficiency_metrics = cooling_system_b["efficiency_metric_types"]

            modeled_efficiency_b = next(
                (
                    eff
                    for eff, metric in zip(
                        modeled_efficiency_values, modeled_efficiency_metrics
                    )
                    if metric == expected_eff_metric_b
                ),
                None,
            )

            return {
                "total_cool_capacity_b": CalcQ("capacity", total_cool_capacity_b),
                "is_zone_agg_factor_undefined_and_needed": is_zone_agg_factor_undefined_and_needed,
                "expected_baseline_eff_b": expected_eff_b,
                "most_conservative_eff_b": most_conservative_eff_b,
                "modeled_efficiency_b": modeled_efficiency_b,
            }

        def manual_check_required(self, context, calc_vals=None, data=None):
            total_cool_capacity_b = calc_vals["total_cool_capacity_b"]
            is_zone_agg_factor_undefined_and_needed = calc_vals[
                "is_zone_agg_factor_undefined_and_needed"
            ]

            return (
                total_cool_capacity_b is None or is_zone_agg_factor_undefined_and_needed
            )

        def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
            most_conservative_eff_b = calc_vals["most_conservative_eff_b"]
            modeled_efficiency_b = calc_vals["modeled_efficiency_b"]

            if self.precision_comparison(modeled_efficiency_b, most_conservative_eff_b):
                undetermined_msg = "The cooling capacity of the system could not be determined. Check if the modeled baseline DX cooling efficiency was established correctly based upon equipment capacity and type while accounting for the potential aggregation of zones. The modeled efficiency matches the capacity bracket in Appendix G efficiency tables with the highest efficiency (i.e., most conservative efficiency has been modeled)."
            else:
                undetermined_msg = "The cooling capacity of the system could not be determined. Check if the modeled baseline DX cooling efficiency was established correctly based upon equipment capacity and type while accounting for the potential aggregation of zones."

            return undetermined_msg

        def rule_check(self, context, calc_vals=None, data=None):
            expected_baseline_eff_b = calc_vals["expected_baseline_eff_b"]
            modeled_efficiency_b = calc_vals["modeled_efficiency_b"]
            return self.precision_comparison(
                modeled_efficiency_b, expected_baseline_eff_b
            )

        def is_tolerance_fail(self, context, calc_vals=None, data=None):
            expected_baseline_eff_b = calc_vals["expected_baseline_eff_b"]
            modeled_efficiency_b = calc_vals["modeled_efficiency_b"]
            return std_equal(expected_baseline_eff_b, modeled_efficiency_b)
