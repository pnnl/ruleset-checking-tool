from rct229.data.schema_enums import schema_enums


def find_osstd_table_entry(match_field_name_value_pairs, osstd_table):
    """Find a specific entry in an OSSTD table

    This takes advantage of the consistent structure accross all the OSSTD
    JSON files. Each file contains a dictionary with a single key. The value
    associated with that key is a list of dictionaries. This function searches
    through those inner dictionaries to find one that matches all the
    provided
    match_field_name: match_field_value
    pairs.

    Parameters
    ----------
    match_field_name_value_pairs : list of 2-tuples
        List of (match_field_name, match_field_value) tuples
    osstd_table : dict
        The OSSTD table data as loaded from its JSON file

    Returns
    -------
    dict
        The matching table entry
    """
    assert type(osstd_table) is dict

    keys = list(osstd_table.keys())
    assert len(keys) is 1

    data_list = osstd_table[keys[0]]
    assert type(data_list) is list

    matching_entries = list(
        filter(
            lambda entry: all(
                [
                    entry[match_field_name] == match_field_value
                    for (
                        match_field_name,
                        match_field_value,
                    ) in match_field_name_value_pairs
                ]
            ),
            data_list,
        )
    )
    assert (
        len(matching_entries) == 1
    ), f"Not exactly one match in OSSTD for {match_field_name_value_pairs}, found {len(matching_entries)} instead."

    matching_entry = matching_entries[0]
    assert type(matching_entry) is dict

    return matching_entries[0]


def check_enumeration_to_osstd_match_field_value_map(
    match_field_name,
    enum_type,
    osstd_table,
    enumeration_to_match_field_value_map,
    exclude_enum_names=[],
):
    """A sanity check for an enumeration to OSSTD match field value map

    Checks that
    1. Each enumerated value (except for those in exclude_enum_names) is a
       key in the map
    2. There is actually a matching entry in the underlying OSSTD table
       corresponding to each enumated value

    This function only applies to OSSTD tables that have a field name,
    match_field_name, whose values are unique in the OSSTD table.

    Parameters
    ----------
    match_field_name : str
        Field name for the OSSTD lookup
    enum_type : str
        The name of an enumeration from the ruleset
    osstd_table : dict
        An OSSTD table
    enumeration_to_match_field_value_map : dict
        The map to be checked
    exclude_enum_names: list
        A list of strings of the enumeration names to be excluded from the check
        For example, "NONE" may be used as a flag that is not intended to be
        looked up.

    Returns
    -------
    dict
        The matching table entry
    """
    schema_enum = schema_enums[enum_type]
    for e in schema_enum:
        e_name = e.name
        if e_name in exclude_enum_names:
            continue

        # Make sure each space type in the enumeration is in our map
        match_field_value = enumeration_to_match_field_value_map[e_name]
        assert match_field_value is not None, f"{e_name} is not in the map"

        # Make sure there is a corresponding entry in the OSSTD table
        # find_osstd_table_entry() will throw if not
        entry = find_osstd_table_entry(
            [(match_field_name, match_field_value)], osstd_table
        )
