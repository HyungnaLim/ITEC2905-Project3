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
    artist_genres = search_response['artists']['items'][0]['genres']
    artist_image_url = search_response['artists']['items'][0]['images'][0]['url']

    print(f'Searched artist is ... "{artist_name}"')
    print(f'Genre: {', '.join(artist_genres)}')

    return artist_name, artist_id, artist_image_url


def get_top_tracks_by_artist_id(auth, artist_id):
    json_res = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks',
                                          headers=auth).json()
    tracks = json_res['tracks']
    track_collector = []

    for i, track in enumerate(tracks):
        if i >= 3:  # Stop after the third item
            break
        track_title = track['name']
        album_title = track['album']['name']
        release_date = track['album']['release_date']
        spotify_url = track['external_urls']['spotify']

        track_collector.append(track_title)

        print(f'{track_title} [{album_title}] {release_date} {spotify_url}')

    return track_collector


class Spotify:
    def __init__(self, artist, image):
        self.artist = artist
        self.image_url = image
        self.tracks = []



def main():
    token = get_token()
    Spotify.artist, artist_id, Spotify.image_url = get_artist_id(token)
    Spotify.tracks = get_top_tracks_by_artist_id(token, artist_id)



if __name__ == '__main__':
    main()


# TODO
#  - test more features from Spotify API. maybe related artist?
#  - exception/error handling