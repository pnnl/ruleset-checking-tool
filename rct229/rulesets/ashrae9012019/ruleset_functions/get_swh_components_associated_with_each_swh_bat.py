from dataclasses import dataclass, field
from typing import List

from rct229.rulesets.ashrae9012019.ruleset_functions.get_building_segment_swh_bat import (
    get_building_segment_swh_bat,
)
from rct229.rulesets.ashrae9012019.ruleset_functions.get_energy_required_to_heat_swh_use import (
    get_energy_required_to_heat_swh_use,
)
from rct229.utils.assertions import getattr_
from rct229.utils.jsonpath_utils import find_all
from rct229.utils.pint_utils import ZERO
from rct229.utils.utility_functions import (
    find_exactly_one_service_water_heating_distribution_system,
    find_exactly_one_service_water_heating_use,
)
from rct229.utils.assertions import getattr_


@dataclass
class SWHEquipmentAssociations:
    energy_required: ZERO.ENERGY
    swh_distribution: List[str] = field(default_factory=list)
    swh_heating_eq: List[str] = field(default_factory=list)
    pumps: List[str] = field(default_factory=list)
    tanks: List[str] = field(default_factory=list)
    piping: List[str] = field(default_factory=list)
    solar_thermal: List[str] = field(default_factory=list)
    swh_uses: List[str] = field(default_factory=list)


def get_swh_components_associated_with_each_swh_bat(
    rmd: dict,
) -> dict[str, SWHEquipmentAssociations]:
    """
    This function gets all the SWH equipment connected to a particular SWH use type.  The information is stored in a dictionary where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 and values are a dictionary giving the ServiceWaterHeatingDistributionSystem, ServiceWaterHeatingEquipment, and Pumps connected to the particular use type.  There is also an entry for the total energy required to heat all SWH uses for a year: "EnergyRequired" .

    Parameters
    ----------
    rmd: dict, RMD at RuleSetModelDescription level

    Returns
    -------
    swh_and_equip_dict: A dictionary containing where the keys are the ServiceWaterHeatingSpaceOptions2019ASHRAE901 in the RMD and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.
                        Example:  {"DORMITORY":{"swh_distribution":["swhd1","swhd2"], "swh_heating_eq":["swh_eq1","swh_eq2"], "pumps":["p1"], "tanks":["t1"], "piping":["piping1"], "solar_thermal":[], "swh_uses":["swh_use1","swh_use2"], "energy_required": 100000 Btu}}
    """

    swh_and_equip_dict = {}
    for building_segment in find_all("$.buildings[*].building_segments[*]", rmd):
        swh_bat = get_building_segment_swh_bat(rmd, building_segment["id"])
        if swh_bat is None:
            # if returns None, it means there is no swh system in the RPD.
            swh_bat = "UNDETERMINED"
        swh_and_equip_dict[swh_bat] = SWHEquipmentAssociations(
            energy_required=ZERO.ENERGY
        )
        # TODO Need to update json path if schema changes
        for swh_use_id in find_all(
            f'$.buildings[*].building_segments[*][?(@.id="{building_segment["id"]}")].zones[*].spaces['
            f"*].service_water_heating_uses[*]",
            rmd,
        ):
            swh_use = find_exactly_one_service_water_heating_use(rmd, swh_use_id)
            swh_use_energy_by_space_dict = get_energy_required_to_heat_swh_use(
                swh_use["id"], rmd, building_segment["id"]
            )

            swh_and_equip_dict[swh_bat].energy_required += sum(
                swh_use_energy_by_space_dict[space_id]
                for space_id in swh_use_energy_by_space_dict
                if swh_use_energy_by_space_dict[space_id]
            )

            swh_and_equip_dict[swh_bat].swh_uses.append(swh_use["id"])
            distribution_id = swh_use.get("served_by_distribution_system")
            if distribution_id not in swh_and_equip_dict[swh_bat].swh_distribution:
                swh_and_equip_dict[swh_bat].swh_distribution.append(distribution_id)
                distribution = (
                    find_exactly_one_service_water_heating_distribution_system(
                        rmd, distribution_id
                    )
                )
                tanks = getattr_(
                    distribution, "service_water_heating_distribution_systems", "tanks"
                )
                for tank in tanks:
                    swh_and_equip_dict[swh_bat].tanks.append(tank["id"])

                piping = distribution.get("service_water_piping")
                if piping:
                    queue = [piping]
                    piping_ids = []
                    # BFS approach
                    while queue:
                        current_piping = queue.pop(0)
                        piping_ids.append(current_piping["id"])
                        if current_piping.get("child"):
                            queue.extend(current_piping["child"])
                    swh_and_equip_dict[swh_bat].piping.extend(piping_ids)

        for swh_bat in swh_and_equip_dict:
            for pump in find_all("$.pumps[*]", rmd):
                if pump.get("loop_or_piping") in swh_and_equip_dict[swh_bat].piping:
                    swh_and_equip_dict[swh_bat].pumps.append(pump["id"])

            for swh_equip in find_all("$.service_water_heating_equipment[*]", rmd):
                if (
                    swh_equip.get("distribution_system")
                    in swh_and_equip_dict[swh_bat].swh_distribution
                ):
                    swh_and_equip_dict[swh_bat].swh_heating_eq.append(swh_equip["id"])
                    getattr_(
                        swh_equip,
                        "service_water_heating_equipment",
                        "solar_thermal_systems",
                    )
                    for solar_t in swh_equip["solar_thermal_systems"]:
                        swh_and_equip_dict[swh_bat].solar_thermal.append(solar_t["id"])

    return swh_and_equip_dict
