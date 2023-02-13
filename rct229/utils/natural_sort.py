import re

"""
This is the implementation of human sorting originated in a discussion from Ned Batchlder:
It is Toothy's implementation in the comment:
http://nedbatchelder.com/blog/200712/human_sorting.html

"""


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    Parameters
    ----------
    text: a string

    Returns sorted list
    -------
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]
