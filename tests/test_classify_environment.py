import math

import pytest

from src.transform.gold_integration import classify_environment


@pytest.mark.parametrize(
    "ratio, expected",
    [
        (0.60, "Green"),
        (0.30, "Green"),
        (0.29, "Moderate"),
        (0.10, "Moderate"),
        (0.09, "Critical"),
        (0.0, "Critical"),
    ],
)
def test_more_renewable_share_is_never_worse(ratio, expected):
    assert classify_environment(ratio) == expected


def test_undefined_ratio_is_unknown():
    assert classify_environment(math.nan) == "Unknown"
