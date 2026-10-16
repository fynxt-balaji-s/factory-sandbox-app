from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def line_total(qty: int, unit_price: Decimal) -> Decimal:
    if qty < 0:
        raise ValueError("qty must be >= 0")
    return (unit_price * qty).quantize(CENT, ROUND_HALF_UP)


def invoice_total(lines: list[tuple[int, Decimal]], tax_rate: Decimal) -> Decimal:
    subtotal = sum((line_total(q, p) for q, p in lines), Decimal("0"))
    return (subtotal * (1 + tax_rate)).quantize(CENT, ROUND_HALF_UP)


def item_count(lines: list[tuple[int, Decimal]]) -> int:
    """Return the total quantity across all lines (not distinct products)."""
    return sum(q for q, _ in lines)
