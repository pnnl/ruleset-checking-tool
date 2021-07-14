def slash_prefix_guarantee(str):
    """Guarantees that a string starts with a slash by prepending one if
    not already present

    Parameters
    ----------
    str : string

    Returns
    -------
    string
        The original string possibly prepended with a slash if it did not
        already start with one
    """
    slash_str = str if len(str) is 0 or str[0] is "/" else "/" + str
    return slash_str
