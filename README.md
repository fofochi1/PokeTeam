# The Pokédex

## Deployed App
Try the app on Heroku [here](https://fathomless-inlet-43045.herokuapp.com/)!


## Description
Powered by the PokéAPI, **The Pokédex** allows users to search for Pokémon by name and add (or remove) up to 6 Pokémon onto a personal team that they can view.\
Users must sign in with a Google account.


### Technologies
This app uses Flask, HTML, CSS and Jinja, SQLAlchemy


### Libraries
os, requests, python-dotenv, Flask, Flask-Login, Flask-SQLAlchemy, OAuth


### APIs
[Google OAuth](https://console.cloud.google.com/)
[PokéAPI](https://pokeapi.co/)

#### Instructions
- You will need a Google Client ID and Google Client Secret ID from the Google API to be able to use Google Sign In.
- You will need the URL to a remote PostgreSQL database.
- All Python library installation requirements are included in `requirements.txt` and can be installed with:\
`pip install -r requirements.txt`\
- A `.env` file can be used to store the following environment variables:
```
APP_SECRET_KEY
DATABASE_URL
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
```

### Authors (Section 002)
Eric Burch\
Alfonso Buzeta Borquez\
Ivan Garcia\
Brian Williams