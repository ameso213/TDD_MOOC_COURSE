# 09_AddingNewFeaturesTestFirst.py
# Real-life example: Adding OAuth login to a legacy app.
# TDD the OAuth module separately.

class AuthService:
    def login(self, username, password):
        # Legacy logic
        if username == "admin":
            return True
        return False

# New feature: OAuth
class OAuthHandler:
    def authenticate(self, token):
        # TDD this first
        return token == "valid_token"

# Integrate
class EnhancedAuthService(AuthService):
    def __init__(self):
        self.oauth = OAuthHandler()

    def login_oauth(self, token):
        return self.oauth.authenticate(token)

# Tests for OAuth first
# def test_oauth_valid():
#     handler = OAuthHandler()
#     assert handler.authenticate("valid_token")

# Real-life example: Implementing a new search filter in an e-commerce site.

class ProductSearch:
    def search(self, products, query):
        # Legacy: exact match
        return [p for p in products if query in p["name"]]

# New feature: Filter by category
def filter_by_category(products, category):
    return [p for p in products if p["category"] == category]

# TDD filter_by_category first
# def test_filter_category():
#     products = [{"name": "Apple", "category": "fruit"}]
#     assert filter_by_category(products, "fruit") == products

# Integrate
class EnhancedProductSearch(ProductSearch):
    def search_with_filter(self, products, query, category=None):
        results = self.search(products, query)
        if category:
            results = filter_by_category(results, category)
        return results