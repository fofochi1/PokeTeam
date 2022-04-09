# pylint: disable = missing-class-docstring, missing-function-docstring
"""
Disabled Pylint Warnings & Justifications:
missing-class-docstring: useful, but not necessary (maybe for polishing phase)
missing-function-docstring: useful, but not necessary (maybe for polishing phase)
"""
import unittest
from unittest.mock import MagicMock, patch

from app import is_user_in_db, User


class UserInDBTest(unittest.TestCase):
    def user_set_up(self):
        self.db_mock = [
            User(id="1", email="mockedtest@email.com", name="mockedtest", pic="random")
        ]

    def test_user_in_db_test(self):
        with patch("app.User.query") as mock_query:
            mock_response = MagicMock()
            mock_response.all.return_value = self.db_mock
            mock_query.filter_by.return_value = mock_response

            self.assertEqual(is_user_in_db("mockedtest@email.com"), True)

            mock_response.all.return_value = self.db_mock
            mock_query.filter_by.return_value = mock_response

            self.assertEqual(is_user_in_db("mockedtest99@email.com"), False)


if __name__ == "__main__":
    unittest.main()
