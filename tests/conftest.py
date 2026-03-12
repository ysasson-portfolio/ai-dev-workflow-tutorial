"""
Shared pytest fixtures for the ShopSmart Sales Analytics Dashboard test suite.

See specs/001-sales-dashboard/data-model.md for Transaction schema details.
"""
from datetime import date

import pandas as pd
import pytest


@pytest.fixture
def raw_df():
    """Sample raw DataFrame (10 rows) matching the Transaction schema.

    Includes one row with a null total_amount and one with a null category
    to support clean_data() tests.
    """
    return pd.DataFrame(
        {
            "date": [
                "2024-01-05",
                "2024-01-12",
                "2024-02-03",
                "2024-02-18",
                "2024-03-07",
                "2024-03-22",
                "2024-04-10",
                "2024-04-25",
                "2024-05-14",
                "2024-05-30",
            ],
            "order_id": [
                "ORD-001",
                "ORD-002",
                "ORD-003",
                "ORD-004",
                "ORD-005",
                "ORD-006",
                "ORD-007",
                "ORD-008",
                "ORD-009",
                "ORD-010",
            ],
            "product": [
                "Wireless Headphones",
                "Phone Case",
                "Bluetooth Speaker",
                "Smart Watch",
                "Laptop Stand",
                "USB Hub",
                "Keyboard",
                "Mouse",
                "Webcam",
                "Monitor",
            ],
            "category": [
                "Audio",
                "Accessories",
                "Audio",
                "Wearables",
                "Accessories",
                "Electronics",
                "Electronics",
                "Electronics",
                None,           # null category — should be excluded by clean_data()
                "Electronics",
            ],
            "region": [
                "North",
                "South",
                "East",
                "West",
                "North",
                "South",
                "East",
                "West",
                "North",
                "South",
            ],
            "quantity": [2, 1, 3, 1, 2, 4, 1, 2, 1, 1],
            "unit_price": [49.99, 19.99, 79.99, 199.99, 39.99, 29.99, 89.99, 49.99, 69.99, 399.99],
            "total_amount": [
                99.98,
                19.99,
                239.97,
                199.99,
                79.98,
                119.96,
                89.99,
                99.98,
                None,           # null total_amount — should be excluded by clean_data()
                399.99,
            ],
        }
    )


@pytest.fixture
def clean_df():
    """Sample cleaned DataFrame (8 rows) — nulls removed, date parsed.

    Derived from raw_df() after clean_data() removes the two invalid rows
    (null category on row 8, null total_amount on row 8 — same row index 8).
    Total sales: 99.98+19.99+239.97+199.99+79.98+119.96+89.99+99.98+399.99 = 1349.83
    Actually let's remove the two null rows (index 8 has null category AND null total_amount is at index 8 too).
    Wait, looking at the raw_df: index 8 has null category, index 8 also has None total_amount.
    So both nulls are on the same row (index 8). That means only 1 row is excluded.
    clean_df has 9 rows.

    Total sales = 99.98+19.99+239.97+199.99+79.98+119.96+89.99+99.98+399.99 = 1349.83
    Unique order_ids = 9 (ORD-001 through ORD-010 minus ORD-009)
    """
    return pd.DataFrame(
        {
            "date": [
                date(2024, 1, 5),
                date(2024, 1, 12),
                date(2024, 2, 3),
                date(2024, 2, 18),
                date(2024, 3, 7),
                date(2024, 3, 22),
                date(2024, 4, 10),
                date(2024, 4, 25),
                date(2024, 5, 30),
            ],
            "order_id": [
                "ORD-001",
                "ORD-002",
                "ORD-003",
                "ORD-004",
                "ORD-005",
                "ORD-006",
                "ORD-007",
                "ORD-008",
                "ORD-010",
            ],
            "product": [
                "Wireless Headphones",
                "Phone Case",
                "Bluetooth Speaker",
                "Smart Watch",
                "Laptop Stand",
                "USB Hub",
                "Keyboard",
                "Mouse",
                "Monitor",
            ],
            "category": [
                "Audio",
                "Accessories",
                "Audio",
                "Wearables",
                "Accessories",
                "Electronics",
                "Electronics",
                "Electronics",
                "Electronics",
            ],
            "region": [
                "North",
                "South",
                "East",
                "West",
                "North",
                "South",
                "East",
                "West",
                "South",
            ],
            "quantity": [2, 1, 3, 1, 2, 4, 1, 2, 1],
            "unit_price": [49.99, 19.99, 79.99, 199.99, 39.99, 29.99, 89.99, 49.99, 399.99],
            "total_amount": [
                99.98,
                19.99,
                239.97,
                199.99,
                79.98,
                119.96,
                89.99,
                99.98,
                399.99,
            ],
        }
    )
