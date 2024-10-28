from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_swh_uses_associated_with_each_building_segment import (
    get_swh_uses_associated_with_each_building_segment,
)
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_service_water_heating_use,
    find_exactly_one_service_water_heating_distribution_system,
)


def get_swh_components_associated_with_each_swh_bat(
    rmd: dict, is_leap_year: bool
) -> dict[str, dict]:
    """
    This function gets all the SWH equipment connected to a particular SWH use type.  The information is stored in a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a dictionary giving the ServiceWaterHeatingDistributionSystem, ServiceWaterHeatingEquipment, and Pumps connected to the particular use type.  There is also an entry for the total energy required to heat all SWH uses for a year: "EnergyRequired" .

    Parameters
    ----------
    rmd: dict, RMD at RuleSetModelDescription level
    is_leap_year: bool, default: False
        Whether the year is a leap year or not.
    Returns
    -------
    swh_and_equip_dict: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.
                        Example:  {"DORMITORY":{"SWHDistribution":["swhd1","swhd2"], "SWHHeatingEq":["swh_eq1","swh_eq2"], "Pumps":["p1"], "Tanks":["t1"], "Piping":["piping1"], "SolarThermal":[], "SWH_Uses":["swh_use1","swh_use2"], "EnergyRequired": 100000 Btu}}
    """

    swh_and_equip_dict = {}
    for building_segment in find_all("$.buildings[*].building_segments[*]", rmd):
        swh_bat = get_building_segment_swh_bat(rmd, building_segment["id"])
        swh_and_equip_dict.setdefault(
            swh_bat,
            {
                "SWHDistribution": [],
                "SWHHeatingEq": [],
                "Pumps": [],
                "Tanks": [],
                "Piping": [],
                "SolarThermal": [],
                "SWH_Uses": [],
                "EnergyRequired": ZERO.ENERGY,
            },
        )

        service_water_heating_use_ids = (
            get_swh_uses_associated_with_each_building_segment(
                rmd, building_segment["id"]
            )
        )
        for swh_use_id in service_water_heating_use_ids:
            swh_use = find_exactly_one_service_water_heating_use(rmd, swh_use_id)
            energy_required = get_energy_required_to_heat_swh_use(
                swh_use_id, rmd, building_segment["id"], is_leap_year
            )
            if list(energy_required.values())[0] is not None:
                swh_and_equip_dict[swh_bat]["EnergyRequired"] += list(
                    energy_required.values()
                )[0]
            swh_and_equip_dict[swh_bat]["SWH_Uses"].append(swh_use_id)
            distribution_id = swh_use.get("served_by_distribution_system")
            if distribution_id not in swh_and_equip_dict[swh_bat]["SWHDistribution"]:
                swh_and_equip_dict[swh_bat]["SWHDistribution"].append(distribution_id)
                distribution = (
                    find_exactly_one_service_water_heating_distribution_system(
                        rmd, distribution_id
                    )
                )
                tanks = distribution.get("tanks")
                for tank in tanks:
                    swh_and_equip_dict[swh_bat]["Tanks"].append(tank["id"])

                for piping in distribution.get("service_water_piping", []):
                    queue = [piping]
                    piping_ids = []
                    # BFS approach
                    while queue:
                        current_piping = queue.pop(0)
                        piping_ids.append(current_piping["id"])
                        if current_piping.get("child"):
                            queue.extend(current_piping["child"])
                    swh_and_equip_dict[swh_bat]["Piping"].extend(piping_ids)

        for swh_bat in swh_and_equip_dict:
            for pump in find_all("$.pumps[*]", rmd):
                if pump.get("loop_or_piping") in swh_and_equip_dict[swh_bat]["Piping"]:
                    swh_and_equip_dict[swh_bat]["Pumps"].append(pump["id"])

            for swh_equip in find_all("$.service_water_heating_equipment[*]", rmd):
                if (
                    swh_equip.get("distribution_system")
                    in swh_and_equip_dict[swh_bat]["SWHDistribution"]
                ):
                    swh_and_equip_dict[swh_bat]["SWHHeatingEq"].append(swh_equip["id"])
                    for solar_t in swh_equip.get("solar_thermal_systems"):
                        swh_and_equip_dict[swh_bat]["SolarThermal"].append(
                            solar_t["id"]
                        )

    return swh_and_equip_dict
