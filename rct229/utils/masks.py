def invert_mask(mask):
    """Returns a new mask that is the inverse of the original

    A mask is a list whose entries are either 0 or 1.
    The inverse mask has 0 entries where the original has 1 entries and visa versa

    Parameters
    ----------
    mask : list
        The original mask list

    Returns
    -------
    list
        The new inverse mask
    """
    # The mask should have zeros and ones only
    assert all(list(map(lambda x: x in [0, 1], mask)))
    # (0 + 1) % 2 == 1
    # (1 + 1) % 2 == 0
    return [(mask_val + 1) % 2 for mask_val in mask]
