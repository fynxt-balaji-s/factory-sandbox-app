from decimal import Decimal

import pytest

from invoice import format_money


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        (Decimal("1234.5"), "1,234.50"),
        (Decimal("0"), "0.00"),
        (Decimal("-12.3"), "-12.30"),
        (Decimal("-1234.5"), "-1,234.50"),
        (Decimal("0.005"), "0.01"),
        (Decimal("-0.005"), "-0.01"),
        (Decimal("1234567.891"), "1,234,567.89"),
        (Decimal("999.995"), "1,000.00"),
        (Decimal("-0.001"), "0.00"),
    ],
)
def test_format_money(amount, expected):
    assert format_money(amount) == expected
