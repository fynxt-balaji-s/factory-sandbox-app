from decimal import Decimal

import pytest

from invoice import invoice_total

LINES = [(2, Decimal("10")), (1, Decimal("5"))]


def test_discount_applied_before_tax():
    assert invoice_total(LINES, Decimal("0.2"), Decimal("10")) == Decimal("27.00")


def test_no_discount_unchanged():
    assert invoice_total(LINES, Decimal("0.2")) == Decimal("30.00")


def test_explicit_zero_discount():
    assert invoice_total(LINES, Decimal("0.2"), Decimal("0")) == Decimal("30.00")


def test_full_discount():
    assert invoice_total(LINES, Decimal("0.2"), Decimal("100")) == Decimal("0.00")


@pytest.mark.parametrize("pct", [Decimal("-1"), Decimal("100.01")])
def test_discount_out_of_range(pct):
    with pytest.raises(ValueError):
        invoice_total(LINES, Decimal("0.2"), pct)


def test_discount_rounds_half_up():
    # 0.05 * 0.9 = 0.045 -> 0.05 with ROUND_HALF_UP (banker's would give 0.04)
    assert invoice_total([(1, Decimal("0.05"))], Decimal("0"), Decimal("10")) == Decimal("0.05")
