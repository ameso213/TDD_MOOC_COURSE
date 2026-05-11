

def calculate_balance(transactions: list) -> float:
    """
    Calculates the net balance from a list of transactions.
    Each transaction: {"amount": float, "type": "income" | "expense"}
    """
    balance = 0.0
    for tx in transactions:
        amount = tx.get("amount", 0.0)
        if amount < 0:
            raise ValueError("Transaction amount cannot be negative")
            
        if tx.get("type") == "income":
            balance += amount
        elif tx.get("type") == "expense":
            balance -= amount
    return round(balance, 2)

def get_category_summary(transactions: list) -> dict:
    """
    Groups total spending by category.
    """
    summary = {}
    for tx in transactions:
        if tx.get("type") == "expense":
            cat = tx.get("category", "Uncategorized")
            summary[cat] = summary.get(cat, 0.0) + tx.get("amount", 0.0)
    
    # Round values for clean display
    return {k: round(v, 2) for k, v in summary.items()}

if __name__ == "__main__":
    # Quick manual verification
    sample_txs = [{"amount": 100.0, "type": "income"}, {"amount": 50.0, "type": "expense", "category": "Food"}]
    print(f"Test Balance: {calculate_balance(sample_txs)}")
    print(f"Test Summary: {get_category_summary(sample_txs)}")