"""Lab 6 - Branch coverage tests for restaurant_bill.py

Goal: make every decision (if / elif) evaluate to BOTH True and False, and
exercise each side of the compound conditions and boundary values.
Run:  coverage run --branch -m pytest BranchCoverageTest_restaurant_bill.py
      coverage report -m
"""
import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# ---------------- bill_total ----------------
# if section not in SERVICE_CHARGE
def test_unknown_section_raises():
    with pytest.raises(ValueError, match="unknown section"):
        bill_total("balcony", 1000, 2, False)


# if food_total < 0 or guests < 1   (each operand True on its own + both False)
def test_negative_food_total_raises():
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", -1, 2, False)


def test_zero_guests_raises():
    with pytest.raises(ValueError, match="invalid order"):
        bill_total("dine_in", 1000, 0, False)


def test_zero_food_total_is_valid():
    # boundary: food_total == 0 is allowed
    assert bill_total("dine_in", 0, 1, False) == 0


# if is_happy_hour and section != "takeaway"
def test_dine_in_no_happy_hour():          # is_happy_hour False
    assert bill_total("dine_in", 1000, 2, False) == 1155


def test_dine_in_happy_hour():             # both True -> discount applied
    assert bill_total("dine_in", 1000, 2, True) == 924


def test_rooftop_happy_hour():             # both True, different service rate
    # 800 + 120 service = 920; +46 tax = 966
    assert bill_total("rooftop", 1000, 2, True) == 966


def test_takeaway_happy_hour_no_discount():   # is_happy_hour True, section == takeaway
    assert bill_total("takeaway", 1000, 2, True) == 1050


def test_rooftop_no_happy_hour():
    # 1000 + 150 service = 1150; +57 tax = 1207
    assert bill_total("rooftop", 1000, 2, False) == 1207


# if guests >= 8   (boundary 7 / 8)
def test_seven_guests_no_surcharge():
    assert bill_total("dine_in", 1000, 7, False) == 1155


def test_eight_guests_surcharge():
    assert bill_total("dine_in", 1000, 8, False) == 1365


# ---------------- split_bill ----------------
# if people < 1
def test_split_invalid_people_raises():
    with pytest.raises(ValueError, match="invalid people count"):
        split_bill(1000, 0, 10)


# if tip_percent < 0
def test_split_invalid_tip_raises():
    with pytest.raises(ValueError, match="invalid tip"):
        split_bill(1000, 2, -5)


def test_split_zero_tip_is_valid():
    assert split_bill(1000, 2, 0) == 500


# if grand_total % people != 0   (True and False)
def test_even_split():
    assert split_bill(1000, 4, 10) == 275


def test_uneven_split_rounds_up():
    assert split_bill(1000, 3, 0) == 334


# ---------------- table_wait ----------------
# if party_size > 12   (boundary 12 / 13)
def test_party_of_13_call_ahead():
    assert table_wait(13, 5, False) == "call ahead"


def test_party_of_12_not_call_ahead():
    assert table_wait(12, 5, False) == "seat now"


def test_call_ahead_beats_reservation():
    assert table_wait(13, 5, True) == "call ahead"


# if has_reservation
def test_reservation_seats_immediately():
    assert table_wait(4, 0, True) == "seat now"


# if free_tables == 0
def test_no_free_tables_waitlist():
    assert table_wait(2, 0, False) == "waitlist"


# elif party_size > 6 and free_tables < 2
def test_party_of_7_one_table_waitlist():     # both True
    assert table_wait(7, 1, False) == "waitlist"


def test_party_of_6_one_table_seat_now():     # party_size > 6 False (boundary)
    assert table_wait(6, 1, False) == "seat now"


def test_party_of_7_two_tables_seat_now():    # free_tables < 2 False (boundary)
    assert table_wait(7, 2, False) == "seat now"
