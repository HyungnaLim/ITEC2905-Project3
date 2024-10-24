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
service_name = 'youtube'
service_version = 'v3'
# api_key = os.environ.get('DEVELOPER_KEY')   # insert api key into DEVELOPER_KEY env variable

def main(search_term):
    video_title = 'items(snippet/title)'
    video_id = 'items(id/videoId)'
    video_thumbnail = 'items(snippet/thumbnails/high/url)'

    try:
        with (build(service_name, service_version, developerKey='AIzaSyDwqLyFMv40cYjRW8jUEQyBgD-nvxR_PwY')
              as youtube_build):
            youtube_query = youtube_build.search().list(
            part='snippet',
            maxResults=1,
            q=f'{search_term} music video',
            type='video',
            videoCategoryId=10,
            fields=f'{video_title},{video_id},{video_thumbnail}' # returns only specific data
        )

        response, error_message = request_youtube_video(youtube_query)
        chosen_video, error_message = api_data_extraction(response)
        if error_message:
            return None, error_message
        return chosen_video, None

    except Exception as e:
        print(f'{e}')
        return None, e


def request_youtube_video(request_video):
    try:
        youtube_video = request_video.execute()
        return youtube_video, None

    except (UnknownApiNameOrVersion, HttpError, Exception) as e:
        match e:
            case UnknownApiNameOrVersion():
                err_msg = f'Error unknown YouTube API name or version: {e}, supported APIs: {api_name_version_index}'
                return None, err_msg
            case HttpError():
                err_msg = f'Error YouTube response status code: {e.status_code}, reason: {e.error_details}'
                return None, err_msg
            case Exception():
                err_msg = f'YouTube API Error: {e}'
                return None, err_msg


def api_data_extraction(api_response_data):
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
                err_msg = f'YouTube data extraction KeyError: {e}'
                return None, err_msg
            case Exception():
                err_msg = f'YouTube data extraction error: {e}'
                return None, err_msg