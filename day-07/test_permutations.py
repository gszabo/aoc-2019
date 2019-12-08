import pytest

from permutations import generate_permutations, permutations_of


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, []),
        (1, [[0]]),
        (2, [[0, 1], [1, 0]]),
        (3, [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]),
    ],
)
def test_generate_permutations(n, expected):
    assert generate_permutations(n) == expected

@pytest.mark.parametrize(
    "input, expected",
    [
        ([], []),
        (["a"], [["a"]]),
        ([10, 20], [[10, 20], [20, 10]]),
        ([0, 1, 2], [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]),
    ],
)
def test_permutations_of(input, expected):
    assert permutations_of(input) == expected
