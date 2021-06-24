def strict_linear_interpolation(pt0, pt1, x):
    """Performs linear interpolation between two points

    Parameters
    ----------
    pt0 : (float, float)
        The left-hand point
    pt1 : (float, float)
        The right-hand point; must have pt0[0] <= pt1[0]
    x : float
        The value to be interpolated

    Returns
    -------
    float
        The interpolated value
    """
    x0 = pt0[0]
    y0 = pt0[1]
    x1 = pt1[0]
    y1 = pt1[1]

    if not pt0[0] <= pt1[0]:
        raise ValueError("pt0 pt1 out of order")
    elif not (x0 <= x <= x1):
        raise ValueError("x out of range")
    elif x == x0:
        return y0
    elif x == x1:
        return y1
    else:
        return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def strict_list_linear_interpolation(sorted_pts, x):
    """Performs linear interpolation between a sorted list of points

    Parameters
    ----------
    sorted_pts : list of (float, float)
        A sorted list of points; [0] values are ascending
    x : float
        The value to be interpolated

    Returns
    -------
    float
        The interpolated value
    """
    if x < sorted_pts[0][0] or sorted_pts[-1][0] < x:
        raise ValueError("x out of range")

    for index in range(len(sorted_pts)):
        if x <= sorted_pts[index + 1][0]:
            return strict_linear_interpolation(
                sorted_pts[index], sorted_pts[index + 1], x
            )

    ## Should never get here
    assert False
