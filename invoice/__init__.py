import csv
import io
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
    if discount_pct < 0 or discount_pct > 100:
        raise ValueError("discount_pct must be between 0 and 100")
    subtotal = sum((line_total(q, p) for q, p in lines), Decimal("0"))
    discounted = subtotal * (1 - discount_pct / 100)
    return (discounted * (1 + tax_rate)).quantize(CENT, ROUND_HALF_UP)


def subtotal(lines: list[tuple[int, Decimal]]) -> Decimal:
    total = sum((line_total(q, p) for q, p in lines), Decimal("0"))
    return total.quantize(CENT, ROUND_HALF_UP)


def max_line_total(lines: list[tuple[int, Decimal]]) -> Decimal | None:
    if not lines:
        return None
    return max(line_total(q, p) for q, p in lines)


def summary(lines: list[tuple[int, Decimal]], tax_rate: Decimal) -> dict:
    s = subtotal(lines)
    tot = invoice_total(lines, tax_rate)
    t = (tot - s).quantize(CENT, ROUND_HALF_UP)
    return {"subtotal": s, "tax": t, "total": tot}


def format_money(amount: Decimal) -> str:
    q = amount.quantize(CENT, ROUND_HALF_UP)
    if q == 0:
        q = abs(q)  # avoid "-0.00" for tiny negatives
    return f"{q:,.2f}"


def to_csv(lines: list[tuple[int, Decimal]], tax_rate: Decimal) -> str:
    """Export invoice lines as CSV text.

    Header ``qty,unit_price,line_total``, one row per line, then a final
    ``,,TOTAL <total>`` row. Amounts use ``format_money``; fields containing
    commas (e.g. ``1,234.50``) are quoted by the csv module. Rows are
    separated by ``\n`` and the output always ends with a trailing ``\n``.
    """
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["qty", "unit_price", "line_total"])
    for qty, unit_price in lines:
        writer.writerow(
            [qty, format_money(unit_price), format_money(line_total(qty, unit_price))]
        )
    total = format_money(invoice_total(lines, tax_rate))
    writer.writerow(["", "", f"TOTAL {total}"])
    return buf.getvalue()
