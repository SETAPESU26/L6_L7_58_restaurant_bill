"""Lab 6 - Code (line) coverage tests for restaurant_bill.py

Goal: execute every line of the module at least once.
Run:  coverage run -m pytest CodeCoverageTest_restaurant_bill.py
      coverage report -m
"""
import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# ---------------- bill_total ----------------
def test_dine_in_bill():
    # 1000 + 10% service = 1100; +5% tax = 1155
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_unknown_section_raises():
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("balcony", 1000, 2, False)


def test_invalid_order_raises():
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -1, 2, False)


def test_happy_hour_discount():
    # 1000 -> 800 (20% off); service 80; 880 + 44 tax = 924
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_large_party_surcharge():
    # 1000 + 100 service + 200 large-party = 1300; +65 tax = 1365
    assert bill_total("dine_in", 1000, 8, False) == 1365


# ---------------- split_bill ----------------
def test_even_split():
    assert split_bill(1000, 4, 10) == 275


def test_uneven_split_rounds_up():
    # 1000 / 3 = 333.33 -> 334
    assert split_bill(1000, 3, 0) == 334


def test_split_invalid_people_raises():
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


def test_split_invalid_tip_raises():
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 2, -5)


# ---------------- table_wait ----------------
def test_table_wait_call_ahead():
    assert table_wait(13, 5, False) == "call ahead"


def test_table_wait_reservation():
    assert table_wait(4, 0, True) == "seat now"


def test_table_wait_no_free_tables():
    assert table_wait(2, 0, False) == "waitlist"


def test_table_wait_big_party_one_table():
    assert table_wait(7, 1, False) == "waitlist"


def test_table_wait_seat_now():
    assert table_wait(2, 3, False) == "seat now"
