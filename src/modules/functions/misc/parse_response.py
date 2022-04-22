# pylint: disable = missing-function-docstring
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
"""


def parse_response(response):
    data, error = None, None
    if response.ok:
        data = response.json()
    else:
        error = response.text

    return data, error
