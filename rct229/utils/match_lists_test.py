import pytest

from match_lists import match_lists

# Testing match_lists()
def test_match_lists_with_identical_sorted_lists():
    assert match_lists(
        [
            {'name': 'A'},
            {'name': 'B'},
            {'name': 'C'}
        ],
        [
            {'name': 'A'},
            {'name': 'B'},
            {'name': 'C'}
        ],
        '/name'
    ) == ([
        {'name': 'A'},
        {'name': 'B'},
        {'name': 'C'}
    ],
    [
        {'name': 'A'},
        {'name': 'B'},
        {'name': 'C'}
    ])


def test_match_lists_with_identical_unsorted_lists():
    assert match_lists(
        [
            {'name': 'B'},
            {'name': 'A'},
            {'name': 'C'}
        ],
        [
            {'name': 'B'},
            {'name': 'A'},
            {'name': 'C'}
        ],
        '/name'
    ) == ([
        {'name': 'A'},
        {'name': 'B'},
        {'name': 'C'}
    ],
    [
        {'name': 'A'},
        {'name': 'B'},
        {'name': 'C'}
    ])



def test_match_lists_with_different_unsorted_lists():
    assert match_lists(
        [
            {'name': 'B'},
            {'name': 'A', 'num': 8},
            {'name': 'C'}
        ],
        [
            {'name': 'H'},
            {'name': 'A'}
        ],
        '/name'
    ) == ([
        {'name': 'A', 'num': 8},
        {'name': 'B'},
        {'name': 'C'},
        None
    ],
    [
        {'name': 'A'},
        None,
        None,
        {'name': 'H'}
    ])
