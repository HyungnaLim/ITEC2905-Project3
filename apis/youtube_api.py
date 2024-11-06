"""
Uses Google API Python Client to search YouTube for music videos in a given search term. Requires valid API
token to authenticate the Google API client. Returns dictionary of video title, video ID and video thumbnail.
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
import html
import logging
# import os

# name and version index for supported APIs
name_version_index = 'https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md#youtube'
service_name = 'youtube'
service_version = 'v3'
# api_key = os.environ.get('YOUTUBE_API_KEY')   # insert api key into DEVELOPER_KEY env variable


def main(search_term):
    try:
        with (build(service_name, service_version, developerKey='AIzaSyDwqLyFMv40cYjRW8jUEQyBgD-nvxR_PwY')
              as request):
            response = request.search().list(
                    part='snippet',
                    maxResults=1,
                    q=f'{search_term} music video',
                    type='video',
                    videoCategoryId=10,
                    fields=f'items(snippet/title),items(id/videoId),items(snippet/thumbnails/high/url)'
                ).execute()

        youtube_video, error_message = response_data_extraction(response)
        if error_message:
            return None, error_message
        return youtube_video, None

    except (UnknownApiNameOrVersion, HttpError, Exception) as e:
        match e:
            case UnknownApiNameOrVersion():
                logging.exception(e)
                return None, f'Error, unknown YouTube API name or version: {e}. Supported APIs: {name_version_index}'
            case HttpError():
                logging.exception(e)
                return None, f'Error, YouTube response status code: {e.status_code}, reason: {e.error_details}'
            case Exception():
                logging.exception(e)
                return None, f'YouTube API Error: {e}'


def response_data_extraction(api_response_data):
    try:
        for data in api_response_data.get('items', []):
            video_title = html.unescape(data['snippet']['title'])
            video_id = data['id']['videoId']
            video_thumbnail = data['snippet']['thumbnails']['high']['url']

            chosen_video = { 'video_title': video_title, 'video_id': video_id, 'thumbnail': video_thumbnail }
            return chosen_video, None

    except (KeyError, Exception) as e:
        match e:
            case KeyError():
                logging.exception(e)
                return None, f'YouTube data extraction KeyError: {e}'
            case Exception():
                logging.exception(e)
                return None, f'YouTube data extraction error: {e}'