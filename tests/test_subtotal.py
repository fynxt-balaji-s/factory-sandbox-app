from decimal import Decimal

import pytest

from invoice import subtotal


def test_subtotal_sums_lines():
    assert subtotal([(2, Decimal("10")), (1, Decimal("5"))]) == Decimal("25.00")


def test_subtotal_empty():
    result = subtotal([])
    assert result == Decimal("0.00")
    assert str(result) == "0.00"


def test_subtotal_returns_cents():
    assert str(subtotal([(1, Decimal("5"))])) == "5.00"


def test_subtotal_line_rounding():
    assert subtotal([(3, Decimal("1.10"))]) == Decimal("3.30")
    # each line rounded half-up separately: 0.005 -> 0.01, twice -> 0.02
    assert subtotal([(1, Decimal("0.005")), (1, Decimal("0.005"))]) == Decimal("0.02")


def test_subtotal_negative_qty_raises():
    with pytest.raises(ValueError):
        subtotal([(-1, Decimal("1"))])
