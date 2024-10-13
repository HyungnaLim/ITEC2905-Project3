# TODO make requests to Spotify, Bandsintown, Youtube API

# The other students will have the API Imports

import requests
import logging

def get_artist_name(artist_name):

    #error handling

    try:
        response = requests.get() # TODO - insert API for seaching artists name
        if response.status_code == 404: #not found
            return None, f'Music Artist {artist_name} not found' # username will be artist_name
        response.raise_for_status()
        response_json = response.json()
        artist_info = extract_artist_info(response_json)
        return artist_info, None
    except Exception as e:
        logging.exception(e)
        return None, 'Error connecting to API'

def extract_artist_info(json_response): # TODO inset keys that the API will call
    return {
        'login': json_response.get('login'),
    }
