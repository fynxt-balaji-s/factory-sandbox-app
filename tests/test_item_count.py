from decimal import Decimal

from invoice import item_count


def test_item_count():
    assert item_count([(2, Decimal("10")), (1, Decimal("5"))]) == 3


def test_item_count_empty():
    assert item_count([]) == 0
