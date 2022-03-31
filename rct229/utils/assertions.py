from rct229.utils.jsonpath_utils import find_all


class MissingKeyException(Exception):
    def __init__(self, object_name, obj_id, first_key):
        message = f"{object_name}:{obj_id} is missing {first_key} field"
        super().__init__(message)


def assert_(bool, err_msg):
    assert bool, err_msg


def assert_nonempty_lists(req_nonempty_lists, obj):
    for jpath in req_nonempty_lists:
        for req_list in find_all(jpath + "[*]", obj):
            assert len(req_list) > 0, f"{jpath} id:{req_list['id']} is empty"


def assert_required_fields(req_fields, obj):
    for (jpath, fields) in req_fields.items():
        for element in find_all(jpath, obj):
            for field in fields:
                assert (
                        field in element
                ), f"Missing {field} in {jpath} id:{element.get('id')}"


def getattr_(obj, obj_name: str, first_key, *remaining_keys):
    """Gets the value inside a dictionary described by a key path or raises an expection

    Parameters
    ----------
    obj : dict
        A potentially nested dictionary of dictionaries to be searched. At each
        level along the key path, the dictionary must have an id field.
    obj_name : str
        The name for the dictionary to be searched
    first_key : str
        The first key in the path
    remaining_keys: [str]
        Any additional keys in the path

    Returns
    -------
    any
        The value stored the the given key path

    Raises
    ------
    AssertionError if the key path does not exist. The error message indicates what
    field was missing.
    """
    if first_key not in obj:
        raise MissingKeyException(obj_name, obj["id"], first_key)
    # assert (first_key in obj, f"{obj_name}:{obj['id']} is missing {first_key} field")
    val = obj[first_key]

    return (
        val
        if len(remaining_keys) == 0
        else getattr_(val, first_key, remaining_keys[0], *remaining_keys[1:])
    )
