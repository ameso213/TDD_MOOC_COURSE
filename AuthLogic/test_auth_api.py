import pytest
from AuthLogic.auth_main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_full_auth_flow(client):
    print("\n--- [WALKING SKELETON] Testing Registration and Login Flow ---")
    
    # 1. Register a user
    reg_payload = {"email": "test@test.com", "password": "password123"}
    reg_response = client.post("/register", json=reg_payload)
    assert reg_response.status_code == 201
    assert reg_response.get_json()["status"] == "success"

    # 2. Login with correct credentials
    login_payload = {"email": "test@test.com", "password": "password123"}
    login_response = client.post("/login", json=login_payload)
    assert login_response.status_code == 200
    assert "token" in login_response.get_json()

    # 3. Login with wrong password
    wrong_payload = {"email": "test@test.com", "password": "WRONG"}
    wrong_response = client.post("/login", json=wrong_payload)
    assert wrong_response.status_code == 401

if __name__ == "__main__":
    pytest.main(["-s", __file__])