"""Using Google API Client Library for Python:
https://github.com/googleapis/google-api-python-client?tab=readme-ov-file

User will need to have a Google account and create an api key here:
https://console.cloud.google.com/apis/credentials

Starting code from here:
https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md#build-the-service-object

Index of modules and classes available to googleapiclient:
https://googleapis.github.io/google-api-python-client/docs/epy/index.html

take artist name and top 5 songs from spotify api module?
"""

# using build function from discovery module
# https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build
from googleapiclient.discovery import build
# the only errors that seemed relevant
# https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.errors.Error-class.html
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
import os
import logging

# build() takes api service name and corresponding version args - we're using YouTube api services
# https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md#youtube
api_name_version_index = 'https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md#youtube'
service_name = 'youtube'
service_version = 'v3'

# for api requests, build() takes developerKey arg which is the users API key
# https://github.com/googleapis/google-api-python-client/blob/main/docs/api-keys.md
api_key = os.environ.get('DEVELOPER_KEY')

# https://github.com/googleapis/google-api-python-client/blob/main/docs/logging.md
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# testing queries
test_search = 'Radiohead'
test_search_no_music_video = 'Radiohead Decks Dark' # how to distinguish video and music video if needed
test_search2 = 'Radiohead Creep'
test_search_top_5 = {'radiohead':['creep',      # sample data structure from spotify api??
                                  'no surprises',
                                  'karma police',
                                  'high and dry',
                                  'jigsaw falling into place'
                                  ]}

# def main(video_search_term):
#     # youtube_video(test_search)
#     # youtube_video(test_search2)
#     # print(test_search2)
#     # youtube_video(test_search_no_music_video)
#     # youtube_video(test_search_top_5)
#     print(video_search_term)
#     youtube_video(video_search_term)


def youtube_video(search_term):
    print(search_term)
    title_field = 'items(snippet/title)'
    video_id_field = 'items(id/videoId)'

    try:
        youtube = build(service_name, service_version, developerKey=api_key)

        # search params are used in 'list' method after search()
        # https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.search.html
        response = youtube.search().list(
            part='snippet', # required
            maxResults=1,
            q=search_term + 'music video',   # adding music video to search yields slightly better results
            type='video',
            videoCategoryId=10,     # in US music video category is 10
            # fields parameter yields partial response for needed data
            # fields='items/snippet/title,items/id/videoId'
            fields=f'{title_field},{video_id_field}'
        ).execute()

        youtube.close()
        # print(response)

    # https://realpython.com/python-catch-multiple-exceptions/
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

            # return str/list/dict - will update for whatever flask needs
            chosen_video = f'{video_title} : {video_id}'
            # chosen_video = [video_title, video_id]
            # chosen_video = {'title': video_title, 'video_id': video_id}
            print(chosen_video)
            # return chosen_video


# if __name__ == '__youtube_video__':
#     youtube_video()