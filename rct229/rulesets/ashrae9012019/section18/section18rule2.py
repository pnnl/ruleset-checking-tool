from rct229.rule_engine.rule_base import RuleDefinitionBase
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_instance
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_system_type_compare import (
    baseline_system_type_compare,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.baseline_systems.baseline_system_util import (
    HVAC_SYS,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_building_total_lab_exhaust_from_zone_exhaust_fans import (
    get_building_total_lab_exhaust_from_zone_exhaust_fans,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.g311_exceptions.g311_sub_functions.get_zones_on_same_floor_list import (
    get_zones_on_same_floor_list,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_baseline_system_types import (
    get_baseline_system_types,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_dict_of_zones_and_terminal_units_served_by_hvac_sys import (
    get_dict_of_zones_and_terminal_units_served_by_hvac_sys,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_lab_zone_hvac_systems import (
    get_lab_zone_hvac_systems,
)
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.jsonpath_utils import find_all

FAN_SYSTEM_OPERATION = SchemaEnums.schema_enums["FanSystemOperationOptions"]


APPLICABLE_SYS_TYPES = [
    HVAC_SYS.SYS_1,
    HVAC_SYS.SYS_2,
    HVAC_SYS.SYS_3,
    HVAC_SYS.SYS_4,
    HVAC_SYS.SYS_5,
    HVAC_SYS.SYS_6,
    HVAC_SYS.SYS_7,
    HVAC_SYS.SYS_8,
    HVAC_SYS.SYS_9,
    HVAC_SYS.SYS_10,
    HVAC_SYS.SYS_11_1,
    HVAC_SYS.SYS_12,
    HVAC_SYS.SYS_13,
]

AIRFLOW_15000_CFM = 15000 * ureg("cfm")


class Section18Rule2(RuleDefinitionListIndexedBase):
    """Rule 2 of ASHRAE 90.1-2019 Appendix G Section 18 (HVAC - System Zone Assignment)"""

    def __init__(self):
        super(Section18Rule2, self).__init__(
            rmrs_used=produce_ruleset_model_instance(
                USER=False, BASELINE_0=True, PROPOSED=True
            ),
            each_rule=Section18Rule2.RMDRule(),
            index_rmr=BASELINE_0,
            id="18-2",
            description="Does the modeled system serve the appropriate zones (one system per zone for system types 1, 2, 3, 4, 9, 10, 11, 12, and 13 and "
            "one system per floor for system types 5, 6, 7, and 8, with the exception of system types 5 or 7 serving laboratory spaces - these systems should serve ALL laboratory zones in the buidling).",
            ruleset_section_title="HVAC - System Zone Assignment",
            standard_section="Section 18 HVAC_SystemZoneAssignment",
            is_primary_rule=True,
            list_path="ruleset_model_descriptions[0]",
            required_fields={
                "$": ["weather", "calendar", "ruleset_model_descriptions"],
                "weather": ["climate_zone"],
                "calendar": ["is_leap_year"],
            },
            data_items={
                "climate_zone": (BASELINE_0, "weather/climate_zone"),
                "is_leap_year": (BASELINE_0, "calendar/is_leap_year"),
            },
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(Section18Rule2.RMDRule, self).__init__(
                rmrs_used=produce_ruleset_model_instance(
                    USER=False, BASELINE_0=True, PROPOSED=True
                ),
                each_rule=Section18Rule2.RMDRule.HVACRule(),
                index_rmr=BASELINE_0,
                list_path="$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            rmd_p = context.PROPOSED
            climate_zone_b = data["climate_zone"]
            is_leap_year_b = data["is_leap_year"]

            baseline_system_types_dict_b = get_baseline_system_types(rmd_b)
            applicable_hvac_sys_ids_b = [
                hvac_id
                for sys_type in baseline_system_types_dict_b
                for target_sys_type in APPLICABLE_SYS_TYPES
                if baseline_system_type_compare(sys_type, target_sys_type, False)
                for hvac_id in baseline_system_types_dict_b[sys_type]
            ]

            zones_and_terminal_unit_list_dict_b = (
                get_dict_of_zones_and_terminal_units_served_by_hvac_sys(rmd_b)
            )
            lab_zone_hvac_systems = get_lab_zone_hvac_systems(
                rmd_b, rmd_p, climate_zone_b, is_leap_year_b
            )
            building_total_lab_zone_exhaust_b = (
                get_building_total_lab_exhaust_from_zone_exhaust_fans(rmd_b)
            )

            # create a hvac data dict
            hvac_data_b = {}
            for hvac_id_b in find_all(
                "$.buildings[*].building_segments[*].heating_ventilating_air_conditioning_systems[*].id",
                rmd_b,
            ):
                if hvac_id_b in applicable_hvac_sys_ids_b:
                    lab_zones_only_b = lab_zone_hvac_systems["lab_zones_only"]
                    hvac_data_b[hvac_id_b] = {
                        "is_zone_single_zone_sys_b": any(
                            [
                                hvac_id_b in baseline_system_types_dict_b[sys_type]
                                for sys_type in APPLICABLE_SYS_TYPES
                            ]
                        ),
                        "does_sys_only_serve_lab_b": (
                            hvac_id_b in lab_zones_only_b and len(lab_zones_only_b) == 1
                        ),
                        "does_sys_serve_lab_b": (hvac_id_b in lab_zones_only_b),
                        "does_sys_serve_lab_and_other_b": (
                            hvac_id_b in lab_zone_hvac_systems["lab_and_other"]
                        ),
                        "does_two_sys_exist_on_same_fl_b": "false",
                        "hvac_sys2_id_b": None,
                    }

                    hvac_data_by_id_b = hvac_data_b[hvac_id_b]

                    do_multi_zone_evaluation = not any(
                        [
                            hvac_data_by_id_b["is_zone_single_zone_sys_b"],
                            hvac_data_by_id_b["does_sys_only_serve_lab_b"],
                            hvac_data_by_id_b["does_sys_serve_lab_b"],
                            hvac_data_by_id_b["does_sys_serve_lab_and_other_b"],
                        ]
                    )

                    zones_served_by_system = zones_and_terminal_unit_list_dict_b[
                        hvac_id_b
                    ]["zone_list"]

                    zones_on_floor = (
                        get_zones_on_same_floor_list(
                            rmd_b,
                            zones_and_terminal_unit_list_dict_b[hvac_id_b]["zone_list"],
                        )
                        if do_multi_zone_evaluation
                        else []
                    )

                    # check if all the zones served by the system are on the same floor
                    if all([zone in zones_on_floor for zone in zones_served_by_system]):
                        # check if there are any other systems of the same system type that serve zones on this floor
                        for hvac_sys_type2 in applicable_hvac_sys_ids_b:
                            for hvac_sys2_id_b in baseline_system_types_dict_b[
                                hvac_sys_type2
                            ]:
                                # check if hvac_id_b and hvac_sys2_id_b are the same system
                                if hvac_sys2_id_b != hvac_id_b:
                                    zones_served_by_system2 = (
                                        zones_and_terminal_unit_list_dict_b[
                                            hvac_sys2_id_b
                                        ]["zone_list"]
                                    )
                                    if len(
                                        set(zones_served_by_system2).intersection(
                                            set(zones_on_floor)
                                        )
                                        == 0
                                    ):
                                        hvac_data_b[hvac_id_b][
                                            "does_two_sys_exist_on_same_fl_b"
                                        ] = "false"
                                    elif (
                                        hvac_sys2_id_b
                                        in lab_zone_hvac_systems["lab_zones_only"]
                                        and len(lab_zone_hvac_systems["lab_zones_only"])
                                        == 1
                                        and building_total_lab_zone_exhaust_b
                                        > AIRFLOW_15000_CFM
                                    ):
                                        hvac_data_b[hvac_id_b][
                                            "does_two_sys_exist_on_same_fl_b"
                                        ] = "true"

                                    elif (
                                        hvac_sys2_id_b in lab_zones_only_b
                                        and len(lab_zones_only_b) == 1
                                        and building_total_lab_zone_exhaust_b
                                        <= AIRFLOW_15000_CFM
                                    ):
                                        hvac_data_b[hvac_id_b][
                                            "does_two_sys_exist_on_same_fl_b"
                                        ] = "undetermined"

                                    else:
                                        hvac_data_b[hvac_id_b][
                                            "does_two_sys_exist_on_same_fl_b"
                                        ] = "false"
                                    hvac_data_b[hvac_id_b][
                                        "hvac_sys2_id_b"
                                    ] = hvac_sys2_id_b

            return {
                "hvac_data_b": hvac_data_b,
                "building_total_lab_zone_exhaust_b": building_total_lab_zone_exhaust_b,
            }

        class HVACRule(RuleDefinitionBase):
            def __init__(self):
                super(Section18Rule2.RMDRule.HVACRule, self).__init__(
                    rmrs_used=produce_ruleset_model_instance(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                )

            def get_calc_vals(self, context, data=None):
                hvac_b = context.BASELINE_0
                hvac_id_b = hvac_b["id"]
                hvac_data_b = data["hvac_data_b"][hvac_id_b]

                return {
                    "is_zone_single_zone_sys_b": hvac_data_b[
                        "is_zone_single_zone_sys_b"
                    ],
                    "does_sys_only_serve_lab_b": hvac_data_b[
                        "does_sys_only_serve_lab_b"
                    ],
                    "does_sys_serve_lab_b": hvac_data_b["does_sys_serve_lab_b"],
                    "does_sys_serve_lab_and_other_b": hvac_data_b[
                        "does_sys_serve_lab_and_other_b"
                    ],
                    "does_two_sys_exist_on_same_fl_b": hvac_data_b[
                        "does_two_sys_exist_on_same_fl_b"
                    ],
                    "hvac_sys2_id_b": hvac_data_b["hvac_sys2_id_b"],
                }

            def manual_check_required(self, context, calc_vals=None, data=None):
                does_sys_only_serve_lab_b = calc_vals["does_sys_only_serve_lab_b"]
                does_sys_serve_lab_and_other_b = calc_vals[
                    "does_sys_serve_lab_and_other_b"
                ]
                building_total_lab_zone_exhaust_b = data[
                    "building_total_lab_zone_exhaust_b"
                ]
                does_two_sys_exist_on_same_fl_b = calc_vals[
                    "does_two_sys_exist_on_same_fl_b"
                ]

                return (
                    (
                        (does_sys_only_serve_lab_b or does_sys_serve_lab_and_other_b)
                        and building_total_lab_zone_exhaust_b <= AIRFLOW_15000_CFM
                    )
                ) or does_two_sys_exist_on_same_fl_b == "undetermined"

            def get_manual_check_required_msg(self, context, calc_vals=None, data=None):
                does_sys_only_serve_lab_b = calc_vals["does_sys_only_serve_lab_b"]
                does_sys_serve_lab_and_other_b = calc_vals[
                    "does_sys_serve_lab_and_other_b"
                ]
                does_two_sys_exist_on_same_fl_b = calc_vals[
                    "does_two_sys_exist_on_same_fl_b"
                ]
                hvac_sys2_id_b = calc_vals["hvac_sys2_id_b"]
                building_total_lab_zone_exhaust_b = data[
                    "building_total_lab_zone_exhaust_b"
                ]

                undetermined_msg = ""
                if building_total_lab_zone_exhaust_b <= AIRFLOW_15000_CFM:
                    if not does_sys_only_serve_lab_b:
                        undetermined_msg = (
                            "This system serves only lab zones, which is correct if the building has total lab exhaust greater than 15,000 cfm. "
                            "However, we could not determine with accuracy the total building exhuast."
                        )
                    elif not does_sys_serve_lab_and_other_b:
                        undetermined_msg = (
                            "This HVAC system serves lab zones in a building with > 15,000 cfm of laboratory exhaust. "
                            "The baseline system for laboratory zones should be type 5 or 7 and should serve only and all laboratory zones."
                        )
                elif does_two_sys_exist_on_same_fl_b == "undetermined":
                    undetermined_msg = (
                        f"This HVAC system is on the same floor as {hvac_sys2_id_b}, which servese lab zones in the building. "
                        f"If the building has greater than 15,000 cfm of lab exhaust and {hvac_sys2_id_b} is System type 5 or 7 serving only lab zones, this system passes, otherwise it fails."
                    )

                return undetermined_msg

            def rule_check(self, context, calc_vals=None, data=None):
                is_zone_single_zone_sys_b = calc_vals["is_zone_single_zone_sys_b"]
                does_sys_only_serve_lab_b = calc_vals["does_sys_only_serve_lab_b"]
                does_sys_serve_lab_b = calc_vals["does_sys_serve_lab_b"]
                does_sys_serve_lab_and_other_b = calc_vals[
                    "does_sys_serve_lab_and_other_b"
                ]
                does_two_sys_exist_on_same_fl_b = calc_vals[
                    "does_two_sys_exist_on_same_fl_b"
                ]
                building_total_lab_zone_exhaust_b = data[
                    "building_total_lab_zone_exhaust_b"
                ]

                return (
                    is_zone_single_zone_sys_b
                    or (
                        does_sys_only_serve_lab_b
                        and building_total_lab_zone_exhaust_b > AIRFLOW_15000_CFM
                    )
                    or (
                        (building_total_lab_zone_exhaust_b <= AIRFLOW_15000_CFM)
                        and (does_sys_serve_lab_b or does_sys_serve_lab_and_other_b)
                    )
                    or does_two_sys_exist_on_same_fl_b == "true"
                )

            def get_fail_msg(self, context, calc_vals=None, data=None):
                does_sys_serve_lab_b = context["does_sys_serve_lab_b"]
                does_sys_serve_lab_and_other_b = context[
                    "does_sys_serve_lab_and_other_b"
                ]
                building_total_lab_zone_exhaust_b = data[
                    "building_total_lab_zone_exhaust_b"
                ]

                fail_msg = ""
                if building_total_lab_zone_exhaust_b <= AIRFLOW_15000_CFM:
                    if not does_sys_serve_lab_b:
                        fail_msg = (
                            "This HVAC system serves lab zones in a building with > 15,000 cfm of laboratory exhaust. "
                            "The baseline system should be type 5 or 7 and should serve ALL laboratory zones."
                        )

                    elif not does_sys_serve_lab_and_other_b:
                        fail_msg = (
                            "This HVAC system serves lab zones in a building with > 15,000 cfm of laboratory exhaust. "
                            "The baseline system for laboratory zones should be type 5 or 7 and should serve only and all laboratory zones."
                        )

                return fail_msg
