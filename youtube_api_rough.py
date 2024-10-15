"""
Uses YouTube Data API to search for music videos by artist name in a given search term.
Requires valid YouTube API token to authenticate the Google API client. Returns dictionary
of video title and video ID.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
import os

service_name = 'youtube'
service_version = 'v3'
api_key = os.environ.get('DEVELOPER_KEY')   # insert api key into DEVELOPER_KEY env variable
# name and version index for supported APIs
api_name_version_index = 'https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md#youtube'

def youtube_video(search_term):
    """ Search for music videos on YouTube by given search term
    :param search_term:
    :return dictionary of video title and video ID:
    """

    try:
        youtube = build(service_name, service_version, developerKey=api_key)
        response = youtube.search().list(
            part='snippet',
            maxResults=1,
            q=f'{search_term} music video',
            type='video',
            videoCategoryId=10, # in US music video category is 10
            fields='items(snippet/title),items(id/videoId)' # returns only specific data
        ).execute()
        youtube.close()

        video_data = api_data_extraction(response)
        return video_data

    except (UnknownApiNameOrVersion, HttpError, Exception) as error:
        match error:
            case UnknownApiNameOrVersion():
                print(f'Error unknown YouTube API name or version: {error}, supported APIs: {api_name_version_index}')
            case HttpError():
                print(f'Error YouTube response status code: {error.status_code}, reason: {error.error_details}')
            case Exception():
                print(f'YouTube API Error: {error}')


def api_data_extraction(api_response_data):
    try:
        for data in api_response_data.get('items', []):
            video_title = data['snippet']['title']
            video_id = data['id']['videoId']

            chosen_video = {'video_title': video_title, 'video_id': video_id}
            return chosen_video

    except (KeyError, Exception) as error:
        match error:
            case KeyError():
                print(f'YouTube data extraction KeyError: {error}')
            case Exception():
                print(f'YouTube data extraction error: {error}')

