from ..config import config
from ..auth import get_new_token
from ..__version__ import __version__


def get_token():
    """

    Args:

    Returns:

    """
    return get_new_token(
        base_url=config.get("base_url"),
        username=config.get("username"),
        password=config.get("password"),
        grant_type=config.get("grant_type"),
        scope=config.get("scope"),
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret")
    )


auth_headers = {
    "Authorization": get_token(),
    "Accept": "application/json;v=1.0",
    "Content-Type": "application/json;v=1.0",
    "cxOrigin": "Checkmarx Python SDK " + __version__
}


def update_auth_headers():
    auth_headers.update({"Authorization": get_token()})


def get_v2_headers():
    headers = auth_headers.copy()
    headers["Accept"] = "application/json;v=2.0"
    headers["Content-Type"] = "application/json;v=2.0"
    return headers
