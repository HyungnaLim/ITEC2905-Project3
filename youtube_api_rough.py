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
import os

# build() takes api service name and corresponding version args - we're using YouTube api services
# https://github.com/googleapis/google-api-python-client/blob/main/docs/dyn/index.md#youtube
service_name = 'youtube'
service_version = 'v3'

# for api requests, build() also takes developerKey arg which is the users API key
# https://github.com/googleapis/google-api-python-client/blob/main/docs/api-keys.md
api_key = os.environ.get('DEVELOPER_KEY')

test_search = 'Radiohead' # imported_search_query_from_user_or_spotify_data
test_search_no_music_video = 'Radiohead Decks Dark' # how to distinguish video and music video if needed
test_search2 = 'Radiohead Creep'
test_search_top_5 = {'radiohead':['creep',      # sample data structure from spotify api??
                                  'no surprises',
                                  'karma police',
                                  'high and dry',
                                  'jigsaw falling into place'
                                  ]}

def main():     # testing
    # youtube_video(test_search)
    youtube_video(test_search2)
    # youtube_video(test_search_no_music_video)
    # youtube_video(test_search_top_5)

def youtube_video(search):
    try:
        youtube = build(service_name, service_version, developerKey=api_key)

        # search params are used in 'list' method after search()
        # https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.search.html
        response = youtube.search().list(
            part='snippet', # required
            maxResults=1,
            q=search + 'music video',
            type='video',
            videoCategoryId=10
        ).execute()

        video_id = response['items'][0]['id']['videoId']

        # direct_url = f'https://www.youtube.com/watch?v={video_id}'

        # video = response['items'][0]    # refine to data needed
        # print(video)

        # title = video['snippet']['title']
        # description = video['snippet']['description']
        # thumb = video['snippet']['thumbnails']['high']['url']

        # ids = 'Del3C2W63Pk'
        video_description = youtube.videos().list(id=video_id, part='snippet').execute()
        for data in video_description.get('items', []):
            print(data['id'])
            print(data['snippet']['description'])
            print(data['snippet']['title'])
            print()

        # print(response)
        # print(response['items'])
        # print(response['items'][0])
        # print(response['items'][0]['snippet'])
        # print(response['items'][0]['snippet']['title']) # path to title
        # print(response['items'][0]['snippet']['description'])   # path to desc
        # print(response['items'])
        # print(response['items'][0])
        # print(response['items'][0]['id'])
        # print(response['items'][0]['id']['videoId']) # path to video url id

        youtube.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()