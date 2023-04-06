from rct229.utils.assertions import assert_, getattr_
from rct229.utils.jsonpath_utils import find_all, find_exactly_one_with_field_value


def get_min_oa_cfm_sch_zone(rmi, zone_id, is_leap_year: bool = False):
    """Each zone can have multiple terminal units sering it in the proposed RMR and each of these units could supply OA CFM. In order to obtain a zone level OA CFM schedule the OA CFM provided by each terminal unit needs to be aggregated for each hour of the year. This function receives an RMR (B, U, or P) and a zone ID and loops through each terminal unit associated with the zone to create an aggregated 8760 for OA CFM for the zone.

    Parameters
    ----------
    rmi: json
        The RMR in which the OA CFM schedule will be determined for the specific Zone ID.
    zone_id:
        The Zone ID in which the aggregated (across the terminal units serving the zone) hourly OA CFM schedule will be determined.
    is_leap_year: bool, default: False
        Whether the year is a leap year or not.

    Returns
    -------
    list: An aggregated OA CFM hourly schedule for the zone (for each hour of the year, for each terminal unit, Terminal.minimum_outdoor_airflow is multiplied by Terminal.minimum_outdoor_airflow_multiplier_schedule, this product is summed across the terminal units for each hour of the year) .
    """

    if is_leap_year:
        min_OA_CFM_schedule_for_zone = [0] * 8784
    else:
        min_OA_CFM_schedule_for_zone = [0] * 8760

    for terminal in find_all(
        f'$.buildings[*].building_segments[*].zones[*][?(@.id = "{zone_id}")].terminals[*]',
        rmi,
    ):
        minimum_outdoor_airflow = getattr_(
            terminal, "minimum_outdoor_airflow", "minimum_outdoor_airflow"
        )

        minimum_outdoor_airflow_multiplier_schedule_id = terminal.get(
            "minimum_outdoor_airflow_multiplier_schedule"
        )

        if minimum_outdoor_airflow_multiplier_schedule_id:
            minimum_outdoor_airflow_multiplier_schedule = getattr_(
                find_exactly_one_with_field_value(
                    "$.schedules[*]",
                    "id",
                    minimum_outdoor_airflow_multiplier_schedule_id,
                    rmi,
                ),
                "hourly_values",
                "hourly_values",
            )

            assert_(
                len(minimum_outdoor_airflow_multiplier_schedule)
                in (
                    8760,
                    8784,
                )
                and len(min_OA_CFM_schedule_for_zone)
                == len(minimum_outdoor_airflow_multiplier_schedule),
                f"The length of schedule has to be either 8760 or 8784, but is {len(minimum_outdoor_airflow_multiplier_schedule)}.",
            )

            min_OA_CFM_schedule_for_zone = list(
                map(
                    lambda x, y: x + y * minimum_outdoor_airflow,
                    min_OA_CFM_schedule_for_zone,
                    minimum_outdoor_airflow_multiplier_schedule,
                )
            )

    return min_OA_CFM_schedule_for_zone
