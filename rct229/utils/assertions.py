from rct229.utils.jsonpath_utils import find_all


class AssertionStatusCategory:
    """Enumeration class for RCT execution status"""

    SEVERE: str = "SEVERE"
    WARNING: str = "WARNING"


class RCTException(Exception):
    def __init__(self, message):
        super().__init__(message)
        # self.status = status


class RCTFailureException(RCTException):
    def __init__(self, message):
        super().__init__(message)


class MissingKeyException(RCTException):
    def __init__(self, object_name, obj_id, first_key):
        message = f"{object_name}:{obj_id} is missing {'one of the fields in: ' if isinstance(first_key, list) else ''}{first_key}"
        super().__init__(message)


def assert_(bool, err_msg):
    if not bool:
        raise RCTFailureException(err_msg)


def assert_nonempty_lists(req_nonempty_lists, obj):
    for jpath in req_nonempty_lists:
        for req_list in find_all(jpath + "[*]", obj):
            assert len(req_list) > 0, f"{jpath} id:{req_list['id']} is empty"


def assert_required_fields(req_fields, obj):
    for (jpath, fields) in req_fields.items():
        for element in find_all(jpath, obj):
            for field in fields:
                if field not in element:
                    raise MissingKeyException(jpath, element.get("id"), field)


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
    val = obj[first_key]

    return (
        val
        if len(remaining_keys) == 0
        else getattr_(val, first_key, remaining_keys[0], *remaining_keys[1:])
    )


def get_first_attr_(obj, obj_name: str, key_list):
    """Gets first value inside a dictionary described by a list of keys or raises an expection

    Parameters
    ----------
    obj : dict
        A potentially nested dictionary of dictionaries to be searched. At each
        level along the key path, the dictionary must have an id field.
    obj_name : str
        The name for the dictionary to be searched
    key_list : list
        A list of key to test

    Returns
    -------
    any
        The value stored in the first exist/valid key.

    Raises
    ------
    AssertionError if all keys in the list are not exist in the object, raise MissingKeyException
    """
    for key in key_list:
        if obj.get(key):
            return obj[key]
    raise MissingKeyException(obj_name, obj["id"], key_list)
