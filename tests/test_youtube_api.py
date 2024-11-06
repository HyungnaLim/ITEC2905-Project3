import unittest
from unittest import TestCase
from unittest.mock import patch, call
from apis.youtube_api import main, YoutubeError, get_youtube_video, response_data_extraction, service_name
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
from googleapiclient.http import HttpMock

# https://github.com/googleapis/google-api-python-client/tree/main/tests

class TestMain(TestCase):

    # https://docs.python.org/3/library/unittest.mock.html#nesting-patch-decorators
    @patch('apis.youtube_api.get_youtube_video')
    @patch('apis.youtube_api.response_data_extraction')
    def test_main(self, mock_response_data_extraction, mock_get_youtube_video):

        # artist info from spotify api
        artist_info = 'artist name track title'

        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.return_value
        # dict represents json response from youtube api call
        mock_json_response = {
            'items': [
                {
                    'snippet': {
                        'title': 'video title',
                        'thumbnails': { 'high': { 'url': 'thumb_url' }},
                    'id': { 'videoId': 'video_id' }}
                }
            ]
        }

        mock_get_youtube_video.return_value = mock_json_response

        # return key:value extracted from json
        mock_extract_dict = {'video_title': 'video_title'}
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
    def test_main_raised_error(self, mock_extract, mock_get_video):

        artist_info = 'artist name track title'

        # return error message when raised
        mock_get_video.side_effect = YoutubeError('error message')

        music_video, youtube_error = main(artist_info)

        self.assertIsNone(music_video)
        self.assertIsInstance(youtube_error, YoutubeError)
        mock_get_video.assert_called_once_with(artist_info)
        mock_extract.assert_not_called()


class TestGetYouTubeVideo(TestCase):

    @patch('apis.youtube_api.build')
    def test_get_youtube_video(self, mock_build):
        self.http = HttpMock({
            'items': [
                {
                    'snippet': {
                        'title': 'video title',
                        'thumbnails': { 'high': { 'url': 'thumb_url' }},
                    'id': { 'videoId': 'video_id' }}
                }
            ]
        }, {'status': '200'})

        mock_build = build('youtube', 'v3', http=self.http, static_discovery=False)



    # def test_unknown_api_name_or_version(self):
    #     http = HttpMockSequence(
    #         [
    #             ({"status": "404"}, read_datafile("zoo.json", "rb")),
    #             ({"status": "404"}, read_datafile("zoo.json", "rb")),
    #         ]
    #     )
    #     with self.assertRaises(UnknownApiNameOrVersion):
    #         plus = build("plus", "v1", http=http, cache_discovery=False)
    # def test_full_featured(self):
    #     # Zoo should exercise all discovery facets
    #     # and should also have no future.json file.
    #     self.http = HttpMock(datafile("zoo.json"), {"status": "200"})
    #     zoo = build("zoo", "v1", http=self.http, static_discovery=False)
    #     self.assertTrue(getattr(zoo, "animals"))
    #
    #     request = zoo.animals().list(name="bat", projection="full")
    #     parsed = urllib.parse.urlparse(request.uri)
    #     q = urllib.parse.parse_qs(parsed.query)
    #     self.assertEqual(q["name"], ["bat"])
    #     self.assertEqual(q["projection"], ["full"])
    # def test_discovery_with_valid_version_uses_v1(self):
    #     http = HttpMockSequence(
    #         [
    #             ({"status": "200"}, read_datafile("zoo.json", "rb")),
    #         ]
    #     )
    #     build(
    #         "zoo",
    #         version="v123",
    #         http=http,
    #         cache_discovery=False,
    #         static_discovery=False,
    #     )
    #     validate_discovery_requests(self, http, "zoo", "v123", V1_DISCOVERY_URI)
    #     artist_info = 'artist name track title'
    #     # credentials = { service_name: 'youtube', service_version: 'v3', api_key: '123' }
    #     #
    #     # mock_api_request = mock_service.search().list().execute().return_value
    #     mock_api_request.return_value = {
    #         'items': [
    #             {
    #                 'snippet': {
    #                     'title': 'video title',
    #                     'thumbnails': { 'high': { 'url': 'thumb_url' }},
    #                 'id': { 'videoId': 'video_id' }}
    #             }
    #         ]
    #     }
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




if __name__ == '__main__':
    unittest.main()