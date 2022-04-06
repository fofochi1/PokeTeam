""" Imports the .env file from os """
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Configurations
GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
