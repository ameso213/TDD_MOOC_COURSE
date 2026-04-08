import pytest
from expense_logic import calculate_balance, get_category_summary

def test_balance_should_start_at_zero():
    assert calculate_balance([]) == 0.0

def test_income_and_expenses_should_calculate_correctly():
    txs = [
        {"amount": 100.0, "type": "income"},
        {"amount": 30.0, "type": "expense"},
        {"amount": 20.0, "type": "expense"}
    ]
    assert calculate_balance(txs) == 50.0

def test_should_raise_error_on_negative_amount():
    txs = [{"amount": -10.0, "type": "income"}]
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_balance(txs)

def test_category_summary_should_group_correctly():
    txs = [
        {"amount": 50.0, "type": "expense", "category": "Food"},
        {"amount": 20.0, "type": "expense", "category": "Food"},
        {"amount": 100.0, "type": "expense", "category": "Rent"},
        {"amount": 500.0, "type": "income", "category": "Salary"} # Should ignore income
    ]
    summary = get_category_summary(txs)
    assert summary["Food"] == 70.0
    assert summary["Rent"] == 100.0
    assert "Salary" not in summary

if __name__ == "__main__":
    print("Running Expense Logic Tests...")
    pytest.main(["-v", __file__])