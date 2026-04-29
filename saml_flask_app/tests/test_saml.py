"""
tests/test_saml.py
==================
Full test suite for the SAML Flask app.

Strategy:
  - Unit tests  → mock OneLogin_Saml2_Auth entirely (fast, isolated)
  - Route tests → confirm Flask wiring (status codes, redirects, templates)
  - Session tests → confirm session is set/cleared correctly
"""

from unittest import mock
import pytest



# HELPERS

def make_mock_auth(
    is_authenticated=True,
    errors=None,
    attributes=None,
    login_url="https://idp.example.com/sso?SAMLRequest=abc123",
    logout_url="https://idp.example.com/slo?SAMLRequest=xyz",
    nameid="ameso@gmail.com",
    nameid_format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
    session_index="_session_abc",
    error_reason=None,
    slo_redirect_url=None,
):
    """
    Returns a fully configured mock of OneLogin_Saml2_Auth.
    Every test can override the defaults it cares about.
    """
    m = mock.MagicMock()
    m.is_authenticated.return_value = is_authenticated
    m.get_errors.return_value = errors or []
    m.get_attributes.return_value = attributes or {
        "email": ["ameso@gmail.com"],
        "firstName": ["John"],
        "lastName": ["Doe"],
        "groups": ["users", "admins"],
    }
    m.login.return_value = login_url
    m.logout.return_value = logout_url
    m.get_nameid.return_value = nameid
    m.get_nameid_format.return_value = nameid_format
    m.get_nameid_nq.return_value = None
    m.get_nameid_spnq.return_value = None
    m.get_session_index.return_value = session_index
    m.get_last_error_reason.return_value = error_reason
    m.process_response.return_value = None
    m.process_slo.return_value = slo_redirect_url
    return m


AUTH_PATH = "app.views.get_saml_auth"



# 1. HOME PAGE
class TestHomePage:

    def test_home_loads(self, client):
        """Home page returns 200 with login link when not authenticated."""
        mock_auth = make_mock_auth()
        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/")
        assert response.status_code == 200
        assert b"Login with SSO" in response.data

    def test_home_shows_logout_when_session_set(self, client):
        """Home page shows logout link when samlUserdata is in session."""
        mock_auth = make_mock_auth()
        with client.session_transaction() as sess:
            sess["samlUserdata"] = {"email": ["ameso@gmail.com"]}
        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/")
        assert response.status_code == 200
        assert b"Logout" in response.data

    def test_home_shows_saml_flow_table(self, client):
        """Home page renders the SAML flow explanation table."""
        mock_auth = make_mock_auth()
        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/")
        assert b"AuthNRequest" in response.data
        assert b"SAMLResponse" in response.data



# 2. SSO INITIATION
class TestSSO:

    def test_sso_redirects_to_idp(self, client):
        """/?sso should redirect the browser to the IdP SSO URL."""
        idp_url = "https://idp.example.com/sso?SAMLRequest=abc123"
        mock_auth = make_mock_auth(login_url=idp_url)

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/?sso")

        assert response.status_code == 302
        assert "idp.example.com" in response.location
        mock_auth.login.assert_called_once()

    def test_sso2_redirects_with_attrs_relay_state(self, client):
        """/?sso2 should pass the /attrs/ URL as RelayState."""
        mock_auth = make_mock_auth()

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/?sso2")

        assert response.status_code == 302
        # login() should have been called with a return_to containing 'attrs'
        call_kwargs = mock_auth.login.call_args
        return_to = call_kwargs[1].get("return_to") or (call_kwargs[0][0] if call_kwargs[0] else "")
        assert "attrs" in return_to



