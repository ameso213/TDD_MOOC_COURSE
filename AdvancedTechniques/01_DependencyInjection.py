from typing import Protocol

# Advanced Technique: Dependency Inversion using Protocols
# This decouples high-level business logic from low-level infrastructure (like APIs).

class PaymentGateway(Protocol):
    """An interface for payment processing."""
    def process_payment(self, amount: float) -> bool:
        ...

class StripeService:
    """A concrete implementation for production."""
    def process_payment(self, amount: float) -> bool:
        print(f"Contacting Stripe API to charge ${amount}...")
        return True

class OrderManager:
    """Business logic that depends on the abstraction, not the implementation."""
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def complete_order(self, total: float):
        if total <= 0:
            raise ValueError("Invalid order total")
        return self.gateway.process_payment(total)

# --- Testing Logic ---

class MockPaymentGateway:
    """A test double to verify behavior without hitting a real API."""
    def __init__(self):
        self.was_called = False

    def process_payment(self, amount: float) -> bool:
        self.was_called = True
        return True

def test_order_manager_executes_payment():
    mock = MockPaymentGateway()
    manager = OrderManager(mock)
    assert manager.complete_order(50.0) is True
    assert mock.was_called is True