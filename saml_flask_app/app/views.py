import os
from flask import (
    Blueprint,
    request,
    session,
    redirect,
    render_template,
    make_response,
    current_app,
)
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from app.utils import prepare_flask_request

saml_bp = Blueprint("saml", __name__)


def get_saml_auth(req):
    """
    Initializes the SAML Auth object.
    Uses custom SAML_PATH from app config if set,
    otherwise defaults to the saml/ folder beside run.py.
    """
    saml_path = current_app.config.get("SAML_PATH") or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saml"
    )
    return OneLogin_Saml2_Auth(req, custom_base_path=saml_path)



# HOME
@saml_bp.route("/", methods=["GET", "POST"])
def index():
    req = prepare_flask_request(request)
    auth = get_saml_auth(req)
    errors = []
    error_reason = None
    is_authenticated = False
    attributes = {}
    paint_logout = False
    msg = ""

    # ── SSO: Initiate login → redirect to IdP ──
    if "sso" in request.args:
        return redirect(auth.login())

    # ── SSO2: Login with custom RelayState ──
    elif "sso2" in request.args:
        return_to = f"{request.host_url}attrs/"
        return redirect(auth.login(return_to=return_to))

    # ── SLO: Initiate logout → redirect to IdP ──
    elif "slo" in request.args:
        name_id         = session.get("samlNameId")
        name_id_format  = session.get("samlNameIdFormat")
        name_id_nq      = session.get("samlNameIdNameQualifier")
        name_id_spnq    = session.get("samlNameIdSPNameQualifier")
        session_index   = session.get("samlSessionIndex")
        return redirect(
            auth.logout(
                name_id=name_id,
                session_index=session_index,
                nq=name_id_nq,
                name_id_format=name_id_format,
                spnq=name_id_spnq,
            )
        )

    # ── ACS: Handle IdP response after login ──
    elif "acs" in request.args:
        request_id = session.get("AuthNRequestID")
        auth.process_response(request_id=request_id)
        errors = auth.get_errors()

        if errors:
            error_reason = auth.get_last_error_reason()
        else:
            session.pop("AuthNRequestID", None)

            if not auth.is_authenticated():
                msg = "Not authenticated — IdP returned a failed response."
            else:
                # Store SAML user data in session
                session["samlUserdata"]               = auth.get_attributes()
                session["samlNameId"]                 = auth.get_nameid()
                session["samlNameIdFormat"]           = auth.get_nameid_format()
                session["samlNameIdNameQualifier"]    = auth.get_nameid_nq()
                session["samlNameIdSPNameQualifier"]  = auth.get_nameid_spnq()
                session["samlSessionIndex"]           = auth.get_session_index()
                paint_logout = True

                self_url = OneLogin_Saml2_Utils.get_self_url(req)
                relay_state = request.form.get("RelayState", "")

                # Redirect to RelayState only if it differs from current URL
                # and is a trusted local URL (prevents Open Redirect)
                if relay_state and self_url != relay_state and relay_state.startswith(request.host_url):
                    return redirect(relay_state)

                msg = "Successfully authenticated!"

    # ── SLS: Handle IdP logout request/response ──
    elif "sls" in request.args:
        request_id = session.get("LogoutRequestID")

        def delete_session():
            session.clear()

        url = auth.process_slo(
            request_id=request_id,
            delete_session_cb=delete_session,
        )
        errors = auth.get_errors()

        if not errors:
            if url:
                # Validate it's a trusted URL before redirecting
                if url.startswith(request.host_url) or url.startswith("https://idp.example.com"):
                    return redirect(url)
                return redirect("/")
            else:
                msg = "Successfully logged out."
        else:
            error_reason = auth.get_last_error_reason()

    # ── Restore session state for page render ──
    if "samlUserdata" in session:
        paint_logout = True
        if session["samlUserdata"]:
            attributes = session["samlUserdata"]

    return render_template(
        "index.html",
        errors=errors,
        error_reason=error_reason,
        is_authenticated=is_authenticated,
        attributes=attributes,
        paint_logout=paint_logout,
        msg=msg,
    )



# ATTRS: Show logged-in user's SAML attributes
@saml_bp.route("/attrs/")
def attrs():
    paint_logout = "samlUserdata" in session
    attributes = session.get("samlUserdata", {})
    return render_template(
        "attrs.html",
        paint_logout=paint_logout,
        attributes=attributes,
    )



# METADATA: Publish SP metadata XML to IdP

@saml_bp.route("/metadata/")
def metadata():
    saml_path = current_app.config.get("SAML_PATH") or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saml"
    )
    saml_settings = OneLogin_Saml2_Settings(
        custom_base_path=saml_path,
        sp_validation_only=True,
    )
    metadata_xml = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata_xml)

    if errors:
        return make_response(", ".join(errors), 500)

    response = make_response(metadata_xml, 200)
    response.headers["Content-Type"] = "text/xml"
    return response