
from jsonpointer import resolve_pointer
import copy

def match_lists(list0, list1, id_pointer):
    """Returns new lists with the entries matched as much as possible

    Parameters
    ----------
    list0 : list
        The primary list
    list1 : list
        The secondary list
    id_pointer : string
        A json pointer

    Returns
    -------
    tuple of lists
        The the new lists are sorted and match according to id_pointer where
        possible. None is inserted to indicate non-matches.
    """

    def _id_key(obj):
        """ Uses id_pointer as a json pointer to select an identifier from an object"""
        return resolve_pointer(obj, id_pointer)

    # Make shallow copies of the lists
    list0 = copy.copy(list0)
    list1 = copy.copy(list1)

    # Sort the lists
    list0.sort(key = _id_key)
    list1.sort(key = _id_key)


    # Step through list0, looking for matches in list1
    list0_orig_len = len(list0)
    for index in range(list0_orig_len):
        if index >= len(list1):
            list1.append(None)
        elif _id_key(list0[index]) != _id_key(list1[index]):
            # Insert None entries to indicate non-matches
            list1.insert(index, None)


    # Append extra None entries to list0 to match the length of list1
    while len(list0) < len(list1):
        list0.append(None)


    return (list0, list1)
