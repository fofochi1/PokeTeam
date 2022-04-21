# pylint: disable = missing-function-docstring, relative-beyond-top-level
"""
Disabled Pylint Warnings & Justifications:
missing-function-docstring: useful, but not necessary; takes up space
relative-beyond-top-level: pylint doesn't seem to like relative imports
"""


### IMPORTS
# third-party
from requests import get

# native
from ..misc.parse_response import parse_response


BASE_URL = "https://pokeapi.co/api/v2/"


def search(**args):
    category = args["category"].lower()
    search_term = args["search_term"].lower()
    response = get(f"{BASE_URL}{category}/{search_term}")
    return parse_response(response)


def get_id_from_url(url):
    return int(url.split("/")[-2])


def get_pokemon_data(pokemon):
    def mapper(_object, **args):
        category = args["category"]
        properties = args["properties"]
        property_mappers = {
            "base_stat": (lambda: _object["base_stat"]),
            "name": (lambda: _object[category]["name"]),
        }
        output = {"id": get_id_from_url(_object[category]["url"])}
        for _property in properties:
            output[_property] = property_mappers[_property]()

        return output

    main_data = {
        "abilities": None,
        "moves": None,
        "species_no": None,
        "sprite": None,
        "stats": None,
        "types": None,
    }
    data, error = search(category="pokemon", search_term=pokemon)
    if error is None:
        main_data["abilities"] = [
            mapper(ability, category="ability", properties=["name"])
            for ability in data["abilities"]
        ]
        main_data["moves"] = [
            mapper(move, category="move", properties=["name"]) for move in data["moves"]
        ]
        main_data["species_no"] = data["id"]
        main_data["sprite"] = data["sprites"]["front_default"]
        main_data["stats"] = [
            mapper(stat, category="stat", properties=["base_stat", "name"])
            for stat in data["stats"]
        ]
        main_data["types"] = [
            mapper(_type, category="type", properties=["name"])
            for _type in data["types"]
        ]
    else:
        pass

    return main_data
