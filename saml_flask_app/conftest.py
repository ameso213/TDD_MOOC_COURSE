import os
import pytest
from app import create_app

SAML_PATH = os.path.join(os.path.dirname(__file__), "saml")


@pytest.fixture
def app():
    """Create a test Flask app instance."""
    test_app = create_app(
        config={
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "SAML_PATH": os.path.abspath(SAML_PATH),
            "WTF_CSRF_ENABLED": False,
        }
    )
    return test_app


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Flask test CLI runner."""
    return app.test_cli_runner()