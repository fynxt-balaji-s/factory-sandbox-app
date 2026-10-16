from decimal import Decimal

from invoice import invoice_total, line_total


def test_negative_qty_returns_zero():
    assert line_total(-1, Decimal("1")) == Decimal("0.00")


def test_negative_qty_result_is_quantized():
    assert str(line_total(-5, Decimal("2.50"))) == "0.00"


def test_positive_qty_unchanged():
    assert line_total(3, Decimal("1.10")) == Decimal("3.30")
    assert str(line_total(0, Decimal("2.50"))) == "0.00"
    assert line_total(1, Decimal("0.005")) == Decimal("0.01")


def test_invoice_total_negative_line_adds_zero():
    lines = [(2, Decimal("10")), (-3, Decimal("5"))]
    assert invoice_total(lines, Decimal("0")) == Decimal("20.00")
