from flask import Flask, request, jsonify
from library_logic import can_borrow_book

app = Flask(__name__)

# Mock Database
mock_users = {"user_1": {"borrowed_count": 2}}
mock_books = {"book_1": {"status": "Available"}}

@app.route("/borrow", methods=["POST"])
def borrow():
    data = request.json
    user_id = data.get("user_id")
    book_id = data.get("book_id")

    user = mock_users.get(user_id)
    book = mock_books.get(book_id)

    if not user or not book:
        return jsonify({"error": "User or Book not found"}), 404

    # Delegate to our TDD-verified logic
    check = can_borrow_book(user["borrowed_count"], book["status"])
    
    if not check["allowed"]:
        return jsonify(check), 400

    # In a real app, update DB here
    user["borrowed_count"] += 1
    return jsonify({"status": "success", "message": "Book checked out"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5003)