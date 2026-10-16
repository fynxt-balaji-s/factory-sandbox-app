from decimal import Decimal

import pytest

from invoice import invoice_total


def test_invoice_total_with_discount():
    lines = [(2, Decimal("10")), (1, Decimal("5"))]
    assert invoice_total(lines, Decimal("0.2"), Decimal("10")) == Decimal("27.00")


def test_invoice_total_full_discount():
    lines = [(1, Decimal("5"))]
    assert invoice_total(lines, Decimal("0.2"), Decimal("100")) == Decimal("0.00")


@pytest.mark.parametrize("pct", [Decimal("-1"), Decimal("100.01")])
def test_invoice_total_invalid_discount(pct):
    with pytest.raises(ValueError):
        invoice_total([(1, Decimal("5"))], Decimal("0.2"), pct)
