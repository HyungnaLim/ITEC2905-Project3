"""
Uses YouTube Data API to search for music videos by artist name in a given search term.
Requires valid YouTube API token to authenticate the Google API client. Returns dictionary
of video title, video ID and video thumbnail.
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
import html
import os

# name and version index for supported APIs
api_name_version_index = 'https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md#youtube'

def main(search_term):
    api_builder = google_api_details()
    api_request_details = get_request_details(api_builder, search_term)
    chosen_video = get_youtube_video(api_request_details)
    return chosen_video


def google_api_details():
    service_name = 'youtube'
    service_version = 'v3'
    # api_key = os.environ.get('DEVELOPER_KEY')   # insert api key into DEVELOPER_KEY env variable

    with build(service_name, service_version, developerKey='AIzaSyDwqLyFMv40cYjRW8jUEQyBgD-nvxR_PwY') as youtube_build:
        return youtube_build


def get_request_details(api_build, search_term):
    video_title = 'items(snippet/title)'
    video_id = 'items(id/videoId)'
    video_thumbnail = 'items(snippet/thumbnails/high/url)'

    google_api_request = api_build.search().list(
        part='snippet',
        maxResults=1,
        q=f'{search_term} music video',
        type='video',
        videoCategoryId=10, # in US music video category is 10
        fields=f'{video_title},{video_id},{video_thumbnail}' # returns only specific data
    )
    return google_api_request


def get_youtube_video(request_details):
    response = request_youtube_video(request_details)
    video_data = api_data_extraction(response)
    return video_data


def request_youtube_video(request_video):
    try:
        youtube_video = request_video.execute()
        return youtube_video

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
            video_title = html.unescape(data['snippet']['title'])
            video_id = data['id']['videoId']
            video_thumbnail = data['snippet']['thumbnails']['high']['url']

            chosen_video = { 'video_title': video_title, 'video_id': video_id, 'thumbnail': video_thumbnail }
            return chosen_video

    except (KeyError, Exception) as error:
        match error:
            case KeyError():
                print(f'YouTube data extraction KeyError: {error}')
            case Exception():
                print(f'YouTube data extraction error: {error}')