# pylint: disable = missing-class-docstring, missing-function-docstring, relative-beyond-top-level
"""
missing-class-docstring: unnecessary, classes are already straightforward
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't seem to like relative imports
"""


### IMPORTS
# third-party
from unittest import main, TestCase

# native
from .pokeapi import (
    get_id_from_url,
    # get_pokemon_data,
    # search
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


# class TestSearch(TestCase):


if __name__ == "__main__":
    main()
