import requests
import os

"""
This module uses Spotify API to search and get artist data.
Detailed documentation of API: https://developer.spotify.com/documentation/web-api
"""

def get_token():
    """
    SET ENVIRONMENT VARIABLES 'SPOTIFY_ID' AND 'SPOTIFY_SECRET' TO MAKE THIS CODE WORK. (setup guide in README.md)
    Make a request to get an access token using the environment variables from OS.
    Return a token to use Spotify API. Raise exception if the request is not successful.
    """
    # get environment variables for client credentials from OS
    client_id = os.environ.get('SPOTIFY_ID')
    client_secret = os.environ.get('SPOTIFY_SECRET')
    if client_id is None or client_secret is None:
        raise Exception('could not find environment variables, check your OS environment variables')

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    grant_type = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    token_res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=grant_type)
    if token_res.status_code != 200:
        raise Exception('could not get valid token, check your client credentials.')

    token_json = token_res.json()
    token_type = token_json['token_type']
    access_token = token_json['access_token']

    return {'Authorization': f'{token_type} {access_token}'}


def get_artist_info(token, search_artist):
    """
    Make a request to search an artist closest to the user's search term (search_artist) and get artist data from API.
    Raise exception for each error status code, and if API can't find any matching artist.
    Return artist name(str), artist id(str), image url(str), genres(list).
    If no image url or genres found from API response, they will be None.
    """
    endpoint = 'https://api.spotify.com/v1/search'
    search_query = {'q': search_artist, 'type': 'artist', 'limit': 3}
    search_res = requests.get(endpoint, params=search_query, headers=token)

    if search_res.status_code == 401:
        raise Exception('Bad or expired token. Try re-authenticate the user.')
    elif search_res.status_code == 403:
        raise Exception('Bad OAuth request')
    elif search_res.status_code == 429:
        raise Exception('The app has exceeded its rate limits.')

    search_json = search_res.json()

    if not search_json.get('artists', {}).get('items'):
        raise Exception('No matching artist found.')

    artist = search_json['artists']['items'][0]
    artist_name = artist['name']
    artist_id = artist['id']
    artist_image_url = artist['images'][0]['url'] if artist['images'] else None
    artist_genres = artist['genres'] if artist['genres'] else None

    return artist_name, artist_id, artist_image_url, artist_genres


def get_top_tracks_by_artist_id(token, artist_id):
    """
    Request and get top tracks data from API using artist id.
    Raise exception for each error status code.
    Return a list of dictionaries.
    Each dictionary stores data(str) about each track - track title, album title, release date, spotify url
    If less than 3 top tracks are found, only the available tracks are returned.
    If no tracks are found, an empty list is returned.
    """
    tracks_res = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks', headers=token)
    if tracks_res.status_code == 401:
        raise Exception('Bad or expired token. Try re-authenticate the user.')
    elif tracks_res.status_code == 403:
        raise Exception('Bad OAuth request')
    elif tracks_res.status_code == 429:
        raise Exception('The app has exceeded its rate limits.')

    tracks_json = tracks_res.json()
    tracks = tracks_json.get('tracks', [])
    if not tracks:
        return []

    track_collector = []
    for track in tracks[:3]:
        track_dict = {'title': track['name'],
                      'album': track['album']['name'],
                      'release date': track['album']['release_date'],
                      'spotify url': track['external_urls']['spotify']}
        track_collector.append(track_dict)

    return track_collector


class Spotify:
    """
    class to store artist data & genre_str method to display list of genre in a string format
    """
    def __init__(self, artist, image, genres, tracks):
        self.artist = artist
        self.image_url = image
        self.genres = genres
        self.tracks = tracks

    def genres_str(self):
        genres_formatted = ', '.join(self.genres) if self.genres else None
        return genres_formatted



def main(search_artist):
    """
    search and get artist data from Spotify API.
    Return tuple for error handling on app.py
    First item is data retrieved from API (stored in a Spotify class). If exception occurs, this will be None.
    Second item is error message. If exception does not occur, this will be None.
    """
    try:
        token = get_token()
        name, id, img_url, genres = get_artist_info(token, search_artist)
        tracks = get_top_tracks_by_artist_id(token, id)
        artist_info = Spotify(name, img_url, genres, tracks)
        return artist_info, None
    except Exception as e:
        return None, f'Spotify API error: {e}'