# pylint: disable = missing-class-docstring, missing-function-docstring
"""
Disabled Pylint Warnings & Justifications:
missing-class-docstring: useful, but not necessary (maybe for polishing phase)
missing-function-docstring: useful, but not necessary (maybe for polishing phase)
"""


from unittest import main, TestCase

# from unittest.mock import MagicMock, patch


from functions.pokeapi import ENDPOINT_ERROR_MESSAGE, search


class TestPokeAPI(TestCase):
    def test_prohibited_endpoint(self):
        # definitely cutting corners with this one; it's "unmocked"
        endpoint = "contest"
        search_term = "Hearthome"
        _, output = search(endpoint=endpoint, search_term=search_term)
        expected_output = ENDPOINT_ERROR_MESSAGE
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    main()
