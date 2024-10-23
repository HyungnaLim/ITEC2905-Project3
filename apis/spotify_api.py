import requests

def get_token():
    # TODO: set client credentials as environment variables
    client_id = '0c5ba66cb29e46e8a415a35c19033bdd'
    client_secret = '280da5fed992434abc6598b3beadb449'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    grant_type = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}

    json_res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=grant_type).json()

    token_type = json_res['token_type']
    access_token = json_res['access_token']

    token_str = f'{token_type} {access_token}'
    auth = {'Authorization': token_str}

    return auth


def get_artist_info(auth, search_artist):
    endpoint = 'https://api.spotify.com/v1/search'

    search_query = {'q': search_artist, 'type': 'artist', 'limit': 3}

    search_response = requests.get(endpoint, params=search_query, headers=auth).json()

    artist_name = search_response['artists']['items'][0]['name']
    artist_id = search_response['artists']['items'][0]['id']
    artist_image_url = search_response['artists']['items'][0]['images'][0]['url']
    artist_genres = search_response['artists']['items'][0]['genres']

    return artist_name, artist_id, artist_image_url, artist_genres


def get_top_tracks_by_artist_id(auth, artist_id):
    json_res = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks',
                                          headers=auth).json()
    tracks = json_res['tracks']

    track_collector = []

    for i, track in enumerate(tracks):
        if i >= 3:  # Stop after the third item
            break

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

    def __str__(self):
        return f'{self.artist}, {self.image_url}, {self.genres}, {self.tracks}'

    def genres_str(self):
        genres_formatted = ', '.join(self.genres)
        return genres_formatted



def main(search_artist):
    token = get_token()
    name, id, img_url, genres = get_artist_info(token, search_artist)
    tracks = get_top_tracks_by_artist_id(token, id)

    artist_info = Spotify(name, img_url, genres, tracks)

    return artist_info