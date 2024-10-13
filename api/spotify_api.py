import requests
import os
import api.youtube_api as get_video
from pprint import *


def get_token():
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    grant_type = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}

    json_res = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=grant_type).json()
    # pprint(json_res)

    token_type = json_res.get('token_type')
    access_token = json_res.get('access_token')

    token_str = f'{token_type} {access_token}'
    auth = {'Authorization': token_str}

    return auth


def get_artist_id(auth, artist_search_term):
    endpoint = 'https://api.spotify.com/v1/search'

    search_query = {'q': artist_search_term, 'type': 'artist', 'limit': 3}

    search_response = requests.get(endpoint, params=search_query, headers=auth).json()
    # pprint(search_response)
    artist = search_response.get('artists')
    # items = artist.get(0)

    # artist_name = artist.get('name')
    # artist_id = artist.get('id')

    artist_name = artist['items'][0]['name']
    artist_id = artist['items'][0]['id']

    print(f'Searched artist is ... "{artist_name}"')
    # TODO: maybe display more artist info

    return artist_name, artist_id


def get_top_tracks_by_artist_id(auth, artist_id):
    json_res = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks',
                                          headers=auth).json()
    tracks = json_res['tracks']
    # pprint(tracks)
    # track_ids = []
    number_of_tracks = 5    # max 10
    top_tracks = []
    # sliced https://stackoverflow.com/questions/2688079/how-to-iterate-over-the-first-n-elements-of-a-list
    for track in tracks[:number_of_tracks]:
        # track_ids.append(tracks['id'])
        track_title = track['name']
        album_title = track['album']['name']
        release_date = track['album']['release_date']
        spotify_url = track['external_urls']['spotify']

        top_tracks.append(f'{track_title} - {album_title} {release_date} {spotify_url}')

        # print(track_title, album_title, release_date, spotify_url)
    return top_tracks
    # get_video.youtube_video(f'Radiohead {tracks[0]['name']}')
    # return track_ids


# def get_track_info_by_track_id(auth, artist_name, track_ids):
#     print(f'\nTop Tracks of {artist_name}')
#
#     for track_id in track_ids:
#         json_res = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=auth).json()
#
#         track_title = json_res['name']
#         album_title = json_res['album']['name']
#         release_date = json_res['album']['release_date']
#         spotify_url = json_res['external_urls']['spotify']
#
#         print(track_title, album_title, release_date, spotify_url)



def main(artist_search_term):
    token = get_token()
    artist_name, artist_id = get_artist_id(token, artist_search_term)
    top_track_info = get_top_tracks_by_artist_id(token, artist_id)  # can get all info from data in this call
    # tracks = get_top_tracks_by_artist_id(token, artist_id)
    # get_track_info_by_track_id(token, artist_name, tracks)  # app is making 8 api calls
    # get_video.youtube_video(f'{artist_name} {tracks[0]}')
    get_video.youtube_video(f'{artist_name} {top_track_info[0]}')
    return { artist_name : top_track_info }


if __name__ == '__main__':
    main(artist_search_term=None)


# TODO
#  - test more features from Spotify API. maybe related artist?
#  - exception/error handling