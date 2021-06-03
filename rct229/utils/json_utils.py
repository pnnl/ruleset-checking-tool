def to_json_pointer(str):
    """Guarantees that a string is either the empty string or it starts with
    a slash

    Parameters
    ----------
    str : string

    Returns
    -------
    string
        The original string possibly prepended with a slash if it did not
        already start with one. The empty string is left unchanged.
    """
    slash_str = str if str == "" or str[0] is "/" else "/" + str

    return slash_str
