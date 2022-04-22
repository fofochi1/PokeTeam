# pylint: disable = missing-function-docstring, relative-beyond-top-level
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't seem to like relative imports
"""


### IMPORTS
## third-party
from json import dumps
from oauthlib.oauth2 import WebApplicationClient
from requests import get, post

## native
# data
from ...data.env import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# functions
from ..misc.parse_response import parse_response


GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)  # probably move to different file


def get_client():
    return WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():  # modularize error handling later
    response = get(GOOGLE_DISCOVERY_URL)
    return parse_response(response)


def get_login_request_uri(**args):  # error handling
    base_url = args["base_url"]
    client = get_client()
    google_provider_cfg, _ = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    redirect_uri = f"{base_url}/callback"
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirect_uri,
        scope=["openid", "email", "profile"],
    )
    return request_uri


def get_google_user(**args):  # error handling
    url = args["url"]
    base_url = args["base_url"]
    code = args["code"]
    client = get_client()
    google_provider_cfg, _ = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint, authorization_response=url, redirect_url=base_url, code=code
    )
    token_response = post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(dumps(token_response.json()))  # clean later
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)  # error handling
    google_user = userinfo_response.json()
    return google_user
