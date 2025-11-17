from rct229.rulesets.ashrae9012022.data_fns.table_J_4_fns import table_J_4_lookup
from rct229.rulesets.ashrae9012022.data_fns.table_J_6_fns import table_J_6_lookup
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import assert_, getattr_
from rct229.utils.std_comparisons import std_equal_with_precision

ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]
CHILLER_COMPRESSOR = SchemaEnums.schema_enums["ChillerCompressorOptions"]
CHILLER_EFFICIENCY_METRIC = SchemaEnums.schema_enums["ChillerEfficiencyMetricOptions"]


EXPECTED_VALIDATION_PLR = [0.25, 0.50, 0.75, 1.00]
EXPECTED_CHILLED_WATER_TEMPS = [39.0, 45.0, 50.0, 55.0]
EXPECTED_ENTERING_CONDENSER_WATER_TEMPS = [60.0, 72.5, 85.0, 97.5, 104.0]

J4_CURVE_SET = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
]
J6_CURVE_SET = ["V", "X", "Y", "Z", "AA", "AB"]


def is_chiller_performance_app_j(chiller: dict, curve_set: str) -> bool:
    """
    Evaluates whether the chiller performance curves align with the sets of performance curves specified in Appendix J of ASHRAE 90.1-2022 Appendix G.

    Parameters
    ----------
    chiller: dict
         The chiller object containing all relevant data for the chiller to be validated against the performance curves in Appendix J of ASHRAE 90.1-2022.
         This includes the rated capacity, full load efficiency (COP), compressor type, and the lists of capacity and power operating points.
    curve_set: str
        The curve set that the chiller is expected to align with. This should be a letter code of A, B, etc. to lookup in either Table J-4 or J-6.

    Returns
    -------
    bool
        boolean value indicating whether the chiller performance validation passed or failed.

    """

    if curve_set in J4_CURVE_SET:
        table_lookup = "J-4"
    elif curve_set in J6_CURVE_SET:
        table_lookup = "J-6"
    else:
        raise ValueError(
            "Invalid curve set provided. Must be A-U for Table J-4 or V-AB for Table J-6."
        )

    rated_capacity = getattr_(chiller, "chillers", "rated_capacity")
    full_load_efficiency_rated = getattr_(
        chiller, "chillers", "efficiency_metric_values"
    )[
        0
    ]  # First item is `FULL_LOAD_EFFICIENCY_RATED`, specified under the `efficiency_metric_types` key

    assert_(
        rated_capacity > 0 * ureg("W"), "The `capacity` value must be greater than 0 W."
    )
    assert_(
        full_load_efficiency_rated > 0,
        "The `efficiency_metric_values` must be greater than 0.",
    )

    rated_power = rated_capacity / full_load_efficiency_rated

    if table_lookup == "J-4":
        eir_f_t_coefficients = table_J_4_lookup(curve_set, "EIR-f-T")
        cap_f_t_coefficients = table_J_4_lookup(curve_set, "CAP-f-T")
        plr_coefficients = table_J_4_lookup(curve_set, "EIR-f-PLR")
    else:
        eir_f_t_coefficients = table_J_6_lookup(curve_set, "EIR-f-T")
        cap_f_t_coefficients = table_J_6_lookup(curve_set, "CAP-f-T")
        plr_coefficients = table_J_6_lookup(curve_set, "EIR-f-PLR")

    capacity_operating_pts_dict = {}
    capacity_operating_points = getattr_(
        chiller, "chillers", "capacity_operating_points"
    )
    for capacity_operating_point in capacity_operating_points:
        chilled_water_supply_temp = getattr_(
            capacity_operating_point,
            "capacity_operating_points",
            "chilled_water_supply_temperature",
        ).to("degF")
        condenser_temp = getattr_(
            capacity_operating_point,
            "capacity_operating_points",
            "condenser_temperature",
        ).to("degF")

        dict_key = (
            f"{round(chilled_water_supply_temp.m, 1)}, {round(condenser_temp.m, 1)}"
        )
        capacity_operating_pts_dict[dict_key] = getattr_(
            capacity_operating_point,
            "capacity_operating_points",
            "capacity",
        )
        assert_(
            capacity_operating_pts_dict[dict_key] > 0,
            "The 'capacity' value must be greater than 0 W.",
        )

    power_operating_pts_dict = {}
    power_operating_points = getattr_(chiller, "chillers", "power_operating_points")
    for power_operating_point in power_operating_points:
        chilled_water_supply_temp = getattr_(
            power_operating_point,
            "power_operating_points",
            "chilled_water_supply_temperature",
        ).to("degF")
        condenser_temp = getattr_(
            power_operating_point,
            "power_operating_points",
            "condenser_temperature",
        ).to("degF")

        dict_key = (
            f"{round(chilled_water_supply_temp.m, 1)}, {round(condenser_temp.m, 1)}"
        )

        power_operating_pts_dict.setdefault(dict_key, [])
        power_operating_pts_dict[dict_key].append(power_operating_point)

    given_capacities = {}
    non_matching_capacity_operating_points = []
    missing_capacity_operating_points = []
    for chwt in EXPECTED_CHILLED_WATER_TEMPS:
        for ecwt in EXPECTED_ENTERING_CONDENSER_WATER_TEMPS:
            dict_key = f"{chwt}, {ecwt}"
            if dict_key in capacity_operating_pts_dict:
                expected_capacity = (
                    cap_f_t_coefficients[0]
                    + cap_f_t_coefficients[1] * chwt
                    + cap_f_t_coefficients[2] * chwt**2
                    + cap_f_t_coefficients[3] * ecwt
                    + cap_f_t_coefficients[4] * ecwt**2
                    + cap_f_t_coefficients[5] * chwt * ecwt
                ) * rated_capacity

                given_capacity = capacity_operating_pts_dict[dict_key]
                given_capacities[dict_key] = given_capacity

                if not std_equal_with_precision(
                    given_capacity, expected_capacity, 1 * ureg("W")
                ):
                    non_matching_capacity_operating_points.append(
                        {"CHWT": chwt, "ECWT": ecwt}
                    )
            else:
                missing_capacity_operating_points.append({"CHWT": chwt, "ECWT": ecwt})

    non_matching_power_operating_points = []
    missing_power_operating_points = []
    for chwt in EXPECTED_CHILLED_WATER_TEMPS:
        for ecwt in EXPECTED_ENTERING_CONDENSER_WATER_TEMPS:
            dict_key = f"{chwt}, {ecwt}"
            if dict_key in power_operating_pts_dict:
                for power_operating_point in power_operating_pts_dict[dict_key]:
                    load = getattr_(
                        power_operating_point, "power_operating_points", "load"
                    )
                    given_power = getattr_(
                        power_operating_point, "power_operating_points", "power"
                    )

                    plr = (
                        load / given_capacities[dict_key]
                    )  # no need to check `given_capacities[dict_key]` = 0.0 (checked in line 95)

                    # plr.m because plr is a "dimensionless" unit
                    if any(
                        [
                            std_equal_with_precision(plr.m, expected_plr, 2)
                            for expected_plr in EXPECTED_VALIDATION_PLR
                        ]
                    ):
                        eir_plr = (
                            plr_coefficients[0]
                            + plr_coefficients[1] * plr
                            + plr_coefficients[2] * plr**2
                        )
                        eir_ft = (
                            eir_f_t_coefficients[0]
                            + eir_f_t_coefficients[1] * chwt
                            + eir_f_t_coefficients[2] * chwt**2
                            + eir_f_t_coefficients[3] * ecwt
                            + eir_f_t_coefficients[4] * ecwt**2
                            + eir_f_t_coefficients[5] * chwt * ecwt
                        )
                        expected_power = (
                            given_capacities[dict_key]
                            * eir_ft
                            * eir_plr
                            * rated_power
                            / rated_capacity
                        )

                        if not std_equal_with_precision(
                            given_power, expected_power, 1 * ureg("W")
                        ):
                            non_matching_power_operating_points.append(
                                {"CHWT": chwt, "ECWT": ecwt, "PLR": "ALL"}
                            )
                    else:
                        missing_power_operating_points.append(
                            {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                        )
            else:
                missing_power_operating_points.append(
                    {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                )

    return (
        len(non_matching_capacity_operating_points)
        == len(missing_capacity_operating_points)
        == len(non_matching_power_operating_points)
        == len(missing_power_operating_points)
        == 0
    )
