# pylint: disable = missing-class-docstring, missing-function-docstring, relative-beyond-top-level
"""
missing-class-docstring: unnecessary, classes are already straightforward
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't seem to like relative imports
"""


### IMPORTS
# third-party
from unittest import main, TestCase
from unittest.mock import MagicMock, patch

# native
from .pokeapi import (
    get_id_from_url,
    # get_pokemon_data,
    search,
)


class TestGetIdFromUrl(TestCase):
    def test_regular_url(self):
        _input = "https://pokeapi.co/api/v2/ability/150/"
        output = get_id_from_url(_input)
        expected_output = 150
        self.assertEqual(output, expected_output)

    def test_url_without_id(self):
        _input = "https://pokeapi.co/api/v2/pokemon/ditto/"
        output = get_id_from_url(_input)
        expected_output = None
        self.assertEqual(output, expected_output)

    def test_bogus_url(self):
        _input = ""
        output = get_id_from_url(_input)
        expected_output = None
        self.assertEqual(output, expected_output)


# class TestGetPokemonData(TestCase):


class TestSearch(TestCase):
    def test_bad_category(self):
        # cheating, can't figure out how to mock without errors
        _input = {"category": "", "search_term": "Typhlosion"}
        # yields "ValueError: Empty module name"
        # mock_response = MagicMock()
        # with patch("pokeapi.get") as mock_requests_get:
        #     mock_requests_get.return_value = mock_response

        output = search(category=_input["category"], search_term=_input["search_term"])
        expected_output = (None, "Invalid category or search term")
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    main()
