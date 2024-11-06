"""Program to search YouTube for videos.

Uses Google API Python Client to build query, then search YouTube for videos with a given search term.
Requires valid API token to authenticate client. Returns data for video or error message.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
from dotenv import load_dotenv
import html
import logging
import os
load_dotenv()

service_name = 'youtube'
service_version = 'v3'
api_key = os.environ.get('DEVELOPER_KEY')


def main(artist_info):
    """Return video data from search.

    Pass search string to the YouTube call, then pass the response to extract music video data.

    Return:
        tuple - A tuple containing either:
        - (video_data, None) if successful, where video data is a dictionary.
        - (None, error_message) if error raised, where error_message describes the error.

    Example:
        >main('The Beatles Here Comes The Sun')
        return ({
            'video_title': 'The Beatles - Here Comes The Sun (2019 Mix)',
            'video_id': 'KQetemT1sWc',
            'thumbnail': 'https://i.ytimg.com/vi/KQetemT1sWc/hqdefault.jpg'}, None)
    """
    try:
        response = get_youtube_video(artist_info)
        youtube_video = response_data_extraction(response)

        return youtube_video, None

    except YoutubeError as e:
        logging.exception(e)
        return None, e


def get_youtube_video(search_term):
    """Return JSON response data from YouTube search.

    Args:
        search_term: string used to search for the video.

    Return:
        dict: JSON formatted response containing video data.

    Example:
        >get_youtube_video('The Beatles Here Comes The Sun')
        return {
                    'items': [
                        {
                            'snippet': { 'title': 'The Beatles - Here Comes The Sun (2019 Mix)' },
                            'id': { 'videoId': 'KQetemT1sWc' },
                            'snippet': { 'thumbnails': { 'high': { 'url': 'thumbnail url' }}}
                        }
                    ]
                }
    """
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

        return response

    except (UnknownApiNameOrVersion, HttpError) as e:
        match e:
            case UnknownApiNameOrVersion():
                raise YoutubeError(f'Error, unknown YouTube API name or version: {e}.')
            case HttpError():
                raise YoutubeError(f'Error, YouTube response status code: {e.status_code}, reason: {e.error_details}')


def response_data_extraction(api_response_data):
    """Return video details.

    Extract details from json data, format to dict of video title, id, and thumbnail.

    Return:
        A dict mapping keys to video details.
    Raises:
        KeyError: YouTube data extraction mismatch.
    """
    try:
        for data in api_response_data.get('items', []):
            video_title = html.unescape(data['snippet']['title'])
            video_id = data['id']['videoId']
            video_thumbnail = data['snippet']['thumbnails']['high']['url']

            chosen_video = { 'video_title': video_title, 'video_id': video_id, 'thumbnail': video_thumbnail }
            return chosen_video

    except KeyError as e:
        raise YoutubeError(f'YouTube data extraction error: {e}')


class YoutubeError(Exception):
    """Handle YouTube errors."""
    pass
