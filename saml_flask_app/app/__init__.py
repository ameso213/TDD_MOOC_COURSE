from flask import Flask


def create_app(config=None):
    app = Flask(__name__, template_folder="../templates")
    app.secret_key = "saml-flask-demo-secret-key-change-in-production"

    # Default config
    app.config["SAML_PATH"] = None  # Will use default saml/ folder next to run.py

    if config:
        app.config.update(config)

    from app.views import saml_bp
    app.register_blueprint(saml_bp)

    return app