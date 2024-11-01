import unittest
from unittest import TestCase
from unittest.mock import patch, call
from apis.youtube_api import main, YoutubeError, get_youtube_video, response_data_extraction


class TestMain(TestCase):

    # https://docs.python.org/3/library/unittest.mock.html#nesting-patch-decorators
    @patch('apis.youtube_api.get_youtube_video')
    @patch('apis.youtube_api.response_data_extraction')
    def test_main(self, mock_response_data_extraction, mock_get_youtube_video):

        # artist info from spotify api
        artist_info = 'artist name track title'

        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.return_value
        # dict represents json response from youtube api call
        mock_json_response = {'title': 'video title'}
        mock_get_youtube_video.return_value = mock_json_response

        # return key:value extracted from json
        mock_extract_dict = {'video_title': 'video_title'}
        mock_response_data_extraction.return_value = mock_extract_dict

        music_video, youtube_error = main(artist_info)

        self.assertEqual(music_video, mock_extract_dict)
        self.assertIsNone(youtube_error)
        mock_get_youtube_video.assert_called_once_with(artist_info)
        mock_response_data_extraction.assert_called_once_with(mock_json_response)

    @patch('apis.youtube_api.get_youtube_video')
    @patch('apis.youtube_api.response_data_extraction')
    def test_main_error(self, mock_extract, mock_get_video):

        # artist info from spotify apigit 
        artist_info = 'artist name track title'

        # return error message when raised
        mock_get_video.side_effect = YoutubeError('error message')

        music_video, youtube_error = main(artist_info)

        self.assertIsNone(music_video)
        self.assertIsInstance(youtube_error, YoutubeError)
        mock_get_video.assert_called_once_with(artist_info)
        mock_extract.assert_not_called()

    #
    #     # call main with tuple
    #     music_video, youtube_error = main(artist_info)
    #
    #     # youtube error should return None
    #     self.assertIsNone(youtube_error)
    #     # passed artist info on to get youtube video
    #     mock_get_youtube_video.assert_called_once_with(artist_info)
    #
    #
    # @patch('apis.youtube_api.response_data_extraction')
    # def test_main_response_data_extraction(self, mock_response_data_extraction):
    #     artist_info = 'artist name track title'
    #     mock_response = 'json_response'
    #     # youtube video extracted from json data
    #     mock_youtube_video = 'dict of video'
    #     # return value should be the of video data
    #     mock_response_data_extraction.side_effect = mock_youtube_video
    #
    #     music_video, youtube_error = main(artist_info)
    #
    #     # music video should be the extracted and formatted video data
    #     self.assertEqual(music_video, mock_response_data_extraction)
    #     self.assertIsNone(youtube_error)
    #     # passed json response on to data extraction
    #     mock_response_data_extraction.assert_called_once_with(mock_response)


if __name__ == '__main__':
    unittest.main()