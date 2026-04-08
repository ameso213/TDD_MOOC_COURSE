import pytest
from library_logic import can_borrow_book, calculate_fine

def test_should_deny_borrowing_if_limit_reached():
    # User already has 3 books
    result = can_borrow_book(current_borrow_count=3, book_status="Available")
    assert result["allowed"] is False
    assert "limit reached" in result["reason"]

def test_should_deny_borrowing_if_book_in_maintenance():
    # Book is broken/being repaired
    result = can_borrow_book(current_borrow_count=0, book_status="Maintenance")
    assert result["allowed"] is False
    assert "maintenance" in result["reason"]

def test_should_allow_borrowing_under_normal_conditions():
    result = can_borrow_book(current_borrow_count=1, book_status="Available")
    assert result["allowed"] is True

def test_should_calculate_correct_fine():
    assert calculate_fine(5) == 5.0
    assert calculate_fine(0) == 0.0
    assert calculate_fine(-2) == 0.0

if __name__ == "__main__":
    pytest.main(["-v", __file__])