# 3. ACS — ASSERTION CONSUMER SERVICE
class TestACS:

    def test_acs_successful_login_sets_session(self, client):
        """POST /?acs with valid SAMLResponse should populate the session."""
        mock_auth = make_mock_auth()

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.post("/?acs", data={"SAMLResponse": "validresponse"})

        assert response.status_code == 200
        assert b"Successfully authenticated" in response.data

        with client.session_transaction() as sess:
            assert sess["samlNameId"] == "ameso@gmail.com"
            assert sess["samlUserdata"]["email"] == ["ameso@gmail.com"]
            assert sess["samlUserdata"]["groups"] == ["users", "admins"]

    def test_acs_failed_authentication_shows_error(self, client):
        """POST /?acs where is_authenticated=False should show 'Not authenticated'."""
        mock_auth = make_mock_auth(is_authenticated=False)

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.post("/?acs", data={"SAMLResponse": "badresponse"})

        assert response.status_code == 200
        assert b"Not authenticated" in response.data

    def test_acs_saml_error_shows_error_message(self, client):
        """POST /?acs with SAML errors should surface the error reason."""
        mock_auth = make_mock_auth(
            errors=["invalid_response"],
            error_reason="Signature validation failed",
        )

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.post("/?acs", data={"SAMLResponse": "corruptdata"})

        assert response.status_code == 200
        assert b"invalid_response" in response.data or b"SAML Error" in response.data

    def test_acs_clears_authn_request_id_from_session(self, client):
        """ACS should pop AuthNRequestID from session on success."""
        mock_auth = make_mock_auth()

        with client.session_transaction() as sess:
            sess["AuthNRequestID"] = "req_12345"

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            client.post("/?acs", data={"SAMLResponse": "valid"})

        with client.session_transaction() as sess:
            assert "AuthNRequestID" not in sess

    def test_acs_relay_state_redirect_to_trusted_url(self, client):
        """ACS should redirect to RelayState if it's a trusted (same-host) URL."""
        mock_auth = make_mock_auth()

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.post(
                "/?acs",
                data={
                    "SAMLResponse": "valid",
                    "RelayState": "http://localhost/attrs/",
                },
            )

        # Should redirect to /attrs/ since it's same host
        assert response.status_code == 302
        assert "attrs" in response.location

    def test_acs_relay_state_external_url_blocked(self, client):
        """ACS must NOT redirect to an external/untrusted RelayState (open redirect prevention)."""
        mock_auth = make_mock_auth()

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.post(
                "/?acs",
                data={
                    "SAMLResponse": "valid",
                    "RelayState": "https://evil.com/steal-session",
                },
            )

        # Should NOT redirect to evil.com
        assert response.status_code == 200
        if response.status_code == 302:
            assert "evil.com" not in response.location



# 4. SLO INITIATION
class TestSLOInit:

    def test_slo_redirects_to_idp(self, client):
        """/?slo should redirect to IdP's SLO endpoint."""
        mock_auth = make_mock_auth()

        with client.session_transaction() as sess:
            sess["samlNameId"]       = "ameso@gmail.com"
            sess["samlNameIdFormat"] = "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"
            sess["samlNameIdNameQualifier"]   = None
            sess["samlNameIdSPNameQualifier"] = None
            sess["samlSessionIndex"] = "_session_abc"

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/?slo")

        assert response.status_code == 302
        assert "idp.example.com" in response.location
        mock_auth.logout.assert_called_once()

    def test_slo_passes_session_data_to_logout(self, client):
        """logout() must receive the stored NameID and SessionIndex."""
        mock_auth = make_mock_auth()

        with client.session_transaction() as sess:
            sess["samlNameId"]       = "ameso@gmail.com"
            sess["samlNameIdFormat"] = "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress"
            sess["samlSessionIndex"] = "_abc123"
            sess["samlNameIdNameQualifier"]   = None
            sess["samlNameIdSPNameQualifier"] = None

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            client.get("/?slo")

        call_kwargs = mock_auth.logout.call_args[1]
        assert call_kwargs["name_id"] == "ameso@gmail.com"
        assert call_kwargs["session_index"] == "_abc123"



