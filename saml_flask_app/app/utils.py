from urllib.parse import urlparse


def prepare_flask_request(request):
    """
    Maps a Flask request object to the dict format
    expected by the python3-saml toolkit.
    """
    url_data = urlparse(request.url)
    return {
        "https": "on" if request.scheme == "https" else "off",
        "http_host": request.host,
        "server_port": url_data.port,
        "script_name": request.path,
        "get_data": request.args.copy(),
        "post_data": request.form.copy(),
    }