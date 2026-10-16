from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def line_total(qty: int, unit_price: Decimal) -> Decimal:
    if qty < 0:
        raise ValueError("qty must be >= 0")
    return (unit_price * qty).quantize(CENT, ROUND_HALF_UP)


def invoice_total(
    lines: list[tuple[int, Decimal]],
    tax_rate: Decimal,
    discount_pct: Decimal = Decimal(0),
) -> Decimal:
    if not Decimal(0) <= discount_pct <= Decimal(100):
        raise ValueError("discount_pct must be between 0 and 100")
    subtotal = sum((line_total(q, p) for q, p in lines), Decimal("0"))
    discounted = subtotal * (1 - discount_pct / 100)
    return (discounted * (1 + tax_rate)).quantize(CENT, ROUND_HALF_UP)
