from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.user_baseline_proposed_vals import UserBaselineProposedVals
from rct229.rulesets.ashrae9012019.data.schema_enums import schema_enums
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
from rct229.utils.assertions import assert_
from rct229.utils.jsonpath_utils import find_all, find_one
from rct229.utils.pint_utils import ZERO, CalcQ

ENERGY_RECOVERY = schema_enums["EnergyRecoveryOptions"]
LIGHTING_SPACE = schema_enums["LightingSpaceOptions2019ASHRAE901TG37"]
VENTILATION_SPACE = schema_enums["VentilationSpaceOptions2019ASHRAE901"]
DEHUMIDIFICATION = schema_enums["DehumidificationOptions"]
ClimateZoneOption = schema_enums["ClimateZoneOptions2019ASHRAE901"]
OA_fraction_b_70 = 0.7
SUPPLY_AIRFLOW_5000CFM = 5000 * ureg("cfm")
REQ_HEATING_SETPOINT = 60 * ureg("degF")
CASE11_FAIL_MSG = "Not all lighting or ventilation space types were defined in the RMD and therefore the potential applicability of exceptions 2 and 3 could not be fully assessed. Fail unless exceptions 2 and 3 are applicable. Exception 2 is that systems exhausting toxic, flammable, or corrosive fumes or paint or dust shall not require exhaust air energy recovery to be modeled in the baseline if it is not included in the proposed design. Exception 3 is that commercial kitchen hoods (grease) classified as Type 1 by NFPA 96 shall not require exhaust air energy recovery to be modeled in the baseline if it is not included in the proposed design."


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


