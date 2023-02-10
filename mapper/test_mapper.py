import pytest

from data import initial1, initial2, expectted1, expectted2
from mapper import main


@pytest.mark.parametrize(
    'initial, expected', [(initial1, expectted1), (initial2, expectted2)]
)
def test_mapper(initial, expected):
    result = main(initial)
    assert result == expected
