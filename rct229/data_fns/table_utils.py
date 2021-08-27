from rct229.data.schema_enums import schema_enums


def find_osstd_table_entry(match_field_value, match_field_name, osstd_table):
    """Find a specific entry in an OSSTD table

    This takes advantage of the consistent structure accross all the OSSTD
    JSON files. Each file contains a dictionary with a single key. The value
    associated with that key is a list of dictionaries. This function searches
    through those inner dictionaries to find one with a matching
    match_field_name: match_field_value pair.

    Parameters
    ----------
    match_field_value : any
        The matching value for the match_field_name field
    match_field_name : str
        The matching field name
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
        filter(lambda entry: entry[match_field_name] == match_field_value, data_list)
    )
    assert len(matching_entries) == 1, f"Not exactly one {match_field_value} in OSSTD"

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
        entry = find_osstd_table_entry(match_field_value, match_field_name, osstd_table)
