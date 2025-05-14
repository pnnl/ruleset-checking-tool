from pydash import flat_map, map_
from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_hvac_sys_and_assoc_zones_largest_exhaust_source import (
    get_hvac_sys_and_assoc_zones_largest_exhaust_source,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_list_hvac_systems_associated_with_zone import (
    get_list_hvac_systems_associated_with_zone,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_
from rct229.utils.compare_standard_val import std_ge
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO, CalcQ
from rct229.utils.utility_functions import find_exactly_one_schedule

ENERGY_RECOVERY = SchemaEnums.schema_enums["EnergyRecoveryOptions"]
LIGHTING_SPACE = SchemaEnums.schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
VENTILATION_SPACE = SchemaEnums.schema_enums["VentilationSpaceOptions2019ASHRAE901"]
DEHUMIDIFICATION = SchemaEnums.schema_enums["DehumidificationOptions"]
ClimateZoneOption = SchemaEnums.schema_enums["ClimateZoneOptions2019ASHRAE901"]
OA_fraction_b_70 = 0.7
SUPPLY_AIRFLOW_5000CFM = 5000 * ureg("cfm")
REQ_HEATING_SETPOINT = 60 * ureg("degF")

APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_9B,
    HVAC_SYS.SYS_10,
]

APPLICABLE_CZ_ZONES = [
    ClimateZoneOption.CZ0A,
    ClimateZoneOption.CZ0B,
    ClimateZoneOption.CZ1A,
    ClimateZoneOption.CZ1B,
    ClimateZoneOption.CZ2A,
    ClimateZoneOption.CZ2B,
    ClimateZoneOption.CZ3A,
    ClimateZoneOption.CZ3B,
    ClimateZoneOption.CZ3C,
]


class PRM9012019Rule07w16(RuleDefinitionListIndexedBase):
    """Rule 21 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(PRM9012019Rule07w16, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            required_fields={
                "$": ["ruleset_model_descriptions"],
            },
            each_rule=PRM9012019Rule07w16.RMDRule(),
            index_rmd=BASELINE_0,
            id="19-21",
            description="Baseline systems with >= 5,000 CFM supply air and >= 70 %OA shall have energy recovery modeled in the baseline design model. The following exceptions apply:"
            "1. Systems serving spaces that are not cooled and that are heated to less than 60°F."
            "2. Systems exhausting toxic, flammable, or corrosive fumes or paint or dust. This exception shall only be used if exhaust air energy recovery is not used in the proposed design."
            "3. Commercial kitchen hoods (grease) classified as Type 1 by NFPA 96. This exception shall only be used if exhaust air energy recovery is not used in the proposed design."
            "4. Heating systems in Climate Zones 0 through 3."
            "5. Cooling systems in Climate Zones 3C, 4C, 5B, 5C, 6B, 7, and 8."
            "6. Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design."
            "7. Systems requiring dehumidification that employ energy recovery in series with the cooling coil. This exception shall only be used if exhaust air energy recovery and series-style energy recovery coils are not used in the proposed design.",
            ruleset_section_title="HVAC - General",
            standard_section="Section G3.1.2.10 and exceptions 1-7",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule07w16.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=PRM9012019Rule07w16.RMDRule.HVACRule(),
                index_rmd=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
                required_fields={
                    "$": ["weather"],
                    "weather": ["climate_zone"],
                },
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone = rmd_b["weather"]["climate_zone"]

            dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
                get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
            )

            baseline_hvac_system_dict = get_baseline_system_types(rmd_b)

            zone_data = {}
            for hvac_id_b in find_all(
                "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
                rmd_b,
            ):
                zone_data[hvac_id_b] = {
                    "serves_zones_with_systems_likely_exhausting_toxic_etc_p": False,
                    "serves_kitchen_space_p": False,
                    "all_lighting_space_types_defined_p": True,
                    "all_ventilation_space_types_defined_p": False,
                    "serves_zones_that_have_dehumid_heat_recovery_p": False,
                    "sys_type_heating_only_b": False,
                    "serves_zones_heated_to_60_or_higher_p": False,
                }

                for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                    hvac_id_b
                ]["zone_list"]:
                    spaces_p = find_all(
                        f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")].spaces[*]',
                        rmd_p,
                    )
                    assert_(spaces_p, f"No spaces found in zone id: {zone_id_b}.")

                    space_lighting_space_type_list_p = [
                        space.get("lighting_space_type", None) for space in spaces_p
                    ]

                    zone_data[hvac_id_b]["serves_kitchen_space_p"] = (
                        LIGHTING_SPACE.FOOD_PREPARATION_AREA
                        in space_lighting_space_type_list_p
                    )

                    zone_data[hvac_id_b]["all_lighting_space_types_defined_p"] = all(
                        space_lighting_space_type_list_p
                    )

                    space_ventilation_space_type_list_p = [
                        space.get("ventilation_space_type", None) for space in spaces_p
                    ]

                    zone_data[hvac_id_b][
                        "serves_zones_with_systems_likely_exhausting_toxic_etc_p"
                    ] = (
                        LIGHTING_SPACE.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                        in space_lighting_space_type_list_p
                    ) or (
                        VENTILATION_SPACE.MISCELLANEOUS_SPACES_MANUFACTURING_WHERE_HAZARDOUS_MATERIALS_ARE_USED_EXCLUDES_HEAVY_INDUSTRIAL_AND_CHEMICAL_PROCESSES
                        in space_ventilation_space_type_list_p
                    )

                    zone_data[hvac_id_b]["serves_kitchen_space_p"] = (
                        VENTILATION_SPACE.FOOD_AND_BEVERAGE_SERVICE_KITCHEN_COOKING
                        in space_ventilation_space_type_list_p
                    )

                    zone_data[hvac_id_b]["all_ventilation_space_types_defined_p"] = all(
                        space_ventilation_space_type_list_p
                    )

                    for hvac_id_p in get_list_hvac_systems_associated_with_zone(
                        rmd_p, zone_id_b
                    ):
                        hvac_p = find_one(
                            f'$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*][?(@.id = "{hvac_id_p}")]',
                            rmd_p,
                        )

                        zone_data[hvac_id_b][
                            "serves_zones_that_have_dehumid_heat_recovery_p"
                        ] = (
                            find_one("$.cooling_system.dehumidification_type", hvac_p)
                            == DEHUMIDIFICATION.SERIES_HEAT_RECOVERY
                        )

                    zone_data[hvac_id_b].update(
                        get_hvac_sys_and_assoc_zones_largest_exhaust_source(
                            rmd_b, hvac_id_b
                        )
                    )

                zone_data[hvac_id_b]["sys_type_heating_only_b"] = any(
                    [
                        hvac_id_b in baseline_hvac_system_dict[applicable_sys_type]
                        for applicable_sys_type in APPLICABLE_SYS_TYPES
                    ]
                )

                thermostat_heating_setpoint_schedule_list = map_(
                    dict_of_zones_and_terminal_units_served_by_hvac_sys_b[hvac_id_b][
                        "zone_list"
                    ],
                    lambda zone_id: find_one(
                        f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id}")].thermostat_heating_setpoint_schedule',
                        rmd_p,
                    ),
                )

                assert_(
                    thermostat_heating_setpoint_schedule_list,
                    "No thermostat heating setpoint schedule found in zones.",
                )

                # use this to remove duplications
                thermostat_heating_setpoint_schedule_list = list(
                    set(thermostat_heating_setpoint_schedule_list)
                )
                # this flattens the 2d array to 1d array
                thermostat_heating_setpoint_list = flat_map(
                    thermostat_heating_setpoint_schedule_list,
                    lambda schedule_id: find_exactly_one_schedule(
                        rmd_p, schedule_id
                    ).get("hourly_value", [0]),
                )

                max_thermostat_heating_setpoint_schedule_p = max(
                    thermostat_heating_setpoint_list
                ) * ureg("degC")

                zone_data[hvac_id_b]["serves_zones_heated_to_60_or_higher_p"] = (
                    max_thermostat_heating_setpoint_schedule_p > REQ_HEATING_SETPOINT
                )

            return {
                "climate_zone": climate_zone,
                "zone_data": zone_data,
            }

        class HVACRule(RuleDefinitionBase):
            def __init__(self):
                super(PRM9012019Rule07w16.RMDRule.HVACRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=True
                    ),
                    required_fields={
                        "$": ["fan_system"],
                        "fan_system": [
                            "supply_fans",
                            "minimum_outdoor_airflow",
                            "maximum_outdoor_airflow",
                        ],
                    },
                    precision={
                        "OA_fraction_b": {
                            "precision": 0.01,
                        },
                        "supply_airflow_b": {"precision": 1, "unit": "cfm"},
                    },
                )

            def get_calc_vals(self, context, data=None):
                hvac_b = context.BASELINE_0
                hvac_p = context.PROPOSED
                hvac_id_b = hvac_b["id"]

                climate_zone_b = data["climate_zone"]
                ER_not_req_for_heating_sys_b = climate_zone_b in APPLICABLE_CZ_ZONES

                zone_data = data["zone_data"][hvac_id_b]
                serves_zones_with_systems_likely_exhausting_toxic_etc_p = zone_data[
                    "serves_zones_with_systems_likely_exhausting_toxic_etc_p"
                ]
                serves_kitchen_space_p = zone_data["serves_kitchen_space_p"]
                all_lighting_space_types_defined_p = zone_data[
                    "all_lighting_space_types_defined_p"
                ]
                all_ventilation_space_types_defined_p = zone_data[
                    "all_ventilation_space_types_defined_p"
                ]
                serves_zones_that_have_dehumid_heat_recovery_p = zone_data[
                    "serves_zones_that_have_dehumid_heat_recovery_p"
                ]
                sys_type_heating_only_b = zone_data["sys_type_heating_only_b"]
                serves_zones_heated_to_60_or_higher_p = zone_data[
                    "serves_zones_heated_to_60_or_higher_p"
                ]
                maximum_zone_exhaust_b = zone_data["maximum_zone_exhaust"]
                num_hvac_exhaust_fans_b = zone_data["num_hvac_exhaust_fans"]
                hvac_fan_sys_exhaust_sum_b = zone_data["hvac_fan_sys_exhaust_sum"]
                maximum_hvac_exhaust_b = zone_data["maximum_hvac_exhaust"]

                fan_sys_b = hvac_b["fan_system"]

                supply_airflow_b = sum(
                    [
                        supply_fan_b.get("design_airflow", ZERO.FLOW)
                        for supply_fan_b in fan_sys_b["supply_fans"]
                    ]
                )

                min_outdoor_airflow_b = fan_sys_b["minimum_outdoor_airflow"]
                max_outdoor_airflow_b = fan_sys_b["maximum_outdoor_airflow"]

                OA_fraction_b = (
                    min_outdoor_airflow_b / supply_airflow_b
                    if supply_airflow_b != ZERO.FLOW
                    else 0.0
                )

                ER_modeled_b = find_one(
                    "$.fan_system.air_energy_recovery.energy_recovery_operation",
                    hvac_b,
                ) not in (
                    None,
                    ENERGY_RECOVERY.NONE,
                )

                ER_modeled_p = find_one(
                    "$.fan_system.air_energy_recovery.energy_recovery_operation",
                    hvac_p,
                ) not in (
                    None,
                    ENERGY_RECOVERY.NONE,
                )

                exception_1_applies = (
                    sys_type_heating_only_b
                    and not serves_zones_heated_to_60_or_higher_p
                )
                exception_2_applies = (
                    not ER_modeled_p
                    and serves_zones_with_systems_likely_exhausting_toxic_etc_p
                )
                exception_6_applies = (
                    not ER_modeled_p
                    and max(hvac_fan_sys_exhaust_sum_b, maximum_zone_exhaust_b)
                    < 0.75 * max_outdoor_airflow_b
                )
                exception_7_applies = (
                    not ER_modeled_p and serves_zones_that_have_dehumid_heat_recovery_p
                )

                return {
                    "climate_zone_b": climate_zone_b,
                    "ER_not_req_for_heating_sys_b": ER_not_req_for_heating_sys_b,
                    "serves_zones_with_systems_likely_exhausting_toxic_etc_p": serves_zones_with_systems_likely_exhausting_toxic_etc_p,
                    "serves_kitchen_space_p": serves_kitchen_space_p,
                    "all_lighting_space_types_defined_p": all_lighting_space_types_defined_p,
                    "all_ventilation_space_types_defined_p": all_ventilation_space_types_defined_p,
                    "serves_zones_that_have_dehumid_heat_recovery_p": serves_zones_that_have_dehumid_heat_recovery_p,
                    "sys_type_heating_only_b": sys_type_heating_only_b,
                    "hvac_fan_sys_exhaust_sum_b": hvac_fan_sys_exhaust_sum_b,
                    "maximum_zone_exhaust_b": maximum_zone_exhaust_b,
                    "num_hvac_exhaust_fans_b": num_hvac_exhaust_fans_b,
                    "maximum_hvac_exhaust_b": maximum_hvac_exhaust_b,
                    "supply_airflow_b": CalcQ("air_flow_rate", supply_airflow_b),
                    "min_outdoor_airflow_b": CalcQ(
                        "air_flow_rate", min_outdoor_airflow_b
                    ),
                    "OA_fraction_b": OA_fraction_b,
                    "ER_modeled_b": ER_modeled_b,
                    "ER_modeled_p": ER_modeled_p,
                    "max_outdoor_airflow_b": max_outdoor_airflow_b,
                    "exception_1_applies": exception_1_applies,
                    "exception_2_applies": exception_2_applies,
                    "exception_6_applies": exception_6_applies,
                    "exception_7_applies": exception_7_applies,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                OA_fraction_b = calc_vals[
                    "OA_fraction_b"
                ].magnitude  # .magnitude is because `OA_fraction_b` is a `dimensionless` unit in pint
                supply_airflow_b = calc_vals["supply_airflow_b"]
                ER_modeled_b = calc_vals["ER_modeled_b"]
                ER_modeled_p = calc_vals["ER_modeled_p"]
                serves_kitchen_space_p = calc_vals["serves_kitchen_space_p"]
                max_outdoor_airflow_b = calc_vals["max_outdoor_airflow_b"]
                num_hvac_exhaust_fans_b = calc_vals["num_hvac_exhaust_fans_b"]
                hvac_fan_sys_exhaust_sum_b = calc_vals["hvac_fan_sys_exhaust_sum_b"]
                maximum_hvac_exhaust_b = calc_vals["maximum_hvac_exhaust_b"]

                return (
                    (
                        OA_fraction_b > OA_fraction_b_70
                        or self.precision_comparison["OA_fraction_b"](
                            OA_fraction_b,
                            OA_fraction_b_70,
                        )
                    )
                    and (
                        supply_airflow_b > SUPPLY_AIRFLOW_5000CFM
                        or self.precision_comparison["supply_airflow_b"](
                            supply_airflow_b,
                            SUPPLY_AIRFLOW_5000CFM,
                        )
                    )
                    and not ER_modeled_b
                ) and (
                    # Case 7
                    (not ER_modeled_p and serves_kitchen_space_p)
                    or
                    # Case 8
                    (
                        num_hvac_exhaust_fans_b > 1
                        and max(hvac_fan_sys_exhaust_sum_b, maximum_hvac_exhaust_b)
                        < 0.75 * max_outdoor_airflow_b
                    )
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                hvac_b = context.BASELINE_0
                hvac_id_b = hvac_b["id"]

                ER_modeled_p = calc_vals["ER_modeled_p"]
                serves_kitchen_space_p = calc_vals["serves_kitchen_space_p"]

                if not ER_modeled_p and serves_kitchen_space_p:
                    UNDETERMINED_MSG = f"The baseline system {hvac_id_b} supply air cfm >= 5,000 CFM and the OA fraction is >= 70 %OA, per G3.1.2.10 exhaust air energy recovery is required to be modeled in the baseline and it has not been modeled. However, the system serves kitchen type spaces and exception 3 may be applicable which is that commercial kitchen hoods (grease) classified as Type 1 by NFPA 96 shall not require exhaust air energy recovery to be modeled if exhaust air energy recovery is not used in the proposed design (note that it has not modeled in the proposed). Conduct manual check to determine if exception 3 is applicable."
                else:
                    UNDETERMINED_MSG = f"Exhaust air energy recovery was not modeled in the baseline when the OA fraction is greater or equal to 70% and the supply cfm is greater or equal to 5,000 cfm. However, it appears that Section 90.1 G3.1.2.10 Exception 6 may be applicable which states, 'Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design.'. There are multilple exhaust fans associated with the hvac system and therefore this could not be assessed as the configuration is unknown. Conduct manual check to determine if this exception applies. If not, then fail."

                return UNDETERMINED_MSG

            def rule_check(self, context, calc_vals=None, data=None):
                OA_fraction_b = calc_vals[
                    "OA_fraction_b"
                ].magnitude  # .magnitude is because `OA_fraction_b` is a `dimensionless` unit in pint
                supply_airflow_b = calc_vals["supply_airflow_b"]
                ER_modeled_b = calc_vals["ER_modeled_b"]
                exception_1_applies = calc_vals["exception_1_applies"]
                exception_2_applies = calc_vals["exception_2_applies"]
                exception_6_applies = calc_vals["exception_6_applies"]
                exception_7_applies = calc_vals["exception_7_applies"]
                ER_not_req_for_heating_sys_b = calc_vals["ER_not_req_for_heating_sys_b"]
                sys_type_heating_only_b = calc_vals["sys_type_heating_only_b"]
                all_lighting_space_types_defined_p = calc_vals[
                    "all_lighting_space_types_defined_p"
                ]
                all_ventilation_space_types_defined_p = calc_vals[
                    "all_ventilation_space_types_defined_p"
                ]
                ER_modeled_p = calc_vals["ER_modeled_p"]

                return (
                    (
                        (
                            OA_fraction_b > OA_fraction_b_70
                            or self.precision_comparison["OA_fraction_b"](
                                OA_fraction_b,
                                OA_fraction_b_70,
                            )
                        )
                        and (
                            supply_airflow_b > SUPPLY_AIRFLOW_5000CFM
                            or self.precision_comparison["supply_airflow_b"](
                                supply_airflow_b,
                                SUPPLY_AIRFLOW_5000CFM,
                            )
                        )
                        and (
                            # CASE 1
                            (ER_modeled_b)
                            or
                            # CASE 2
                            (exception_1_applies)
                            or
                            # CASE 3
                            (exception_2_applies)
                            or
                            # CASE 4
                            (ER_not_req_for_heating_sys_b and sys_type_heating_only_b)
                            or
                            # CASE 5
                            (exception_6_applies)
                            or
                            # CASE 6
                            (exception_7_applies)
                        )
                    )
                    or (
                        # CASE 9 and 10
                        (
                            OA_fraction_b < OA_fraction_b_70
                            or supply_airflow_b < SUPPLY_AIRFLOW_5000CFM
                        )
                    )
                    or
                    # Case 11
                    (
                        (
                            all_lighting_space_types_defined_p
                            and all_ventilation_space_types_defined_p
                        )
                        or ER_modeled_p
                    )
                )

            def is_tolerance_fail(self, context, calc_vals=None, data=None):
                OA_fraction_b = calc_vals[
                    "OA_fraction_b"
                ].magnitude  # .magnitude is because `OA_fraction_b` is a `dimensionless` unit in pint
                supply_airflow_b = calc_vals["supply_airflow_b"]
                ER_modeled_b = calc_vals["ER_modeled_b"]
                exception_1_applies = calc_vals["exception_1_applies"]
                exception_2_applies = calc_vals["exception_2_applies"]
                exception_6_applies = calc_vals["exception_6_applies"]
                exception_7_applies = calc_vals["exception_7_applies"]
                ER_not_req_for_heating_sys_b = calc_vals["ER_not_req_for_heating_sys_b"]
                sys_type_heating_only_b = calc_vals["sys_type_heating_only_b"]
                all_lighting_space_types_defined_p = calc_vals[
                    "all_lighting_space_types_defined_p"
                ]
                all_ventilation_space_types_defined_p = calc_vals[
                    "all_ventilation_space_types_defined_p"
                ]
                ER_modeled_p = calc_vals["ER_modeled_p"]

                return (
                    (
                        (std_ge(val=OA_fraction_b, std_val=OA_fraction_b_70))
                        and (
                            std_ge(val=supply_airflow_b, std_val=SUPPLY_AIRFLOW_5000CFM)
                        )
                        and (
                            # CASE 1
                            (ER_modeled_b)
                            or
                            # CASE 2
                            (exception_1_applies)
                            or
                            # CASE 3
                            (exception_2_applies)
                            or
                            # CASE 4
                            (ER_not_req_for_heating_sys_b and sys_type_heating_only_b)
                            or
                            # CASE 5
                            (exception_6_applies)
                            or
                            # CASE 6
                            (exception_7_applies)
                        )
                    )
                    or (
                        # CASE 9 and 10
                        (
                            OA_fraction_b < OA_fraction_b_70
                            or supply_airflow_b < SUPPLY_AIRFLOW_5000CFM
                        )
                    )
                    or
                    # Case 11
                    (
                        (
                            all_lighting_space_types_defined_p
                            and all_ventilation_space_types_defined_p
                        )
                        or ER_modeled_p
                    )
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                all_lighting_space_types_defined_p = calc_vals[
                    "all_lighting_space_types_defined_p"
                ]
                all_ventilation_space_types_defined_p = calc_vals[
                    "all_ventilation_space_types_defined_p"
                ]
                ER_modeled_p = calc_vals["ER_modeled_p"]

                return (
                    "Not all lighting or ventilation space types were defined in the RMD and therefore the potential applicability of exceptions 2 and 3 could not be fully assessed. Fail unless exceptions 2 and 3 are applicable. "
                    "Exception 2 is that systems exhausting toxic, flammable, or corrosive fumes or paint or dust shall not require exhaust air energy recovery to be modeled in the baseline if it is not included in the proposed design. Exception 3 is that commercial kitchen hoods (grease) classified as Type 1 by NFPA 96 shall not require exhaust air energy recovery to be modeled in the baseline if it is not included in the proposed design."
                    if not (
                        (
                            all_lighting_space_types_defined_p
                            and all_ventilation_space_types_defined_p
                        )
                        or ER_modeled_p
                    )
                    else ""
                )
