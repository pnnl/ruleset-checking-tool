import json


def load_json(json_file_path):
    with open(json_file_path) as f:
        return json.load(f)


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
    return str if len(str) == 0 or str[0] == "/" else "/" + str
