
from jsonpointer import resolve_pointer
import copy

def match_lists(index_list, list2, id_pointer):
    """Returns a new list of entries taken from list2 that match the
    corresponding entries of index_list. An entry is set to None if there is no
    match in list2.

    Parameters
    ----------
    index_list : list
        The primary list
    list2 : list
        The secondary list
    id_pointer : string
        A json pointer to the field to be used to match the list entries,
        usually 'name' or 'id'

    Returns
    -------
    list
        A new list of entries taken from list2 that match the
        corresponding entries of index_list. An entry is set to None if there is no
        match in list2.
    """

    def id_key(obj):
        """ Uses id_pointer as a json pointer to select an identifier from an object"""
        return resolve_pointer(obj, id_pointer)


    # Step through index_list, looking for matches in list2
    match_list = list(map(
        lambda entry:
            # Grabs the first entry in list2 that matches or None
            next(iter([entry2 for entry2 in list2 if id_key(entry) == id_key(entry2)]), None),
        index_list
    ))

    return match_list
