import json
import logging
import sys

def load_json(json_file_path):
    with open(json_file_path) as f:
        return json.load(f)


def get_value_from_key(key, context, func_name=None):
    """
    This function handles the exception raise when key is not in context
    Parameters
    ----------
    key
    context

    Returns
    -------

    """
    logger = logging.getLogger(func_name if func_name is not None else __name__)

    if context.get(key) is None:
        logger.info("key: '%s' is not in the context" % key)
        return None
    return context[key]


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
    return str if len(str) is 0 or str[0] is "/" else "/" + str
