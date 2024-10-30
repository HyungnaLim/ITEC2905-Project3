import requests
import os

def get_token():
    # get environment variables for client credentials from OS
    # client_id = os.environ.get('SPOTIFY_ID')
    # client_secret = os.environ.get('SPOTIFY_SECRET')

    # USE THIS TO TEST WITHOUT USING OS ENV VARIABLES
    client_id = '0c5ba66cb29e46e8a415a35c19033bdd'
    client_secret = '280da5fed992434abc6598b3beadb449'

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    grant_type = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    token_res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=grant_type)
    if token_res.status_code != 200:
        raise Exception(f'could not get valid token, check your client credentials.')

    token_json = token_res.json()
    token_type = token_json['token_type']
    access_token = token_json['access_token']

    return {'Authorization': f'{token_type} {access_token}'}


def get_artist_info(auth, search_artist):
    endpoint = 'https://api.spotify.com/v1/search'
    search_query = {'q': search_artist, 'type': 'artist', 'limit': 3}
    search_res = requests.get(endpoint, params=search_query, headers=auth)

    if search_res.status_code == 401:
        raise Exception('Bad or expired token. Try re-authenticate the user.')
    elif search_res.status_code == 403:
        raise Exception('Bad OAuth request')
    elif search_res.status_code == 429:
        raise Exception('The app has exceeded its rate limits.')

    search_json = search_res.json()

    print(search_json)

    if not search_json.get('artists', {}).get('items'):
        raise Exception('No matching artist found.')

    artist = search_json['artists']['items'][0]
    artist_name = artist['name']
    artist_id = artist['id']
    artist_image_url = artist['images'][0]['url'] if artist['images'] else None
    artist_genres = artist['genres'] if artist['genres'] else ['No genre found for this artist']

    return artist_name, artist_id, artist_image_url, artist_genres


def get_top_tracks_by_artist_id(auth, artist_id):
    tracks_res = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks', headers=auth)
    if tracks_res.status_code == 401:
        raise Exception('Bad or expired token. Try re-authenticate the user.')
    elif tracks_res.status_code == 403:
        raise Exception('Bad OAuth request')
    elif tracks_res.status_code == 429:
        raise Exception('The app has exceeded its rate limits.')

    tracks_json = tracks_res.json()
    print(tracks_json)

    # TODO: error handling for having less than 3 tracks or no track
    tracks = tracks_json.get('tracks', [])
    if not tracks:
        # no top tracks
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
    def __init__(self, artist, image, genres, tracks):
        self.artist = artist
        self.image_url = image
        self.genres = genres
        self.tracks = tracks

    def genres_str(self):
        genres_formatted = ', '.join(self.genres)
        return genres_formatted



def main(search_artist):
    try:
        token = get_token()
        name, id, img_url, genres = get_artist_info(token, search_artist)
        tracks = get_top_tracks_by_artist_id(token, id)
        artist_info = Spotify(name, img_url, genres, tracks)
        return artist_info, None
    except Exception as e:
        return None, f'Spotify API error: {e}'