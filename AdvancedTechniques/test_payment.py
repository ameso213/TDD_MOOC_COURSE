import pytest
from logic import OrderManager
import sys # Import sys to handle script exit code

class MockPaymentGateway:
    """A test double to verify behavior without hitting a real API."""
    def __init__(self):
        self.was_called = False

    def process_payment(self, amount: float) -> bool:
        print(f"[MockGateway] Intercepted payment request for ${amount}")
        self.was_called = True
        return True

def test_order_manager_executes_payment():
    """GREEN PHASE: Verify that valid orders reach the gateway.""" 
    print(f"\nRunning: Valid Order Test")
    mock = MockPaymentGateway()
    manager = OrderManager(mock)
    
    assert manager.complete_order(50.0) is True, "The order should be successful"
    assert mock.was_called is True, "The gateway method was not called by OrderManager"
    print(f"Test 'Valid Order Test' passed.")

def test_order_manager_raises_error_on_invalid_amount():
    """RED TO GREEN: Verify that invalid orders are caught before the gateway.""" # This comment is part of the docstring, not the print output.
    print(f"\nRunning: Invalid Order Test (Validation Logic)")
    mock = MockPaymentGateway()
    manager = OrderManager(mock)
    
    # This test would be 'RED' if the validation in logic.py was missing
    with pytest.raises(ValueError, match="Invalid order total"):
        manager.complete_order(-5.0)
    print(f"Test 'Invalid Order Test (Validation Logic)' passed.")

if __name__ == "__main__":
    print("=== Starting TDD Test Run ===")
    exit_code = pytest.main([__file__]) # Run tests in the current file and capture the exit code
    print(f"\n=== TDD Phase: {'Green (All tests passed)!' if exit_code == 0 else 'Red (Tests failed)! Please fix the issues.'} ===")
    sys.exit(exit_code) # Exit with the pytest exit code