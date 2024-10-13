from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
import os
import logging


api_name_version_index = 'https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md#youtube'
service_name = 'youtube'
service_version = 'v3'
api_key = os.environ.get('DEVELOPER_KEY')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def youtube_video(search_term):
    title_field = 'items(snippet/title)'
    video_id_field = 'items(id/videoId)'

    try:
        youtube = build(service_name, service_version, developerKey=api_key)

        response = youtube.search().list(
            part='snippet', # required
            maxResults=1,
            q=search_term + 'music video',   # adding music video to search yields slightly better results
            type='video',
            videoCategoryId=10,     # in US music video category is 10
            fields=f'{title_field},{video_id_field}'
        ).execute()

        youtube.close()

    except (UnknownApiNameOrVersion, HttpError, Exception) as error:
        match error:
            case UnknownApiNameOrVersion():
                print(f'Error unknown API name or version: {error}, supported APIs: {api_name_version_index}')
            case HttpError():
                print(f'Error response status code: {error.status_code}, reason: {error.error_details}')
            case Exception():
                print(f'Error: {error}')

    else:
        for data in response.get('items', []):
            video_title = data['snippet']['title']
            video_id = data['id']['videoId']

            chosen_video = f'{video_title} : {video_id}'
            # chosen_video = [video_title, video_id]
            # chosen_video = {'title': video_title, 'video_id': video_id}
            print(chosen_video)
            # return chosen_video
