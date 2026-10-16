from decimal import Decimal

import invoice
from invoice import invoice_total, summary


def test_basic_summary():
    lines = [(2, Decimal("10")), (1, Decimal("5"))]
    assert summary(lines, Decimal("0.2")) == {
        "subtotal": Decimal("25.00"),
        "tax": Decimal("5.00"),
        "total": Decimal("30.00"),
    }


def test_total_matches_invoice_total_odd_rounding():
    lines = [(3, Decimal("19.99")), (1, Decimal("0.37"))]
    rate = Decimal("0.0825")
    result = summary(lines, rate)
    assert result["total"] == invoice_total(lines, rate)
    assert result["subtotal"] + result["tax"] == result["total"]
    assert result["subtotal"] == Decimal("60.34")


def test_empty_lines():
    result = summary([], Decimal("0.2"))
    assert result == {
        "subtotal": Decimal("0.00"),
        "tax": Decimal("0.00"),
        "total": Decimal("0.00"),
    }
    for v in result.values():
        assert str(v) == "0.00"


def test_all_values_decimal_with_cents():
    result = summary([(1, Decimal("1.234"))], Decimal("0.0825"))
    assert set(result) == {"subtotal", "tax", "total"}
    for v in result.values():
        assert isinstance(v, Decimal)
        assert v.as_tuple().exponent == -2


def test_summary_uses_subtotal(monkeypatch):
    calls = []
    original = invoice.subtotal

    def spy(lines):
        calls.append(lines)
        return original(lines)

    monkeypatch.setattr(invoice, "subtotal", spy)
    lines = [(1, Decimal("5"))]
    result = summary(lines, Decimal("0.1"))
    assert calls == [lines]
    assert result["subtotal"] == Decimal("5.00")
