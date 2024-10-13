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


def get_artist_id(auth):
    endpoint = 'https://api.spotify.com/v1/search'
    artist = input('Enter artist name: ')

    search_query = {'q': artist, 'type': 'artist', 'limit': 3}

    search_response = requests.get(endpoint, params=search_query, headers=auth).json()

    artist_name = search_response['artists']['items'][0]['name']
    artist_id = search_response['artists']['items'][0]['id']

    print(f'Searched artist is ... "{artist_name}"')
    # TODO: maybe display more artist info

    return artist_name, artist_id


def get_top_tracks_by_artist_id(auth, artist_id):
    json_res = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks',
                                          headers=auth).json()
    tracks = json_res['tracks']
    track_ids = []
    for tracks in tracks:
        track_ids.append(tracks['id'])

    return track_ids


def get_track_info_by_track_id(auth, artist_name, track_ids):
    print(f'\nTop Tracks of {artist_name}')

    track_collector = []

    for track_id in track_ids:
        json_res = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=auth).json()

        track_title = json_res['name']
        album_title = json_res['album']['name']
        release_date = json_res['album']['release_date']
        spotify_url = json_res['external_urls']['spotify']

        track_collector.append(track_title)

        print(f'{track_title} [{album_title}] {release_date} {spotify_url}')

    return track_collector


class Spotify:
    def __init__(self, artist):
        self.artist = artist
        self.tracks = []



def main():
    token = get_token()
    Spotify.artist, artist_id = get_artist_id(token)
    track_ids = get_top_tracks_by_artist_id(token, artist_id)
    Spotify.tracks = get_track_info_by_track_id(token, Spotify.artist, track_ids)



if __name__ == '__main__':
    main()


# TODO
#  - test more features from Spotify API. maybe related artist?
#  - exception/error handling