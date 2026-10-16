from decimal import Decimal

from invoice import max_line_total


def test_max_of_two_lines():
    assert max_line_total([(2, Decimal("10")), (1, Decimal("5"))]) == Decimal("20.00")


def test_max_is_by_line_total_not_unit_price():
    assert max_line_total([(10, Decimal("1")), (1, Decimal("5"))]) == Decimal("10.00")


def test_single_line():
    assert max_line_total([(3, Decimal("2.50"))]) == Decimal("7.50")


def test_empty_returns_none():
    assert max_line_total([]) is None
