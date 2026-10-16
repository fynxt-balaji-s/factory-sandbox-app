from decimal import Decimal

from invoice import item_count


def test_item_count_empty():
    assert item_count([]) == 0


def test_item_count_sums_quantities():
    assert item_count([(2, Decimal("10")), (1, Decimal("5"))]) == 3


def test_item_count_counts_quantities_not_distinct_lines():
    lines = [(5, Decimal("1")), (5, Decimal("1")), (0, Decimal("9"))]
    assert item_count(lines) == 10
