from rct229.rulesets.ashrae9012022.data_fns.table_J_6_fns import table_J_6_lookup
from rct229.schema.config import ureg
from rct229.schema.schema_enums import SchemaEnums
from rct229.utils.assertions import getattr_
from rct229.utils.std_comparisons import std_equal_with_precision

ENERGY_SOURCE = SchemaEnums.schema_enums["EnergySourceOptions"]
CHILLER_COMPRESSOR = SchemaEnums.schema_enums["ChillerCompressorOptions"]

EXPECTED_VALIDATION_PLR = [0.25, 0.5, 0.75, 1]
EXPECTED_CHWT_TEMPS = [39, 45, 50, 55]
EXPECTED_ECWT_TEMPS = [60, 104, 85, 72.5, 97.5]


def is_chiller_performance_app_j(chiller: dict) -> bool:
    """
    Evaluates whether the chiller performance curves align with the sets of performance curves specified in Appendix J of ASHRAE 90.1-2022 Appendix G.
    :param chiller:
    """

    compressor_type = getattr_(chiller, "chillers", "compressor_type")
    rated_capacity = getattr_(chiller, "chillers", "rated_capacity")
    if compressor_type == CHILLER_COMPRESSOR.CENTRIFUGAL:
        if rated_capacity < 150 * ureg("ton"):
            curve_set = "Z"
        elif 150 * ureg("ton") <= rated_capacity < 300 * ureg("ton"):
            curve_set = "AA"
        else:
            curve_set = "AB"
    elif compressor_type in (
        CHILLER_COMPRESSOR.POSITIVE_DISPLACEMENT,
        CHILLER_COMPRESSOR.SCROLL,
        CHILLER_COMPRESSOR.SCREW,
    ):
        if rated_capacity < 150 * ureg("ton"):
            curve_set = "V"
        elif rated_capacity > 300 * ureg("ton"):
            curve_set = "Y"
        else:
            curve_set = "X"
    else:
        curve_set = None

    if curve_set is not None:
        rated_power = (
            rated_capacity / chiller["full_load_efficiency"]
            if chiller.get("full_load_efficiency")
            else 0.0
        )

        eir_f_t_coefficients = table_J_6_lookup(curve_set, "EIR-f-T")
        cap_f_t_coefficients = table_J_6_lookup(curve_set, "CAP-f-T")
        plr_coefficients = table_J_6_lookup(curve_set, "EIR-f-PLR")

        capacity_validation_pts_dict = {}
        for capacity_validation_point in chiller.get("capacity_operating_points", []):
            chilled_water_supply_temp = capacity_validation_point.get(
                "chilled_water_supply_temperature", 0.0 * ureg("degC")
            ).to("degF")
            condenser_temp = capacity_validation_point.get(
                "condenser_temperature", 0.0 * ureg("degC")
            ).to("degF")

            dict_key = f"{int(round(chilled_water_supply_temp.m, 1))}, {int(round(condenser_temp.m, 1))}"
            capacity_validation_pts_dict[dict_key] = capacity_validation_point.get(
                "capacity"
            )

        power_validation_pts_dict = {}
        for power_validation_point in chiller.get("power_operating_points", []):
            chilled_water_supply_temp = power_validation_point.get(
                "chilled_water_supply_temperature", 0.0 * ureg("degC")
            ).to("degF")
            condenser_temp = power_validation_point.get(
                "condenser_temperature", 0.0 * ureg("degC")
            ).to("degF")
            dict_key = f"{int(round(chilled_water_supply_temp.m, 1))}, {int(round(condenser_temp.m, 1))}"

            power_validation_pts_dict.setdefault(dict_key, [])
            power_validation_pts_dict[dict_key].append(power_validation_point)

        given_capacities = {}
        missing_capacity_validation_points = []
        non_matching_capacity_validation_points = []
        for chwt in EXPECTED_CHWT_TEMPS:
            for ecwt in EXPECTED_ECWT_TEMPS:
                dict_key = f"{chwt}, {ecwt}"
                if capacity_validation_pts_dict.get(dict_key):
                    expected_capacity = (
                        cap_f_t_coefficients[0]
                        + cap_f_t_coefficients[1] * chwt
                        + cap_f_t_coefficients[2] * chwt**2
                        + cap_f_t_coefficients[3] * ecwt
                        + cap_f_t_coefficients[4] * ecwt**2
                        + cap_f_t_coefficients[5] * chwt * ecwt
                    ) * rated_capacity

                    given_capacity = capacity_validation_pts_dict[dict_key]
                    given_capacities[dict_key] = given_capacity

                    if not std_equal_with_precision(
                        given_capacity, expected_capacity, 1 * ureg("W")
                    ):
                        non_matching_capacity_validation_points.append(
                            {"CHWT": chwt, "ECWT": ecwt}
                        )

                else:
                    missing_capacity_validation_points.append(
                        {"CHWT": chwt, "ECWT": ecwt}
                    )

        non_matching_power_validation_points = []
        missing_power_validation_points = []
        for chwt in EXPECTED_CHWT_TEMPS:
            for ecwt in EXPECTED_ECWT_TEMPS:
                dict_key = f"{chwt}, {ecwt}"
                if power_validation_pts_dict.get(dict_key):
                    given_plrs = []
                    for power_validation_point in power_validation_pts_dict[dict_key]:
                        load = power_validation_point.get("load", 0.0 * ureg("W"))
                        given_power = power_validation_point.get("result")
                        plr = load / given_capacities[dict_key]

                        if plr in EXPECTED_VALIDATION_PLR:
                            given_plrs.append(plr)
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
                                given_capacity[dict_key]
                                * eir_ft
                                * eir_plr
                                * rated_power
                                / rated_capacity
                            )

                            if expected_power == given_power:
                                missing_power_validation_points.append(
                                    {"CHWT": chwt, "ECWT": ecwt, "PLR": "ALL"}
                                )
                            else:
                                missing_power_validation_points.append(
                                    {"CHWT": chwt, "ECWT": ecwt, "PLR": plr}
                                )

    return (
        len(non_matching_capacity_validation_points)
        == len(missing_capacity_validation_points)
        == len(non_matching_power_validation_points)
        == len(missing_power_validation_points)
        == 0
    )
