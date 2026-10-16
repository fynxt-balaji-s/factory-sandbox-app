import csv
import io
from decimal import Decimal

from invoice import to_csv


def test_empty():
    assert to_csv([], Decimal("0.2")) == "qty,unit_price,line_total\n,,TOTAL 0.00\n"


def test_trailing_newline_and_line_endings():
    out = to_csv([(1, Decimal("1.00"))], Decimal("0"))
    assert out.endswith("\n")
    assert not out.endswith("\n\n")
    assert "\r" not in out


def test_multi_line_with_tax():
    lines = [(2, Decimal("3.50")), (1, Decimal("10.00")), (3, Decimal("0.333"))]
    out = to_csv(lines, Decimal("0.2"))
    assert out.split("\n") == [
        "qty,unit_price,line_total",
        "2,3.50,7.00",
        "1,10.00,10.00",
        "3,0.33,1.00",
        ",,TOTAL 21.60",
        "",
    ]


def test_large_amounts_quoted_and_parse_back():
    lines = [(2, Decimal("617.25")), (1, Decimal("5.00"))]
    out = to_csv(lines, Decimal("0"))
    rows = list(csv.reader(io.StringIO(out)))
    assert rows == [
        ["qty", "unit_price", "line_total"],
        ["2", "617.25", "1,234.50"],
        ["1", "5.00", "5.00"],
        ["", "", "TOTAL 1,239.50"],
    ]
    assert all(len(r) == 3 for r in rows)
    assert '"1,234.50"' in out
