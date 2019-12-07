import pytest

from permutations import generate_permutations

@pytest.mark.parametrize(
    "n, expected",
    [
        (0, []),
        (1, [[0]]),
        (2, [[0, 1], [1, 0]]),
        (3, [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]),
    ]
)
def test_permutations(n, expected):
    assert generate_permutations(n) == expected