# 08_FixingBugsTestFirst.py
# Real-life example: Fixing a null pointer exception in a user profile loader.

def load_user_profile(user_id):
    # Bug: No check for None
    profile = get_user_from_db(user_id)
    return profile["name"]  # KeyError if profile is None

def get_user_from_db(user_id):
    # Simulate DB
    return {"name": "John"} if user_id == 1 else None

# Test reproducing bug
# def test_load_profile_none():
#     with pytest.raises(KeyError):  # Or TypeError in real null
#         load_user_profile(2)

# Fix
def load_user_profile(user_id):
    profile = get_user_from_db(user_id)
    if profile is None:
        raise ValueError("User not found")
    return profile["name"]

# Real-life example: Correcting a calculation error in tax software.

def calculate_tax(income):
    # Bug: Wrong formula
    return income * 0.1  # Should be 0.2 for high income

# Test reproducing
# def test_calculate_tax():
#     assert calculate_tax(1000) == 200  # Fails, was 100

# Fix
def calculate_tax(income):
    return income * 0.2