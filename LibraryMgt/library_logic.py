
def can_borrow_book(current_borrow_count: int, book_status: str) -> dict: 
    """
    Business Logic: 
    - Max 3 books per user.
    - Cannot borrow if book is in Maintenance.
    """
    if book_status == "Maintenance":
        return {"allowed": False, "reason": "Book is under maintenance"}
    
    if current_borrow_count >= 3:
        return {"allowed": False, "reason": "Borrowing limit reached (3 books)"}
    
    return {"allowed": True, "reason": "Success"}
    pass

def calculate_fine(days_overdue: int) -> float: 
    """
    Business Logic: $1.00 fine per day overdue.
    """
    if days_overdue <= 0:
        return 0.0
    return float(days_overdue * 1.0)
    pass

if __name__ == "__main__":
    
    
    # Quick manual verification
    print(f"Test Maintenance: {can_borrow_book(0, 'Maintenance')}")
    print(f"Test Limit: {can_borrow_book(3, 'Available')}")
    print(f"Test OK: {can_borrow_book(1, 'Available')}")
    print(f"Test Fine (5 days): ${calculate_fine(5)}")