from rct229.rule_engine.partial_rule_definition import PartialRuleDefinition
from rct229.rule_engine.rule_list_indexed_base import RuleDefinitionListIndexedBase
from rct229.rule_engine.ruleset_model_factory import produce_ruleset_model_description
from rct229.rulesets.ashrae9012019 import BASELINE_0
from rct229.utils.pint_utils import ZERO
from rct229.schema.config import ureg
from rct229.utils.assertions import assert_
from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all

APPLICABILITY_MSG = "This building has service water heating loads. Confirm that service water heating energy consumption is calculated explicitly based upon the volume of service water heating required and the entering makeup water and leaving service water heating temperatures.  Entering water temperatures shall be estimated based upon the location. Leaving temperatures shall be based upon the end-use requirements."


class PRM9012019Rule51s51(RuleDefinitionListIndexedBase):
    """Rule 13 of ASHRAE 90.1-2019 Appendix G Section 11 (Service Water Heating)"""

    def __init__(self):
        super(PRM9012019Rule51s51, self).__init__(
            rmds_used=produce_ruleset_model_description(
                USER=False, BASELINE_0=True, PROPOSED=False
            ),
            each_rule=PRM9012019Rule51s51.RMDRule(),
            index_rmd=BASELINE_0,
            id="11-13",
            description=(
                "Service water-heating energy consumption shall be calculated explicitly based upon the volume of service water heating required and the entering makeup water and the leaving service water-heating temperatures. Entering water temperatures shall be estimated based upon the location. Leaving temperatures shall be based upon the end-use requirements."
            ),
            ruleset_section_title="Service Water Heating",
            standard_section="Table G3.1 #11, baseline column, (e)",
            is_primary_rule=False,
            list_path="ruleset_model_descriptions[0]",
        )

    class RMDRule(RuleDefinitionListIndexedBase):
        def __init__(self):
            super(PRM9012019Rule51s51.RMDRule, self).__init__(
                rmds_used=produce_ruleset_model_description(
                    USER=False, BASELINE_0=True, PROPOSED=False
                ),
                index_rmd=BASELINE_0,
                each_rule=PRM9012019Rule51s51.RMDRule.BuildingRule(),
                list_path="$.buildings[*]",
            )

        def create_data(self, context, data):
            rmd_b = context.BASELINE_0
            energy_required_to_heat_swh_use_dict = {}
            service_water_heating_use_dict = {}

            for building_segment in find_all(
                "$.buildings[*].building_segments[*]", rmd_b
            ):
                service_water_heating_use_list = (
                    get_swh_uses_associated_with_each_building_segment(rmd_b)[
                        building_segment["id"]
                    ]
                )
                service_water_heating_use_dict[
                    building_segment["id"]
                ] = service_water_heating_use_list
                for swh_use in service_water_heating_use_list:
                    # If no swh use specified or swh use is 0, skip
                    if swh_use.get("use", 0) == 0:
                        continue
                    energy_required_to_heat_swh_use = (
                        get_energy_required_to_heat_swh_use(
                            swh_use["id"], rmd_b, building_segment["id"]
                        )
                    )
                    if swh_use["id"] not in energy_required_to_heat_swh_use_dict:
                        energy_required_to_heat_swh_use_dict[swh_use["id"]] = {}
                    energy_required_to_heat_swh_use_dict[swh_use["id"]][
                        building_segment["id"]
                    ] = energy_required_to_heat_swh_use
            return {
                "energy_required_to_heat_swh_use_dict": energy_required_to_heat_swh_use_dict,
                "service_water_heating_use_ids_dict": service_water_heating_use_dict,
            }

        class BuildingRule(PartialRuleDefinition):
            def __init__(self):
                super(PRM9012019Rule51s51.RMDRule.BuildingRule, self).__init__(
                    rmds_used=produce_ruleset_model_description(
                        USER=False, BASELINE_0=True, PROPOSED=False
                    ),
                    manual_check_required_msg=APPLICABILITY_MSG,
                )

            def get_calc_vals(self, context, data=None):
                building_b = context.BASELINE_0
                energy_required_to_heat_swh_use_dict = data[
                    "energy_required_to_heat_swh_use_dict"
                ]
                service_water_heating_use_dict = data[
                    "service_water_heating_use_ids_dict"
                ]
                service_water_heating_info = {
                    "btu_per_year": ZERO.ENERGY,
                    "btu_per_sf_per_year": 0 * ureg("Btu/ft2"),
                }
                is_applicable = False
                for building_segment in find_all("$.building_segments[*]", building_b):
                    for swh_use in service_water_heating_use_dict[
                        building_segment["id"]
                    ]:
                        if swh_use.get("use", 0.0) > 0:
                            is_applicable = True
                            energy_required_by_space = (
                                energy_required_to_heat_swh_use_dict[swh_use["id"]][
                                    building_segment["id"]
                                ]
                            )
                            if None in energy_required_by_space.values():
                                service_water_heating_info[
                                    "btu_per_year"
                                ] = "UNDETERMINED"
                                service_water_heating_info[
                                    "btu_per_sf_per_year"
                                ] = "UNDETERMINED"
                            else:
                                service_water_heating_info["btu_per_year"] += sum(
                                    energy_required_by_space.values()
                                )
                if (
                    service_water_heating_info["btu_per_year"] != "UNDETERMINED"
                    and service_water_heating_info["btu_per_year"] != ZERO.ENERGY
                ):
                    floor_area = sum(
                        find_all(
                            "$.building_segments[*].zones[*].spaces[*].floor_area",
                            building_b,
                        ),
                        ZERO.AREA,
                    )
                    assert_(
                        floor_area > ZERO.AREA,
                        f"Floor area for building: {building_b['id']} is 0, check inputs.",
                    )
                    service_water_heating_info["btu_per_sf_per_year"] = (
                        service_water_heating_info["btu_per_year"] / floor_area
                    )

                return {
                    "is_applicable": is_applicable,
                    "service_water_heating_btu_per_sf_per_year": service_water_heating_info[
                        "btu_per_sf_per_year"
                    ],
                }

            def applicability_check(self, context, calc_vals, data):
                is_applicable = calc_vals["is_applicable"]
                return is_applicable
