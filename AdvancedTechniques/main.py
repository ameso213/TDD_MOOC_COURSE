from logic import OrderManager

class StripeService:
    """A concrete implementation for production."""
    def process_payment(self, amount: float) -> bool:
        # In a real app, this would use the 'stripe' python library
        print(f"[StripeService] Network call: Authorizing ${amount} via Stripe API...")
        return True

if __name__ == "__main__":
    print("=== Production Application Starting ===")
    # Dependency Injection: We 'inject' the real Stripe service into the manager
    stripe = StripeService()
    manager = OrderManager(stripe)
    
    success = manager.complete_order(100.0)
    print(f"=== Order Result: {'Success' if success else 'Failed'} ===")