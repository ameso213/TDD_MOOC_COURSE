import hashlib

# Mock database to store user credentials
users_db = {}

def register_user(email, password):
    """Registers a new user after checking for uniqueness."""
    print(f"[AUTH LOGIC] Attempting to register: {email}")
    
    if email in users_db:
        return {"status": "error", "message": "User already exists"}
    
    # In a real app, use a salt! For this example, we use SHA-256.
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users_db[email] = hashed_password
    
    return {"status": "success", "message": "User registered successfully"}

def login_user(email, password):
    """Verifies credentials and 'logs in' the user."""
    print(f"[AUTH LOGIC] Attempting login for: {email}")
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    if users_db.get(email) == hashed_password:
        return {"status": "success", "token": "secure-session-token-123"}
    
    return {"status": "error", "message": "Invalid email or password"}

if __name__ == "__main__":
    print("--- [GREEN PHASE] Manual Auth Logic Test ---")
    
    # Test Registration
    reg = register_user("dev@example.com", "Password123")
    print(f"Registration Result: {reg}")

    # Test Login (Correct)
    log_ok = login_user("dev@example.com", "Password123")
    print(f"Login Success Result: {log_ok}")

    # Test Login (Wrong Password)
    log_fail = login_user("dev@example.com", "WrongPass")
    print(f"Login Failure Result: {log_fail}")