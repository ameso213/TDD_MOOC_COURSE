# 11_ToInfinityAndBeyond.py

"""
1. THE FIRST 200 HOURS: FOCUS ON NAMING
Note: In the beginning, don't worry about complex architectures. Focus on 
descriptive test names that explain "why" and "what," not "how."
Real-life: A "String Calculator" kata where the tests read like a specification.
"""
import pytest

# Good Naming: The test name describes the business rule.
def test_should_return_zero_when_input_is_empty_string():
    assert add("") == 0

def test_should_sum_two_comma_separated_numbers():
    assert add("1,2") == 3

def add(numbers):
    if not numbers:
        return 0
    return sum(int(n) for n in numbers.split(","))


"""
2. THE 10-YEAR JOURNEY: WRITING TESTABLE CODE
Note: Mastery involves decoupling your core logic from "hard" things like 
Flask, Databases, or APIs. This makes your logic "pure" and easy to test.
Real-life: Separating Flask route logic from the actual Business Logic.
"""
from flask import Flask, request, jsonify

# --- THE DOMAIN (Pure Logic - 100% testable without Flask) ---
class DiscountCalculator:
    def apply_discount(self, total, discount_code):
        if discount_code == "SUMMER20":
            return total * 0.8
        return total

# --- THE INFRASTRUCTURE (Flask - Thin wrapper) ---
app = Flask(__name__)
calculator = DiscountCalculator()

@app.route("/calculate", methods=["POST"])
def calculate_endpoint():
    data = request.json
    # We delegate logic to the testable class
    result = calculator.apply_discount(data["total"], data["code"])
    return jsonify({"final_total": result})


"""
3. TRANSFORMING LEGACY PROJECTS
Note: Applying "Characterization Tests" to old code to make it as safe 
to work with as a brand-new project.
Real-life: Wrapping a 500-line "spaghetti" function in tests before refactoring.
"""
def legacy_shipping_logic(weight, destination):
    # Imagine 100 lines of messy, untested code here
    if destination == "UK":
        return weight * 2
    return weight * 5

# The Mastery approach: Capture current behavior first
def test_characterize_legacy_shipping():
    assert legacy_shipping_logic(10, "UK") == 20
    assert legacy_shipping_logic(10, "US") == 50


"""
4. SIMPLE DESIGN: REMOVING DUPLICATION
Note: Based on Corey Haines' "Four Rules of Simple Design." 
1. Passes tests, 2. Reveals intent, 3. No duplication, 4. Fewest elements.
Real-life: Refactoring redundant validation logic into a reusable decorator.
"""
def validate_positive(func):
    def wrapper(value):
        if value < 0:
            raise ValueError("Value must be positive")
        return func(value)
    return wrapper

@validate_positive
def process_payment(amount):
    return f"Processing ${amount}"

@validate_positive
def update_stock(quantity):
    return f"Stock updated to {quantity}"


"""
5. SUSTAINABLE DESIGN (THE TEST OF TIME)
Note: Writing code that someone (including yourself) can understand 
two years later. 
Real-life: Using Type Hinting and clear abstractions so the "Design" is self-documenting.
"""
from typing import Protocol

class PaymentProcessor(Protocol):
    def charge(self, amount: float) -> bool:
        ...

class StripeProcessor:
    def charge(self, amount: float) -> bool:
        print(f"Charging {amount} via Stripe")
        return True

def checkout(processor: PaymentProcessor, amount: float):
    # This design survives because it's easy to swap Stripe for PayPal 
    # without changing the checkout logic.
    return processor.charge(amount)

"""
Recommended Reading Checklist:
- Kent Beck: TDD By Example (The Fundamentals)
- Freeman & Pryce: Growing Object-Oriented Software (Mocks & Architecture)
- Robert C. Martin: Clean Code (Readability)
"""