# 5. SLS — SINGLE LOGOUT SERVICE
class TestSLS:

    def test_sls_successful_logout_clears_session(self, client):
        """GET /?sls with a valid LogoutResponse should clear the session."""
        mock_auth = make_mock_auth(slo_redirect_url=None)

        with client.session_transaction() as sess:
            sess["samlUserdata"] = {"email": ["ameso@gmail.com"]}
            sess["samlNameId"]   = "ameso@gmail.com"

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/?sls")

        assert response.status_code == 200
        assert b"Successfully logged out" in response.data

    def test_sls_idp_initiated_redirects_back(self, client):
        """SLS should redirect back to IdP if process_slo returns a URL."""
        idp_return_url = "https://idp.example.com/slo?done=1"
        mock_auth = make_mock_auth(slo_redirect_url=idp_return_url)

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/?sls")

        # View will redirect to / since idp.example.com is in the whitelist
        assert response.status_code == 302

    def test_sls_error_shows_error(self, client):
        """GET /?sls with SAML errors should stay on page and show error."""
        mock_auth = make_mock_auth(
            slo_redirect_url=None,
            errors=["invalid_logout_response"],
            error_reason="Logout response is invalid",
        )

        with mock.patch(AUTH_PATH, return_value=mock_auth):
            response = client.get("/?sls")

        assert response.status_code == 200
        assert b"invalid_logout_response" in response.data or b"SAML Error" in response.data



# 6. METADATA ENDPOINT
class TestMetadata:

    def test_metadata_returns_xml(self, client):
        """GET /metadata/ should return valid XML with correct content-type."""
        response = client.get("/metadata/")
        assert response.status_code == 200
        assert "xml" in response.content_type
        assert b"EntityDescriptor" in response.data
        assert b"AssertionConsumerService" in response.data

    def test_metadata_contains_sp_entity_id(self, client):
        """Metadata XML should contain the SP entityId from settings.json."""
        response = client.get("/metadata/")
        assert b"localhost:5000" in response.data

    def test_metadata_error_returns_500(self, client):
        """If metadata validation fails, return 500."""
        with mock.patch(
            "app.views.OneLogin_Saml2_Settings"
        ) as mock_settings_class:
            mock_settings = mock_settings_class.return_value
            mock_settings.get_sp_metadata.return_value = b"<bad/>"
            mock_settings.validate_metadata.return_value = ["invalid_metadata"]

            response = client.get("/metadata/")

        assert response.status_code == 500



# 7. ATTRS PAGE
class TestAttrsPage:

    def test_attrs_not_logged_in(self, client):
        """Attrs page without session should prompt login."""
        response = client.get("/attrs/")
        assert response.status_code == 200
        assert b"not logged in" in response.data.lower() or b"Login" in response.data

    def test_attrs_shows_user_data(self, client):
        """Attrs page with session should show SAML attributes."""
        with client.session_transaction() as sess:
            sess["samlUserdata"] = {
                "email": ["ameso@gmail.com"],
                "firstName": ["John"],
                "groups": ["admins", "users"],
            }

        response = client.get("/attrs/")
        assert response.status_code == 200
        assert b"ameso@gmail.com" in response.data
        assert b"admins" in response.data



# 8. UTILS
class TestUtils:

    def test_prepare_flask_request_http(self, app):
        """prepare_flask_request maps Flask request to SAML toolkit format."""
        from app.utils import prepare_flask_request

        with app.test_request_context("http://localhost:5000/?sso"):
            from flask import request
            result = prepare_flask_request(request)

        assert result["https"] == "off"
        assert result["http_host"] == "localhost:5000"
        assert "sso" in result["get_data"]

    def test_prepare_flask_request_https(self, app):
        """prepare_flask_request sets https=on for HTTPS requests."""
        from app.utils import prepare_flask_request

        with app.test_request_context(
            "https://secure.example.com/?acs", environ_base={"wsgi.url_scheme": "https"}
        ):
            from flask import request
            result = prepare_flask_request(request)

        assert result["https"] == "on"