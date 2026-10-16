from decimal import Decimal

import pytest

from invoice import invoice_total, line_total


def test_line_total():
    assert line_total(3, Decimal("1.10")) == Decimal("3.30")


def test_negative_qty():
    with pytest.raises(ValueError):
        line_total(-1, Decimal("1"))


def test_invoice_total_with_tax():
    lines = [(2, Decimal("10")), (1, Decimal("5"))]
    assert invoice_total(lines, Decimal("0.2")) == Decimal("30.00")
