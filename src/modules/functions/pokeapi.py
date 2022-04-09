# pylint: disable = missing-function-docstring
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary (maybe for polishing phase)
"""


from requests import get


BASE_URL = "https://pokeapi.co/api/v2/"
ENDPOINTS = ["ability", "move", "pokemon"]
ENDPOINT_ERROR_MESSAGE = "An invalid or prohibited endpoint was provided"


def search(**args):
    endpoint, search_term = args["endpoint"].lower(), args["search_term"].lower()
    # catch invalid/prohibited endpoints before attempting an API call
    if not endpoint in ENDPOINTS:
        return None, ENDPOINT_ERROR_MESSAGE
    response = get(f"{BASE_URL}{endpoint}/{search_term}")
    if response.ok:
        return response.json()

    return None, response.text
