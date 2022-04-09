# pylint: disable = missing-class-docstring, missing-function-docstring

import unittest
from app import check_api_status_call
import requests
from modules.data.models import *


class Testing(unittest.TestCase):
    def check_api_status_call_test(self):
        name = "pikachu"
        url = "https://pokeapi.co/api/v2/pokemon/" + name + "/"
        response = requests.get(url)
        actual_output = check_api_status_call(response)
        self.assertEqual(200, actual_output)

    def check_database_test(self):
        users = User.query.all()
        if users:
            data = True
        message = "There is no data."
        self.assertTrue(data, message)


if __name__ == "__main__":
    unittest.main()
