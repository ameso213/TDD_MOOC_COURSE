# 01_WhatIsLegacyCode.py
# Real-life example: Banking application with core transaction logic written 10 years ago, untouched because no tests exist.
# This function processes a bank transfer without any tests, making changes risky.

def process_bank_transfer(amount, from_account, to_account):
    # Simulate checking balance (no error handling)
    if amount > 1000:  # Arbitrary limit
        print("Transfer approved")
        return True
    else:
        print("Transfer denied")
        return False

# Usage (no tests, so hard to verify)
# process_bank_transfer(500, "acc1", "acc2")  # Should work
# process_bank_transfer(1500, "acc1", "acc2")  # Should fail, but no tests to confirm

# Real-life example: E-commerce site's payment processing module inherited from a previous team.
# Adding a new payment method requires manual testing.

def process_payment(amount, payment_method):
    if payment_method == "credit_card":
        # Simulate processing
        return f"Processed ${amount} via credit card"
    elif payment_method == "paypal":
        return f"Processed ${amount} via PayPal"
    else:
        return "Unsupported payment method"