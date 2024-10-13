import requests
import os
import api.youtube_api as get_video


def get_token():
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    grant_type = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}

    json_res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=grant_type).json()

    token_type = json_res.get('token_type')
    access_token = json_res.get('access_token')

    token_str = f'{token_type} {access_token}'
    auth = {'Authorization': token_str}

    return auth


def get_artist_id(auth, artist_search_term):
    endpoint = 'https://api.spotify.com/v1/search'

    search_query = {'q': artist_search_term, 'type': 'artist', 'limit': 3}
    search_response = requests.get(endpoint, params=search_query, headers=auth).json()
    artist = search_response.get('artists')

    artist_name = artist['items'][0]['name']
    artist_id = artist['items'][0]['id']

    print(f'Searched artist is ... "{artist_name}"')
    # TODO: maybe display more artist info

    return artist_name, artist_id


def get_top_tracks_by_artist_id(auth, artist_id):
    json_res = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks',
                                          headers=auth).json()
    tracks = json_res['tracks']
    number_of_tracks = 5    # max 10
    top_tracks = []
    for track in tracks[:number_of_tracks]:
        track_title = track['name']
        album_title = track['album']['name']
        release_date = track['album']['release_date']
        spotify_url = track['external_urls']['spotify']

        top_tracks.append(f'{track_title} - {album_title} {release_date} {spotify_url}')

    return top_tracks


def main(artist_search_term):
    token = get_token()
    artist_name, artist_id = get_artist_id(token, artist_search_term)
    top_track_info = get_top_tracks_by_artist_id(token, artist_id)
    get_video.youtube_video(f'{artist_name} {top_track_info[0]}')
    return { artist_name : top_track_info }


if __name__ == '__main__':
    main(artist_search_term=None)


# TODO
#  - test more features from Spotify API. maybe related artist?
#  - exception/error handling