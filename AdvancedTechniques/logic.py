from typing import Protocol

class PaymentGateway(Protocol):  #This is an abstraction that defines the contract that any paymennt processing service must adhere to.
    """An interface for payment processing."""   #This  is an abstract method with no implementations.
    def process_payment(self, amount: float) -> bool:
        ...

class OrderManager: #Hight level module 
    """Business logic that depends on the abstraction, not the implementation."""
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def complete_order(self, total: float) -> bool:
        print(f"\n[OrderManager] Validating business rules for order: ${total}")
        if total <= 0:
            print("[OrderManager] Validation failed: Total must be positive.")
            raise ValueError("Invalid order total")
        
        print("[OrderManager] Validation passed. Delegating to Gateway implementation...")
        return self.gateway.process_payment(total)