from collections import deque
from dataclasses import dataclass, field
from typing import List

from rct229.rulesets.ashrae9012019.ruleset_functions.get_spaces_served_by_swh_use import (
    get_spaces_served_by_swh_use,
)
from rct229.utils.jsonpath_utils import find_all


@dataclass
class SWHDistributionAssociations:
    swh_heating_eq: List[str] = field(default_factory=list)
    pumps: List[str] = field(default_factory=list)
    tanks: List[str] = field(default_factory=list)
    piping: List[str] = field(default_factory=list)
    solar_thermal: List[str] = field(default_factory=list)
    uses: List[str] = field(default_factory=list)
    spaces_served: List[str] = field(default_factory=list)


def get_swh_equipment_associated_with_each_swh_distribution_system(
    rmd: dict,
) -> dict[str, SWHDistributionAssociations]:
    """
    This function gets all the SWH equipment connected to a SWH distribution system.  The information is stored in a dictionary where the keys are the SWH Distribution System Ids and values are a dictionary giving the ServiceWaterHeatingEquipment, and Pumps connected to the particular SWH distribution system.
    Parameters
    ----------
    rmd: dict, RMD at RuleSetModelDescription level
    Returns
    -------
    swh_and_equip_dict: A dictionary containing where the keys are the SWH Distribution System IDs and values are dictionaries where keys are the type of SWH equipment and values are the ids of the connected equipment.
                        Example:  {"swh_distribution1":{"swh_heating_eq":["swh_eq1","swh_eq2"], "pumps":["p1"], "tanks":["t1"], "piping":["piping1"], "solar_thermal":[], "uses":["sp1_use","sp2_use"], "spaces_served":[sp1,sp2]}}
    """

    swh_and_equip_dict = {}
    for distribution in find_all(
        "$.service_water_heating_distribution_systems[*]", rmd
    ):
        swh_and_equip_dict[distribution["id"]] = SWHDistributionAssociations()
        swh_and_equip_dict[distribution["id"]].tanks = [
            tank["id"] for tank in find_all("$.tanks[*]", distribution)
        ]

        piping = distribution.get("service_water_piping")
        if piping:
            queue = deque([piping])
            piping_ids = []
            # BFS approach
            while queue:
                current_piping = queue.popleft()
                piping_ids.append(current_piping["id"])
                children = current_piping.get("child", [])
                queue.extend(children)
            swh_and_equip_dict[distribution["id"]].piping.extend(piping_ids)

        for pump in find_all("$.pumps[*]", rmd):
            if (
                pump.get("loop_or_piping")
                in swh_and_equip_dict[distribution["id"]].piping
            ):
                swh_and_equip_dict[distribution["id"]].pumps.append(pump["id"])

        for swh_equip in find_all("$.service_water_heating_equipment[*]", rmd):
            if swh_equip.get("distribution_system") == distribution["id"]:
                swh_and_equip_dict[distribution["id"]].swh_heating_eq.append(
                    swh_equip["id"]
                )
                for solar_t in swh_equip.get("solar_thermal_systems", []):
                    swh_and_equip_dict[distribution["id"]].solar_thermal.append(
                        solar_t["id"]
                    )

    # TODO revise the json path if the service_water_heating_uses is relocated in the schema
    for swh_use in find_all(
        "$.service_water_heating_uses[*]",
        rmd,
    ):
        distribution_id = swh_use.get("served_by_distribution_system")
        if distribution_id:
            swh_and_equip_dict[distribution_id].uses.append(swh_use["id"])
            for space_id in get_spaces_served_by_swh_use(rmd, swh_use["id"]):
                if space_id not in swh_and_equip_dict[distribution_id].spaces_served:
                    swh_and_equip_dict[distribution_id].spaces_served.append(space_id)
    return swh_and_equip_dict
