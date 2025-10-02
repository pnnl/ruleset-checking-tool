import pandas as pd


def filter_by_conditions(df, conditions):
    """Filter DataFrame by multiple conditions"""
    query_parts = []
    for col, val in conditions.items():
        if val is not None:
            if isinstance(val, str):
                query_parts.append(f'{col} == "{val}"')
            else:
                query_parts.append(f"{col} == {val}")

    query_str = " & ".join(query_parts)
    if query_str:
        return df.query(query_str)
    else:
        return df


def recalculate_permit_based_average(
        filtered_data, climate_zones, level_number, credit_name, bldg_type
):
    # Define column names
    cz_col = ["Credit", "CZ1", "CZ2", "CZ3", "CZ4", "CZ4C", "CZ5", "CZ6", "CZ7", "CZ8"]
    result_df = pd.DataFrame(columns=cz_col)
    new_row_template = {cz: None for cz in cz_col}

    for level_no in level_number:
        new_row = new_row_template.copy()
        if "baseline" in credit_name:
            new_row["Credit"] = "baseline"
        else:
            new_row["Credit"] = f"{credit_name}_level{level_no}"

        for cz in climate_zones.keys():
            data = filtered_data[bldg_type][cz][str(level_no)]
            new_row[cz] = (
                                  data["Total.Site.EUI.kBtu_ft2"] * data["permits"]
                          ).sum() / data["permits"].sum()

        new_row_df = pd.DataFrame([new_row])
        result_df = pd.concat([result_df, new_row_df], ignore_index=True)

    return result_df


def calc_agg_value_by_climate_zone(credit_name: str, level_number: list[int]):
    level_number = sorted(level_number)

    # Read credit csv
    credit = pd.read_csv(f"./{credit_name}.csv", delimiter=",")

    # Define climate zones and moisture regimes
    climate_zones = {
        "CZ1": {"climate_zone": "Climate Zone 1", "moisture_regime": None},
        "CZ2": {"climate_zone": "Climate Zone 2", "moisture_regime": None},
        "CZ3": {"climate_zone": "Climate Zone 3", "moisture_regime": None},
        "CZ4": {"climate_zone": "Climate Zone 4", "moisture_regime": None},
        "CZ4C": {"climate_zone": "Climate Zone 4", "moisture_regime": "Marine"},
        "CZ5": {"climate_zone": "Climate Zone 5", "moisture_regime": None},
        "CZ6": {"climate_zone": "Climate Zone 6", "moisture_regime": None},
        "CZ7": {"climate_zone": "Climate Zone 7", "moisture_regime": None},
        "CZ8": {"climate_zone": "Climate Zone 8", "moisture_regime": None},
    }

    # Define building types
    bldg_types = ["all", "Single-Family", "Multifamily"]

    # Filter credit data by level, building type, and climate zone
    filtered_data = {}
    for bldg_type in bldg_types:
        filtered_data[bldg_type] = {}
        credit_bldg_type = (
            credit if bldg_type == "all" else credit[credit["bldg_type"] == bldg_type]
        )

        for cz, conditions in climate_zones.items():
            filtered_data[bldg_type][cz] = {}
            filtered_cz = filter_by_conditions(credit_bldg_type, conditions)[
                ["level_0", "Total.Site.EUI.kBtu_ft2", "permits"]
            ]

            for level_no in level_number:
                filtered_data[bldg_type][cz][str(level_no)] = filtered_cz[
                    filtered_cz["level_0"] == level_no
                    ][["Total.Site.EUI.kBtu_ft2", "permits"]]

    # Recalculate permit-based average for all building types
    all_bldg_type_df = recalculate_permit_based_average(
        filtered_data, climate_zones, level_number, credit_name, "all"
    )
    SF_df = recalculate_permit_based_average(
        filtered_data, climate_zones, level_number, credit_name, "Single-Family"
    )
    MF_df = recalculate_permit_based_average(
        filtered_data, climate_zones, level_number, credit_name, "Multifamily"
    )

    return {"all_bldg_type_df": all_bldg_type_df, "SF_df": SF_df, "MF_df": MF_df}


test = calc_agg_value_by_climate_zone("filtered_baseline", [0])
