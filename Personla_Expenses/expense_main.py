from flask import Flask, request, jsonify
from expense_logic import calculate_balance, get_category_summary

app = Flask(__name__)

# In-memory storage for transactions.
transactions = []

@app.route("/transaction", methods=["POST"])
def add_transaction():
    data = request.get_json()
    
    # Basic validation
    if not data.get("amount") or not data.get("type"):
        return jsonify({"error": "Missing amount or type"}), 400

    # Add to our "database"
    transactions.append({
        "amount": float(data["amount"]),
        "type": data["type"],
        "category": data.get("category", "General")
    })
    
    return jsonify({"message": "Transaction recorded"}), 201

@app.route("/summary", methods=["GET"])
def get_summary():
    try:
        current_balance = calculate_balance(transactions)
        category_totals = get_category_summary(transactions)
        
        return jsonify({
            "balance": current_balance,
            "by_category": category_totals
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Running on port 5004
    print("Starting Expense Tracker API on port 5004...")
    app.run(debug=True, port=5004)