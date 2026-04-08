# 02_TheFirstStepInRefactoring.py
# Real-life example: Refactoring a monolithic web app's user authentication logic.
# Without tests, developers hesitate to extract methods or classes.

def authenticate_user(username, password):
    # Hardcoded logic, no separation of concerns
    if username == "admin" and password == "pass":
        return "Login successful"
    else:
        return "Login failed"

# To refactor safely, add tests first
import pytest

def test_authenticate_admin():
    assert authenticate_user("admin", "pass") == "Login successful"

def test_authenticate_invalid():
    assert authenticate_user("admin", "wrong") == "Login failed"

# After tests, refactor to extract logic
class AuthenticationService:
    def __init__(self, valid_username="admin", valid_password="pass"):
        self.valid_username = valid_username
        self.valid_password = valid_password

    def authenticate(self, username, password):
        if self.is_valid_credentials(username, password):
            return "Login successful"
        else:
            return "Login failed"

    def is_valid_credentials(self, username, password):
        return username == self.valid_username and password == self.valid_password

# Tests still pass with refactored code
def test_auth_service_admin():
    service = AuthenticationService()
    assert service.authenticate("admin", "pass") == "Login successful"

def test_auth_service_invalid():
    service = AuthenticationService()
    assert service.authenticate("admin", "wrong") == "Login failed"

# ============================================================================

# Real-life example: Improving a data processing pipeline in a data analytics firm.
# Tests ensure optimizations don't alter output.

# LEGACY (without tests - risky to change)
def process_data_pipeline(data):
    # Simulate processing steps
    cleaned = [x.strip() for x in data]
    filtered = [x for x in cleaned if len(x) > 3]
    return sum(len(x) for x in filtered)

# TO REFACTOR SAFELY, ADD TESTS FIRST
def test_process_pipeline_basic():
    data = ["apple ", " banana", "kiwi", "x"]
    assert process_data_pipeline(data) == 15  # apple(5) + banana(6) + kiwi(4)

def test_process_pipeline_all_short():
    data = ["a", "b", "c"]
    assert process_data_pipeline(data) == 0

def test_process_pipeline_mixed():
    data = ["  hello  ", "hi", "world"]
    assert process_data_pipeline(data) == 10  # hello(5) + world(5)

# REFACTORED (with extracted methods for testability)
class DataPipeline:
    def process(self, data):
        cleaned = self.clean_data(data)
        filtered = self.filter_data(cleaned)
        return self.calculate_total(filtered)

    def clean_data(self, data):
        return [x.strip() for x in data]

    def filter_data(self, data):
        return [x for x in data if len(x) > 3]

    def calculate_total(self, data):
        return sum(len(x) for x in data)

# Tests for refactored version
def test_pipeline_basic():
    pipeline = DataPipeline()
    data = ["apple ", " banana", "kiwi", "x"]
    assert pipeline.process(data) == 15

def test_pipeline_clean():
    pipeline = DataPipeline()
    data = ["  hello  ", "  world  "]
    assert pipeline.clean_data(data) == ["hello", "world"]

def test_pipeline_filter():
    pipeline = DataPipeline()
    data = ["hello", "hi", "world", "x"]
    assert pipeline.filter_data(data) == ["hello", "world"]

def test_pipeline_calculate():
    pipeline = DataPipeline()
    data = ["apple", "banana"]
    assert pipeline.calculate_total(data) == 11