class Section19Rule21(RuleDefinitionListIndexedBase):
    """Rule 21 of ASHRAE 90.1-2019 Appendix G Section 19 (HVAC - General)"""

    def __init__(self):
        super(Section19Rule21, self).__init__(
            rmrs_used=UserBaselineProposedVals(False, True, True),
            required_fields={
                "$": ["weather", "ruleset_model_descriptions"],
                "weather": ["climate_zone"],
            },
            each_rule=Section19Rule21.RMDRule(),
            index_rmr="baseline",
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
            data_items={"climate_zone": ("baseline", "weather/climate_zone")},
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section19Rule21.RMDRule, self).__init__(
                rmrs_used=UserBaselineProposedVals(False, True, True),
                each_rule=Section19Rule21.RMDRule.HVACRule(),
                index_rmr="baseline",
                list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.baseline
            rmd_p = context.proposed

            dict_of_zones_and_terminal_units_served_by_hvac_sys_b = (
                get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
            )

            baseline_hvac_system_dict = get_baseline_system_types(rmd_b)

            zone_data = {}
            hvac_systems_and_assoc_zones_largest_exhaust_source = {}
            for hvac_id_b in find_all(
                "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
                rmd_b,
            ):
                zone_data[hvac_id_b] = {
                    "serves_zones_with_systems_likely_exhausting_toxic_etc": False,
                    "serves_kitchen_space": False,
                    "all_lighting_space_types_defined": True,
                    "all_ventilation_space_types_defined": False,
                }

                for zone_id_b in dict_of_zones_and_terminal_units_served_by_hvac_sys_b[
                    hvac_id_b
                ]["zone_list"]:
                    space_p = find_one(
                        f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id_b}")].spaces[*]',
                        rmd_p,
                    )

                    if space_p is not None and space_p.get(
                        "lighting_space_type", False
                    ):
                        lighting_space_type_p = space_p["lighting_space_type"]
                        if (
                            lighting_space_type_p
                            == LIGHTING_SPACE.LABORATORY_EXCEPT_IN_OR_AS_A_CLASSROOM
                        ):
                            zone_data[hvac_id_b][
                                "serves_zones_with_systems_likely_exhausting_toxic_etc"
                            ] = True

                        if (
                            lighting_space_type_p
                            == LIGHTING_SPACE.FOOD_PREPARATION_AREA
                        ):
                            zone_data[hvac_id_b]["serves_kitchen_space"] = True

                    else:
                        zone_data[hvac_id_b]["all_lighting_space_types_defined"] = False

                    if space_p is not None and space_p.get(
                        "ventilation_space_type", False
                    ):
                        ventilation_space_type_p = space_p["ventilation_space_type"]
                        if (
                            ventilation_space_type_p
                            == VENTILATION_SPACE.MISCELLANEOUS_SPACES_MANUFACTURING_WHERE_HAZARDOUS_MATERIALS_ARE_USED_EXCLUDES_HEAVY_INDUSTRIAL_AND_CHEMICAL_PROCESSES
                        ):
                            zone_data[hvac_id_b][
                                "serves_zones_with_systems_likely_exhausting_toxic_etc"
                            ] = True

                        if (
                            ventilation_space_type_p
                            == VENTILATION_SPACE.FOOD_AND_BEVERAGE_SERVICE_KITCHEN_COOKING
                        ):
                            zone_data[hvac_id_b]["serves_kitchen_space"] = True
                    else:
                        zone_data[hvac_id_b][
                            "all_ventilation_space_types_defined"
                        ] = False

                    for hvac_id_p in get_list_hvac_systems_associated_with_zone(
                        rmd_p, zone_id_b
                    ):
                        hvac_p = find_one(
                            f'$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*][?(@.id = "{hvac_id_p}")]',
                            rmd_p,
                        )
                        ER_modeled_p = find_one(
                            "$.fan_system.air_energy_recovery.energy_recovery_type",
                            hvac_p,
                        ) in (
                            ENERGY_RECOVERY.SENSIBLE_HEAT_EXHANGE,
                            ENERGY_RECOVERY.ENTHALPY_HEAT_EXHANGE,
                            ENERGY_RECOVERY.SENSIBLE_HEAT_WHEEL,
                            ENERGY_RECOVERY.ENTHALPY_HEAT_WHEEL,
                            ENERGY_RECOVERY.HEAT_PIPE,
                            ENERGY_RECOVERY.OTHER,
                        )

                        serves_zones_that_have_dehumid_heat_recovery = (
                            find_one("$.cooling_system.dehumidification_type", hvac_p)
                            == DEHUMIDIFICATION.SERIES_HEAT_RECOVERY
                        )

                    hvac_systems_and_assoc_zones_largest_exhaust_source[
                        hvac_id_b
                    ] = get_hvac_sys_and_assoc_zones_largest_exhaust_source(
                        rmd_b, hvac_id_b
                    )

                sys_type_heating_only = any(
                    [
                        hvac_id_b in baseline_hvac_system_dict[applicable_sys_type]
                        for applicable_sys_type in APPLICABLE_SYS_TYPES
                    ]
                )

            try:
                max_thermostat_heating_setpoint_schedule_p = max(
                    [
                        max(thermostat_schedule)
                        * ureg(
                            "degC"
                        )  # TODO: make sure this unit is degC. The current schema (v 0.0.29) doesn't specify the unit specifically
                        for thermostat_schedule_id in find_all(
                            "$.buildings[*].building_segments[*].zones[*].thermostat_heating_setpoint_schedule",
                            rmd_p,
                        )
                        for thermostat_schedule in find_all(
                            f'$.schedules[*][?(@.id = "{thermostat_schedule_id}")].hourly_values',
                            rmd_p,
                        )
                    ]
                )
            except ValueError:
                max_thermostat_heating_setpoint_schedule_p = ZERO.TEMPERATURE

            serves_zones_heated_to_60_or_higher_p = (
                max_thermostat_heating_setpoint_schedule_p > REQ_HEATING_SETPOINT
            )

            return {
                "zone_data": zone_data,
                "ER_modeled_p": ER_modeled_p,
                "serves_zones_that_have_dehumid_heat_recovery": serves_zones_that_have_dehumid_heat_recovery,
                "sys_type_heating_only": sys_type_heating_only,
                "hvac_systems_and_assoc_zones_largest_exhaust_source": hvac_systems_and_assoc_zones_largest_exhaust_source,
                "serves_zones_heated_to_60_or_higher_p": serves_zones_heated_to_60_or_higher_p,
            }

        class HVACRule(RuleDefinitionBase):
            def __init__(self):
                super(Section19Rule21.RMDRule.HVACRule, self).__init__(
                    rmrs_used=UserBaselineProposedVals(False, True, True),
                    required_fields={
                        "$": ["fan_system"],
                        "fan_system": [
                            "supply_fans",
                            "minimum_outdoor_airflow",
                            "maximum_outdoor_airflow",
                        ],
                    },
                )

            def get_calc_vals(self, context, data=None):
                hvac_b = context.baseline
                hvac_id_b = hvac_b["id"]

                climate_zone = data["climate_zone"]
                ER_not_req_for_heating_sys = climate_zone in APPLICABLE_CZ_ZONES

                zone_data = data["zone_data"][hvac_id_b]
                serves_zones_with_systems_likely_exhausting_toxic_etc = zone_data[
                    "serves_zones_with_systems_likely_exhausting_toxic_etc"
                ]
                serves_kitchen_space = zone_data["serves_kitchen_space"]
                all_lighting_space_types_defined = zone_data[
                    "all_lighting_space_types_defined"
                ]
                all_ventilation_space_types_defined = zone_data[
                    "all_ventilation_space_types_defined"
                ]
                ER_modeled_p = data["ER_modeled_p"]
                serves_zones_that_have_dehumid_heat_recovery = data[
                    "serves_zones_that_have_dehumid_heat_recovery"
                ]
                sys_type_heating_only = data["sys_type_heating_only"]
                hvac_systems_and_assoc_zones_largest_exhaust_source = data[
                    "hvac_systems_and_assoc_zones_largest_exhaust_source"
                ][hvac_id_b]
                serves_zones_heated_to_60_or_higher_p = data[
                    "serves_zones_heated_to_60_or_higher_p"
                ]

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

                ER_modeled_b = fan_sys_b.get("air_energy_recovery") not in (
                    None,
                    ENERGY_RECOVERY.NONE,
                )

                exception_1_applies = (
                    sys_type_heating_only and not serves_zones_heated_to_60_or_higher_p
                )
                exception_2_applies = (
                    not ER_modeled_p
                    and serves_zones_with_systems_likely_exhausting_toxic_etc
                )
                exception_6_applies = (
                    not ER_modeled_p
                    and max(
                        hvac_systems_and_assoc_zones_largest_exhaust_source[
                            "hvac_fan_sys_exhaust_sum"
                        ],
                        hvac_systems_and_assoc_zones_largest_exhaust_source[
                            "maximum_zone_exhaust"
                        ],
                    )
                    < 0.75 * max_outdoor_airflow_b
                )

                exception_7_applies = (
                    not ER_modeled_p and serves_zones_that_have_dehumid_heat_recovery
                )

                return {
                    "climate_zone": climate_zone,
                    "ER_not_req_for_heating_sys": ER_not_req_for_heating_sys,
                    "serves_zones_with_systems_likely_exhausting_toxic_etc": serves_zones_with_systems_likely_exhausting_toxic_etc,
                    "serves_kitchen_space": serves_kitchen_space,
                    "all_lighting_space_types_defined": all_lighting_space_types_defined,
                    "all_ventilation_space_types_defined": all_ventilation_space_types_defined,
                    "serves_zones_that_have_dehumid_heat_recovery": serves_zones_that_have_dehumid_heat_recovery,
                    "sys_type_heating_only": sys_type_heating_only,
                    "supply_airflow_b": CalcQ("air_flow_rate", supply_airflow_b),
                    "min_outdoor_airflow_b": CalcQ(
                        "air_flow_rate", min_outdoor_airflow_b
                    ),
                    "OA_fraction_b": OA_fraction_b,
                    "ER_modeled_b": ER_modeled_b,
                    "ER_modeled_p": ER_modeled_p,
                    "max_outdoor_airflow_b": max_outdoor_airflow_b,
                    "hvac_systems_and_assoc_zones_largest_exhaust_source": hvac_systems_and_assoc_zones_largest_exhaust_source,
                    "exception_1_applies": exception_1_applies,
                    "exception_2_applies": exception_2_applies,
                    "exception_6_applies": exception_6_applies,
                    "exception_7_applies": exception_7_applies,
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                OA_fraction_b = calc_vals["OA_fraction_b"]
                supply_airflow_b = calc_vals["supply_airflow_b"]
                ER_modeled_b = calc_vals["ER_modeled_b"]
                ER_modeled_p = calc_vals["ER_modeled_p"]
                serves_kitchen_space = calc_vals["serves_kitchen_space"]
                max_outdoor_airflow_b = calc_vals["max_outdoor_airflow_b"]
                hvac_systems_and_assoc_zones_largest_exhaust_source = calc_vals[
                    "hvac_systems_and_assoc_zones_largest_exhaust_source"
                ]

                return (
                    # Case 7
                    (
                        OA_fraction_b >= OA_fraction_b_70
                        and supply_airflow_b >= SUPPLY_AIRFLOW_5000CFM
                    )
                    and (not ER_modeled_p and serves_kitchen_space)
                    or
                    # Case 8
                    (
                        not ER_modeled_b
                        and hvac_systems_and_assoc_zones_largest_exhaust_source[
                            "num_hvac_exhaust_fans"
                        ]
                        > 1
                        and max(
                            hvac_systems_and_assoc_zones_largest_exhaust_source[
                                "hvac_fan_sys_exhaust_sum"
                            ],
                            hvac_systems_and_assoc_zones_largest_exhaust_source[
                                "maximum_hvac_exhaust"
                            ],
                        )
                        < 0.75 * max_outdoor_airflow_b
                    )
                )

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                hvac_b = context.baseline
                hvac_id_b = hvac_b["id"]

                OA_fraction_b = calc_vals["OA_fraction_b"]
                supply_airflow_b = calc_vals["supply_airflow_b"]
                ER_modeled_p = calc_vals["ER_modeled_p"]
                serves_kitchen_space = calc_vals["serves_kitchen_space"]

                if (
                    OA_fraction_b >= OA_fraction_b_70
                    and supply_airflow_b >= SUPPLY_AIRFLOW_5000CFM
                    and not ER_modeled_p
                    and serves_kitchen_space
                ):
                    UNDETERMINED_MSG = f"The baseline system {hvac_id_b} supply air cfm >= 5,000 CFM and the OA fraction is >= 70 %OA, per G3.1.2.10 exhaust air energy recovery is required to be modeled in the baseline and it has not been modeled. However, the system serves kitchen type spaces and exception 3 may be applicable which is that commercial kitchen hoods (grease) classified as Type 1 by NFPA 96 shall not require exhaust air energy recovery to be modeled if exhaust air energy recovery is not used in the proposed design (note that it has not modeled in the proposed). Conduct manual check to determine if exception 3 is applicable."
                else:
                    UNDETERMINED_MSG = f"Exhaust air energy recovery was not modeled in the baseline when the OA fraction is greater or equal to 70% and the supply cfm is greater or equal to 5,000 cfm. However, it appears that Section 90.1 G3.1.2.10 Exception 6 may be applicable which states, 'Where the largest exhaust source is less than 75% of the design outdoor airflow. This exception shall only be used if exhaust air energy recovery is not used in the proposed design.'. There are multilple exhaust fans associated with the hvac system and therefore this could not be assessed as the configuration is unknown. Conduct manual check to determine if this exception applies. If not, then fail."

                return UNDETERMINED_MSG

            def rule_check(self, context, calc_vals=None, data=None):
                climate_zone = calc_vals["climate_zone"]
                OA_fraction_b = calc_vals["OA_fraction_b"]
                supply_airflow_b = calc_vals["supply_airflow_b"]
                ER_modeled_b = calc_vals["ER_modeled_b"]
                exception_1_applies = calc_vals["exception_1_applies"]
                exception_2_applies = calc_vals["exception_2_applies"]
                exception_6_applies = calc_vals["exception_6_applies"]
                exception_7_applies = calc_vals["exception_7_applies"]
                ER_not_req_for_heating_sys = calc_vals["ER_not_req_for_heating_sys"]
                sys_type_heating_only = calc_vals["sys_type_heating_only"]
                all_lighting_space_types_defined = calc_vals[
                    "all_lighting_space_types_defined"
                ]
                all_ventilation_space_types_defined = calc_vals[
                    "all_ventilation_space_types_defined"
                ]
                ER_modeled_p = calc_vals["ER_modeled_p"]

                return (
                    (
                        OA_fraction_b >= OA_fraction_b_70
                        and supply_airflow_b >= SUPPLY_AIRFLOW_5000CFM
                        and (
                            # CASE 1
                            (ER_modeled_b)
                            or
                            # CASE 2
                            (not ER_modeled_b and exception_1_applies)
                            or
                            # CASE 3
                            (not ER_modeled_b and exception_2_applies)
                            or
                            # CASE 4
                            (
                                not ER_modeled_b
                                and ER_not_req_for_heating_sys
                                and sys_type_heating_only
                            )
                            or
                            # CASE 5
                            (not ER_modeled_b and exception_6_applies)
                            or
                            # CASE 6
                            (not ER_modeled_b and exception_7_applies)
                        )
                    )
                    or (
                        (
                            OA_fraction_b < OA_fraction_b_70
                            or supply_airflow_b < SUPPLY_AIRFLOW_5000CFM
                        )
                        and
                        # CASE 9
                        (not ER_modeled_b)
                        or
                        # CASE 10
                        (ER_modeled_b)
                    )
                    or
                    # Case 11
                    not (
                        (
                            not all_lighting_space_types_defined
                            or not all_ventilation_space_types_defined
                        )
                        and not ER_modeled_p
                    )
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                all_lighting_space_types_defined = calc_vals[
                    "all_lighting_space_types_defined"
                ]
                all_ventilation_space_types_defined = calc_vals[
                    "all_ventilation_space_types_defined"
                ]
                ER_modeled_p = calc_vals["ER_modeled_p"]

                return (
                    CASE11_FAIL_MSG
                    if not (
                        (
                            not all_lighting_space_types_defined
                            or not all_ventilation_space_types_defined
                        )
                        and not ER_modeled_p
                    )
                    else ""
                )
