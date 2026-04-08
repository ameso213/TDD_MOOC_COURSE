from flask import Flask, request, jsonify
from AuthLogic.auth_logic import register_user, login_user

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    print("[API] Registration request received.")
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400
        
    result = register_user(email, password)
    status_code = 201 if result["status"] == "success" else 400
    return jsonify(result), status_code

@app.route("/login", methods=["POST"])
def login():
    print("[API] Login request received.")
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    result = login_user(email, password)
    status_code = 200 if result["status"] == "success" else 401
    return jsonify(result), status_code

@app.route("/", methods=["GET"])
def index():
    return """
    <h1>Auth System API</h1>
    <p>Endpoints: <code>/register</code> and <code>/login</code> (POST)</p>
    """

if __name__ == "__main__":
    # Running on port 5002 to avoid conflicts
    app.run(debug=True, port=5002)