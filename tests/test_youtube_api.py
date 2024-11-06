import os
import json
import unittest
from unittest import TestCase
from unittest.mock import patch
from apis.youtube_api import main, YoutubeError, get_youtube_video, response_data_extraction
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
from googleapiclient.http import HttpMock

# https://github.com/googleapis/google-api-python-client/blob/main/docs/mocks.md
# https://github.com/googleapis/google-api-python-client/tree/main/tests

# directory to json file
DATA_DIR = os.path.join(os.path.dirname(__file__), 'resources')

def datafile(filename):
    return os.path.join(DATA_DIR, filename)

def read_datafile(filename, mode='r'):
    with open(datafile(filename), mode=mode) as f:
        return f.read()


class TestMain(TestCase):

    # https://docs.python.org/3/library/unittest.mock.html#nesting-patch-decorators
    @patch('apis.youtube_api.get_youtube_video')
    @patch('apis.youtube_api.response_data_extraction')
    def test_main(self, mock_response_data_extraction, mock_get_youtube_video):

        # artist info from spotify api
        artist_info = 'artist name track title'

        mock_json_response = read_datafile('youtube.json')
        mock_get_youtube_video.return_value = mock_json_response

        # return key:value extracted from json
        mock_extract_dict = {'video_title': 'video title'}
        mock_response_data_extraction.return_value = mock_extract_dict

        music_video, youtube_error = main(artist_info)

        # returned music video should match extracted data
        self.assertEqual(music_video, mock_extract_dict)

        # youtube error should return none
        self.assertIsNone(youtube_error)

        # passed info to call youtube api
        mock_get_youtube_video.assert_called_once_with(artist_info)
        mock_response_data_extraction.assert_called_once_with(mock_json_response)

    @patch('apis.youtube_api.get_youtube_video')
    @patch('apis.youtube_api.response_data_extraction')
    def test_main_raised_youtube_error(self, mock_extract, mock_get_video):

        artist_info = 'artist name track title'

        # return error message when raised
        mock_get_video.side_effect = YoutubeError('error message')

        music_video, youtube_error = main(artist_info)

        self.assertIsNone(music_video)
        self.assertIsInstance(youtube_error, YoutubeError)
        mock_get_video.assert_called_once_with(artist_info)
        mock_extract.assert_not_called()


# class TestGetYouTubeVideo(TestCase):
#
#     @patch('apis.youtube_api.build')
#     def test_get_youtube_video(self, mock_build):
#         artist_info = 'artist name track title'
#
#         mock_build = build('youtube', 'v3', http=self.http, static_discovery=False)
#         mock_api_request = mock_build.search().list().execute().return_value
#
#         mock_api_request.return_value = datafile('youtube.json')
#
#         mock_build.return_value.__enter__.return_value = mock_api_request
#
#         response = get_youtube_video(artist_info)
#
#         self.assertTrue(getattr(mock_build, 'items'))
#         self.assertEqual(response, datafile('youtube.json'))
    # credentials = { service_name: 'youtube', service_version: 'v3', api_key: '123' }
    #
    # mock_api_request = mock_service.search().list().execute().return_value
#     mock_api_request.return_value = read_datafile('youtube.json')
#
#     mock_build.return_value.__enter__.return_value = mock_service
#
#     response = get_youtube_video(artist_info)
#
#     self.assertEqual(response, {
#         'items': [
#             {
#                 'snippet': {
#                     'title': 'video title',
#                     'thumbnails': { 'high': { 'url': 'thumb_url' }},
#                 'id': { 'videoId': 'video_id' }}
#             }
#         ]
#     })
#
#     mock_build.assert_called_once_with(mock_service)


class TestResponseDataExtraction(TestCase):

    def test_correct_data_from_response_data_extraction(self):
        api_response_data = json.loads(read_datafile('youtube.json'))

        expected_result = {
            'video_title': 'video title',
            'video_id': 'video id',
            'thumbnail': 'thumb url'
        }

        actual_response = response_data_extraction(api_response_data)
        self.assertEqual(actual_response, expected_result)


    def test_key_error_from_response_data_extraction(self):
        # JSON where ID value is deleted
        api_response_data_missing_id = json.loads(read_datafile('no_id_youtube.json'))

        with self.assertRaises(YoutubeError) as context:
            response_data_extraction(api_response_data_missing_id)

        self.assertIn('YouTube data extraction error:', f'{context.exception}')


if __name__ == '__main__':
    unittest.main()