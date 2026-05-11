# 06_CodeCoverage.py
# Real-life example: A CI/CD pipeline uses line coverage to ensure 80% of code is tested,
# but branch coverage reveals untested error paths.

def validate_input(value):
    if value > 0:
        return "Valid"
    else:
        return "Invalid"

# Tests for line coverage (100% lines, but misses else if value <=0 not tested fully)
# def test_validate_positive():
#     assert validate_input(1) == "Valid"

# For branch coverage, add:
# def test_validate_negative():
#     assert validate_input(-1) == "Invalid"

# Real-life example: Mutation testing on a financial calculation library catches tests that don't verify edge cases.

def calculate_interest(principal, rate):
    if rate > 0:
        return principal * rate
    else:
        return 0

# Mutation might change > to >=, and tests should fail if not covered.
# Tests:
# def test_positive_rate():
#     assert calculate_interest(100, 0.1) == 10
# def test_zero_rate():
#     assert calculate_interest(100, 0) == 0  # Covers else

# Without the second test, mutation rate >=0 might not be caught.